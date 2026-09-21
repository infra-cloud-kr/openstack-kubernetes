.. _nova-libvirt-kvm:

===============================================
Nova 의 VM 생성과 자원 격리 (libvirt / KVM)
===============================================

OpenStack on Kubernetes(openstack-helm) 환경에서 Nova 가 인스턴스 생성 요청을 받아
Kubernetes 생태계와 호스트 커널을 거쳐 실제 QEMU 프로세스를 띄우기까지의 전체 과정을 정리합니다.



Nova 에서 VM 이 만들어지기까지
===============================

요청 경로: nova-api 에서 nova-compute 까지
--------------------------------------------

#. **nova-api** — Keystone 으로 토큰을 검증하고, 자원 한도를 확인한 뒤,
   DB에 가상 머신 생성을 위한 정보를 기록합니다.
   이후 nova-conductor 에게 요청을 전달합니다.
#. **nova-conductor** — nova-api로부터 받은 요청을 처리합니다.
   nova-scheduler를 호출해 생성 위치를 정하고, DB 프록시(대리인) 역할을 수행하며,
   최종적으로 선택된 nova-compute에 VM 생성을 지시합니다.
#. **nova-scheduler + Placement** — nova-scheduler는 Placement에게
   vCPU/RAM/디스크 등 조건을 만족하는 컴퓨트 노드를 물어 후보
   목록을 받고, 그중 필터와 가중치를 적용해 최종 호스트를 고릅니다.
   선택이 끝나면 Placement 에 기록(claim)합니다.
#. **nova-compute** — 선택된 컴퓨트 노드의 nova-compute Pod로 요청이 전달됩니다.
   nova-compute는 Glance에서 이미지를 받아오고, Neutron에 네트워크 포트를,
   Cinder에 볼륨을 요청해 VM을 구성합니다.
#. **Pod 간 UNIX 소켓 통신** — openstack-helm 환경에서 nova-compute와 libvirt는 각각 별도의
   DaemonSet Pod로 실행됩니다.
   nova-compute는 도메인 XML을 생성한 후,
   두 Pod가 공유 마운트한 호스트 경로 상의 UNIX 소켓(RPC)을 통해 libvirt Pod 내부의 libvirtd에 전달합니다.


libvirt Pod의 호스트 접근 권한 확보
------------------------------------------------------------------------

컨테이너는 기본적으로 호스트 커널 및 하드웨어 접근이 제한(unprivileged)되어 있으나,
libvirtd는 KVM 제어와 장치 할당을 위해 호스트 권한이 필요합니다.

#. **Pod의 Privileged 모드 설정** — libvirt Pod를 privileged 모드로 실행하여,
   호스트의 실제 디렉터리를 직접 마운트하여 제어합니다.
#. **kubelet cgroup 계층 탈출** - Pod는 기본적으로 kubelet이 관리하는
   cgroup 계층(kubepods) 아래에서 실행됩니다.
   그러나 libvirtd가 이 안에 갇혀 있으면 자식 프로세스인 QEMU도 Pod의 리소스 제한을 받게 됩니다.
   이는 VM의 자원 할당에 제약의 원인이 되므로, libvirt Pod는 호스트 권한을 사용하여 이 계층을 벗어나,
   직접 cgroup을 생성하고 libvirtd의 cgroup을 system.slice 아래로 이동시킵니다.

.. code-block:: console

   # libvirt Pod 내부에서 호스트 cgroup 루트에 직접 접근합니다.
   + cgcreate -g cpu,hugetlb,memory,rdma,misc,pids:/osh-libvirt
   + cgexec -g cpu,hugetlb,memory,rdma,misc,pids:/osh-libvirt \
       systemd-run --scope --slice=system libvirtd --listen
   Running as unit: run-r0cc5ced77b7e40db9c8767d441d96e79.scope

#. ``cgcreate`` 로 cgroup 루트 아래에 ``/osh-libvirt`` 를 직접 만듭니다.
#. ``cgexec`` 로 그 cgroup 으로 이동해 kubelet 이 만든 계층을 벗어난 뒤,
   ``systemd-run --scope --slice=system`` 을 통해 libvirtd 를 호스트 systemd 의
   ``system.slice`` 아래 scope에 새롭게 등록합니다.
#. 컨테이너의 최초 프로세스는 ``systemd-run`` 으로 남아 libvirtd 를 감시합니다.
   libvirtd 가 죽으면 함께 종료되고, Kubernetes 가 Pod 를 다시 띄웁니다.

.. code-block:: console

   $ cat /proc/<libvirtd PID>/cgroup
   0::/system.slice/run-rd2beada6c25e4baf90db578cc514c194.scope

결과적으로 libvirtd는 ``system.slice`` 에 속한 데몬처럼 동작하면서도,
수명 주기는 Kubernetes 의 선언적 관리 아래 남습니다.

libvirtd 가 QEMU 프로세스를 생성하는 과정 (Double Fork & Machine Cgroup)
------------------------------------------------------------------------------------

libvirtd는 nova-compute로부터 받은 도메인 XML(vCPU, 메모리, 가상 디스크, NIC 설정 등)을
해석해 QEMU를 구성하고 프로세스를 생성합니다.

#. Double Fork와 서브리퍼(Subreaper) : libvirtd는 Double fork를 하고
   cgroup을 분리하여 QEMU를 생성합니다.
   이는 **libvirtd 가 재시작, 크래시해도 실행 중인 VM 이 함께 죽지 않도록** 독립시키기 위해서입니다.
   double fork 과정에서 중간 프로세스가 종료되면서 QEMU 는 고아 프로세스가 되고,
   가장 가까운 서브리퍼가 부모 프로세스로 매핑되게 됩니다.

#. Machine cgroup 격리 : libvirtd는 system.slice에 위치하지만,
   생겨난 QEMU 프로세스는 호스트 cgroup 루트 직하의 가상화 전용 구역인 machine 계층으로 이동시킵니다.
   이를 통해 시스템 데몬들과 VM의 자원을 격리하여 VM이 호스트 시스템에 영향을 주지 않도록 합니다.

#. 보안 레이블 및 네임스페이스 :

   - sVirt (SELinux/AppArmor): VM 간 이미지 무단 접근을 차단하기 위해
     QEMU 프로세스와 디스크 파일에 고유 MCS 레이블을 부여합니다.
   - Mount Namespace: QEMU의 /dev 경로를 호스트와 분리하여
     해당 VM에 허용된 가상 장치 파일만 노출합니다.
   - 권한 축소: root 권한이 아닌 libvirt-qemu 유저/그룹 권한으로 실행 단계를 낮춥니다.

.. code-block:: console

   # QEMU의 부모 PID 를 확인합니다.
   $ ps -o pid,ppid,comm -p <QEMU PID>
       PID    PPID COMMAND
     82518   40593 qemu-system-x86

   # QEMU의 부모 프로세스를 조회합니다.
   $ ps -o pid,ppid,comm,args -p 40593
       PID    PPID COMMAND         COMMAND
     40593       1 containerd-shim /usr/bin/containerd-shim-runc-v2 ...

   # QEMU 의 cgroup 경로를 확인합니다.
   $ cat /proc/<QEMU PID>/cgroup
   0::/machine/qemu-1-instance-00000001.libvirt-qemu/emulator

.. note::

   위 cgroup 경로는 ``machine.slice`` 가 아니라
   cgroup 루트 바로 아래의 ``machine`` 계층으로 관찰됩니다.
   Pod를 privileged 모드로 실행하더라도 기본적으로는 호스트의 systemd의 D-Bus에 접근할 수 없으므로,
   호스트의 systemd에게 cgroup 등록을 요청할 수 없습니다.
   따라서 libvirtd 는 직접 cgroupfs를 통해 cgroup의 /machine 계층에 QEMU를 등록합니다.
   중요한 점은 백엔드가 systemd든 cgroupfs든 관계없이,
   QEMU가 배치되는 cgroup(/machine)은
   kubelet의 자원 추적 범위인 kubepods 계층과 격리되어 있다는 것입니다.


QEMU 와 KVM 의 상호작용
========================

사전 개념 : CPU 동작 모드, 호스트 모드와 게스트 모드
-------------------------------------------------------------

게스트 OS 도 스스로를 진짜 OS 로 인식하므로 Ring 0 권한으로 동작해야 하지만,
호스트의 진짜 Ring 0 을 그대로 주면 격리가 파괴됩니다.
Intel VT-x / AMD-V 는 이를 위해 물리 CPU 에 두 가지 동작 모드를 둡니다.

* **호스트 모드 (VMX root)** — KVM 커널 모듈과 QEMU 가 CPU 제어권을 갖는
  모드. 하드웨어에 대한 완전한 접근 권한을 가집니다.
* **게스트 모드 (VMX non-root)** — 게스트가 CPU 제어권을 갖는 모드. 게스트
  모드 안에도 별도의 Ring 0 ~ Ring 3 체계가 있어, 게스트 커널은 게스트
  모드의 Ring 0 에서, 게스트 애플리케이션은 게스트 모드의 Ring 3 에서
  동작합니다.

vCPU의 동작 과정
-----------------

vCPU는 게스트 OS 가 물리 CPU 로 인식하는 가상 CPU 로,
실제로는 호스트의 물리 CPU 위에서 게스트 코드를 대신 실행하는 스레드입니다.

QEMU 는 vCPU 하나마다 호스트 스레드를 하나씩 만듭니다.
호스트 OS 에게 이 스레드는 다른 프로세스와 완전히 동일한 스케줄링 대상입니다.

vCPU 스레드는 아래 과정을 무한 루프로 반복합니다.

#. **VM-Entry** — vCPU 스레드가 ``ioctl(vcpu_fd, KVM_RUN)`` 시스템 콜을 호출하면
   KVM 커널 모듈이 물리 CPU 를 게스트 모드로 전환합니다.
#. **게스트 명령어 직접 실행** — 게스트 코드가 에뮬레이션 없이
   물리 하드웨어 속도로 실행됩니다.
#. **VM-Exit** — 게스트가 I/O 작업, 특정 제어 레지스터 접근 등
   가상화 경계를 넘는 동작을 시도하면 물리 CPU 가 실행을 중단하고
   호스트 모드로 복귀합니다.
#. **처리와 재진입** - KVM 안에서 처리 가능한 것은 KVM 이 처리하고 바로 VM-Entry 로 돌아가며,
   그렇지 않은 I/O 작업 등은 ``ioctl(KVM_RUN)`` 이 반환되어 QEMU 가 에뮬레이션한 뒤,
   루프의 처음으로 돌아가 KVM_RUN 을 다시 호출합니다.

.. note::

    호스트 타이머 인터럽트로 타임 슬라이스가 끝났을 때도 VM-Exit 가 발생합니다.
    이때는 호스트 스케줄러가 vCPU 스레드를 물리 CPU 에서 내리고 다른 프로세스를
    스케줄링합니다.

메모리의 동작 과정
-----------------------------

QEMU 는 호스트 메모리 공간에서 VM 크기만큼의 메모리를 ``mmap`` 으로 확보합니다.

게스트가 이 영역을 0 번지부터 시작하는 연속된 물리 메모리로 인식하도록 만들기 위해,
2단 주소 변환 체계를 사용합니다.
QEMU 는 "게스트 물리 주소(GPA) ↔ 호스트 가상(HVA) 주소" 대응표를
``KVM_SET_USER_MEMORY_REGION`` 명령을 통해 KVM 에 등록하고, KVM 은
이를 바탕으로 **EPT** (Extended Page Table)를 구성합니다.

* 게스트 페이지 테이블 : 게스트 가상 주소(GVA) → 게스트 물리 주소(GPA)
* EPT : 게스트 물리 주소(GPA) → 호스트 물리 주소(HPA)
* EPT 바이올레이션(Violation) : EPT는 초기에 비어있으며,
  게스트가 메모리에 접근할 때마다 EPT violation (VM-Exit)이 발생하여
  KVM 커널이 페이지 매핑을 동적으로 채웁니다.

기타 장치의 동작 과정
---------------------

* 게스트와 QEMU 가 공유하는 링 버퍼(Virtqueue)가 게스트 메모리 안에 있고, 게스트는 I/O 요청을
  그 큐에 쌓습니다.
  이 단계는 단순 메모리 쓰기이므로 VM-Exit 가 발생하지 않습니다.
* 요청을 모아 둔 후 게스트가 알림용 레지스터에 값을 쓰면 VM-Exit 가 발생합니다.
* KVM 커널이 해당 요청을 받고, I/O 완료 처리 등을 위해
  QEMU의 I/O 스레드로 제어권을 넘겨 처리합니다.
* 작업 완료 신호는 게스트에 가상 인터럽트(vIRQ) 형태로 전달됩니다.


격리는 어떻게 이루어지는가
---------------------------

VM 격리는 두 층위(하드웨어 및 호스트 OS)에서 동시에 작동합니다.

#. **하드웨어 수준의 격리** - 게스트 OS 가 허용되지 않은 메모리
   주소나 CPU 특권 레지스터를 건드리는 즉시 물리 CPU 가 명령 실행을 즉시 거부하고
   VM-Exit을 발생시켜 제어권을 KVM 으로 강제 환수합니다.
   KVM 과 QEMU 는 정상적인 I/O 요청만 처리하고, 허용되지 않은 접근은 게스트
   내부의 에러(Page Fault 등)로 되돌려 호스트를 보호합니다.

#. **호스트 OS 수준의 격리** - Kubernetes 컨테이너 환경 위에서도
   QEMU 프로세스는 호스트 OS 차원의 제한을 받습니다.
   sVirt, 마운트 네임스페이스, 시스템 콜 제한(Seccomp),
   자원 점유 제한(cgroup)을 겹겹이 적용하여 QEMU 프로세스 자체가 탈옥되더라도
   피해가 호스트 시스템이나 다른 Pod/VM으로 확산되지 않도록 합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 층위
     - 수단
     - 격리하는 대상
   * - 하드웨어
     - | VMX
       | non-root
     - 게스트의 특권 명령, 특수 레지스터 접근을 제한합니다. 경계를 넘으면
       CPU 가 VM-Exit 로 가로채 KVM 으로 제어권을 넘깁니다.
   * - 하드웨어
     - EPT (Extended Page Table)
     - 게스트 물리 주소 공간을 격리합니다. 게스트는 자신에게 매핑된 영역
       밖을 볼 수 없으며, 매핑 밖 접근은 EPT 바이올레이션으로
       처리됩니다.
   * - 호스트 OS
     - sVirt (SELinux MCS / AppArmor)
     - QEMU 프로세스의 파일 접근을 제한합니다. VM 마다 레이블이 달라
       다른 VM 의 디스크 이미지에 접근할 수 없습니다.
   * - 호스트 OS
     - Mount Namespace
     - QEMU 프로세스가 바라보는 ``/dev`` 를 호스트와 분리해 해당 VM 에
       필요한 장치 파일만 노출합니다.
   * - 호스트 OS
     - Seccomp
     - QEMU 프로세스가 호출할 수 있는 시스템 콜을 허용 목록으로 제한합니다.
   * - 호스트 OS
     - cgroup
     - CPU 시간 배분과 자원 사용량을 집계합니다. VM 마다 별도 cgroup 을
       가집니다.


QEMU와 KVM의 동작 확인해 보기
========================================

QEMU 와 KVM 의 연결 확인
---------------------------

QEMU 프로세스가 열고 있는 파일 디스크립터 중 KVM 관련 항목만 봅니다.

.. code-block:: console

   $ QPID=$(pgrep -f qemu-system-x86_64 | head -1)
   $ sudo ls -l /proc/$QPID/fd | grep kvm
   ... -> /dev/kvm
   ... -> anon_inode:kvm-vm
   ... -> anon_inode:kvm-vcpu:0
   ... -> anon_inode:kvm-vcpu-stats:0

* ``/dev/kvm`` — KVM 서브시스템 전체에 대한 제어. VM 생성 요청도 여기로
  들어가며, 커널은 그 결과로 VM 제어용 파일 디스크립터를 돌려줍니다.
* ``anon_inode:kvm-vm`` — 특정 VM 하나에 대한 제어기. 메모리 슬롯 등록도
  이 파일 디스크립터로 합니다.
* ``anon_inode:kvm-vcpu:0`` — vCPU 단위 제어. ``ioctl(KVM_RUN)`` 이 호출되는
  대상이며, vCPU 마다 파일 디스크립터가 따로 있습니다.

KVM을 통한 CPU 모드 전환 관찰
--------------------------------------------

커널 트레이서로 실제 VM-Entry/Exit 를 볼 수 있습니다.

.. code-block:: console

   $ sudo cat /sys/kernel/debug/tracing/trace | grep -v '^#' | head -20
   CPU 0/KVM-82557 [002] ... kvm_entry: vcpu 0, rip 0xffffffffae1b603b
   CPU 0/KVM-82557 [002] ... kvm_exit: vcpu 0 reason msr rip 0xffffffffad496104

``kvm_entry`` / ``kvm_exit`` 쌍이 게스트 모드 진입과 이탈이고, ``reason`` 필드가 이탈 사유입니다.
위 로그 중 ``msr`` 은 게스트가 MSR(Model Specific
Register)을 읽거나 쓰려 해서 발생한 VM-Exit 입니다.


참고
=====

* :ref:`nova-hypervisor-registration` — 노드가 하이퍼바이저로 등록되는 과정
* :doc:`../foundations/vm-vs-container` — VM 과 컨테이너의 격리 방식 비교
