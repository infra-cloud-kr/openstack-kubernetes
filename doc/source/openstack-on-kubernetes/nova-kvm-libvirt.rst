.. _nova-libvirt-kvm:

===============================================
Nova 의 VM 생성과 자원 격리 (libvirt / KVM)
===============================================

Nova 가 인스턴스 생성 요청을 받아 호스트 위에 실제 QEMU 프로세스를 띄우기까지의
과정을 OS 관점 — 프로세스, cgroup, 하드웨어 가상화 — 에서 정리합니다.

앞의 두 절은 베어메탈 OpenStack 을 기준으로 한 전체 흐름이고,
:ref:`nova-on-k8s-diff` 는 OpenStack on Kubernetes(openstack-helm) 에서
달라지는 지점만 다룹니다.

.. note::

   이 문서는 "nova가 생성한 VM의 생성과 동작" 에 초점을 둡니다.
   하이퍼바이저 등록, 셀 매핑은 :ref:`nova-hypervisor-registration`,
   네트워크 포트가 실제로 붙는 과정은 Neutron 쪽 문서를 참고하세요.

   nova-compute가 VM을 생성하기 위한 Glance, Cinder, Neutron 호출 과정은
   이 문서에서 자세히 다루지 않습니다.


Nova 에서 VM 이 만들어지기까지
===============================

요청 경로: nova-api 에서 nova-compute 까지
--------------------------------------------

#. **nova-api** — Keystone 으로 토큰을 검증하고, 쿼터를 확인한 뒤 인스턴스
   레코드를 만듭니다. 요청은 nova-conductor 를 거쳐 스케줄러로 전달됩니다.
#. **nova-scheduler + Placement** — 스케줄러는 Placement 에게
   vCPU/RAM/디스크 등 조건을 만족하는 컴퓨트 노드를 물어 후보
   목록을 받고, 그중 필터와 가중치를 적용해 최종 호스트를 고릅니다. 선택이
   끝나면 해당 자원을 이 인스턴스가 쓴다고 Placement 에 기록(claim)합니다.
#. **nova-compute** — 다시 conductor 를 거쳐 선택된 호스트의 nova-compute 로
   요청이 전달됩니다. nova-compute 는 glance에서 이미지를 받아오고,
   neutron에 네트워크 포트를, cinder에 볼륨을 요청해 VM을 구성합니다.
#. **libvirt 드라이버** — 모인 정보로 도메인 XML 을 만들어 libvirtd 에
   넘깁니다. 최종적으로 QEMU/KVM 프로세스가 기동되면서 VM 이 생성됩니다.


도메인 XML — VM 의 설계도
----------------------------

nova-compute 가 만든 도메인 XML 에는 vCPU 수, 메모리 크기, CPU 모드,
디스크(가상 디스크 파일 경로와 버스), 네트워크 인터페이스 등이 담깁니다.
libvirtd 는 이 XML 을 해석해 QEMU 명령줄로 옮기고, 격리 설정을 함께
구성합니다.

libvirtd 가 QEMU 프로세스를 생성하는 과정
------------------------------------------

libvirtd 는 fork 와 exec 로 QEMU 프로세스를 만들며, 그 과정에서
cgroup 배치,
VM 간 이미지 접근을 차단하는 디스크 라벨링(sVirt),
QEMU 프로세스의 /dev 를 호스트와 분리해
해당 VM 에 필요한 장치 파일만 노출하는 마운트 네임스페이스(Mount Namespace)를 수행하여
QEMU의 권한을 root 에서 ``libvirt-qemu`` 로 제한합니다.

이 시점에서 호스트에는 cgroup 과 보안 레이블이 걸린 QEMU
프로세스 하나가 보이고, VM 안에서는 가상 CPU/메모리/디스크가 생기며
커널 로딩이 시작됩니다.

QEMU 와 KVM 의 상호작용
========================

사전 개념 : CPU 동작 모드, 호스트 모드와 게스트 모드
-------------------------------------------------------------

게스트 OS 도 스스로를 진짜 OS 로 인식하므로 Ring 0 권한으로 동작해야 하지만,
호스트의 진짜 Ring 0 을 그대로 주면 격리가 깨집니다. Intel VT-x / AMD-V 는
이를 위해 물리 CPU 에 두 가지 동작 모드를 둡니다.

* **호스트 모드 (VMX root)** — KVM 커널 모듈과 QEMU 가 CPU 제어권을 갖는
  모드. 하드웨어에 대한 완전한 접근 권한을 가집니다.
* **게스트 모드 (VMX non-root)** — 게스트가 CPU 제어권을 갖는 모드. 게스트
  모드 안에도 별도의 Ring 0 ~ Ring 3 체계가 있어, 게스트 커널은 게스트
  모드의 Ring 0 에서, 게스트 애플리케이션은 게스트 모드의 Ring 3 에서
  동작합니다.

vCPU의 동작 과정
-----------------

vCPU는 게스트 OS 가 물리 CPU 로 인식하는 가상 CPU 로,
실제로는 호스트의 스레드가 물리 CPU 위에서 게스트 코드를 대신 실행하는 추상화 단위입니다.

QEMU 는 vCPU 하나마다 호스트 스레드를 하나씩 만듭니다. 호스트 OS 에게 이
스레드는 다른 프로세스와 완전히 동일한 스케줄링 대상입니다.

vCPU 스레드는 아래 과정을 무한 루프로 반복합니다.

#. **VM-Entry** — vCPU 스레드가 ``ioctl(vcpu_fd, KVM_RUN)`` 을 호출하면
   KVM 이 물리 CPU 를 게스트 모드로 전환합니다.
#. **게스트 명령어 직접 실행** — 게스트 코드가 번역이나 에뮬레이션 없이
   하드웨어 속도로 실행됩니다.
#. **VM-Exit** — 게스트가 I/O 접근, 특정 제어 레지스터 접근 등
   가상화 경계를 넘는 동작을 시도하면 물리 CPU 가 실행을 중단하고 호스트
   모드로 복귀합니다. KVM 안에서 처리 가능한 것은 KVM 이 처리하고 바로
   VM-Entry 로 돌아가며, 그렇지 않으면 ``KVM_RUN`` 이 반환되어 QEMU 가
   처리합니다.(유저 공간 QEMU 로 복귀)
#. **에뮬레이션 후 재진입** — QEMU 는 ``exit_reason`` 을 보고 요청을
   소프트웨어로 처리한 뒤, 루프 처음으로 돌아가 다시 ``KVM_RUN`` 을
   호출합니다.

.. note::

    호스트 타이머 인터럽트로 타임 슬라이스가 끝났을 때도 VM-Exit 가 발생합니다.
    이때는 호스트 스케줄러가 vCPU 스레드를 물리 CPU 에서 내리고 다른 프로세스를
    올립니다.

메모리의 동작 과정
-----------------------------

QEMU 는 먼저 호스트에서 VM 크기만큼의 메모리를 ``mmap`` 으로 확보합니다.
호스트 입장에서는 그냥 QEMU 프로세스의 익명 메모리입니다.

게스트가 이 영역을 0 번지부터 시작하는 연속된 물리 메모리로 보게 하려면
주소 변환이 한 단계 더 필요합니다. QEMU 는 "게스트 물리 주소 ↔ 호스트 가상
주소" 대응표를 ``KVM_SET_USER_MEMORY_REGION`` 으로 KVM 에 등록하고, KVM 은
이를 바탕으로 **EPT** (Extended Page Table)를 구성합니다.

* 게스트 안에서는 게스트 페이지 테이블이 게스트 가상 주소 → 게스트 물리
  주소를, EPT 가 다시 게스트 물리 주소 → 호스트 물리 주소를 담당하는
  **2단 변환** 이 하드웨어에서 이뤄집니다.(CPU 내 MMU가 담당)
* EPT 는 미리 전부 채워지지 않고, 접근이 일어날 때마다 EPT violation
  (VM-Exit)이 발생해 KVM 이 그때그때 매핑을 채웁니다.
* 매핑이 없거나 쓰기 금지된 주소에 대한 접근은 VM-Exit 로 처리되며, MMIO
  (Memory-mapped I/O)처리도 이 경로를 씁니다.

기타 장치의 동작 과정
---------------------

* 게스트와 QEMU 가 공유하는 큐가 게스트 메모리 안에 있고, 게스트는 요청을
  그 큐에 쌓습니다. 여기까지는 단순 메모리 쓰기라 VM-Exit 가 없습니다.
* 요청을 모아 둔 뒤 게스트가 알림용 레지스터에 값을 쓰면 VM-Exit 가 발생합니다.
* 이 exit이 발생하고 나면 KVM 이 커널에서 처리할 수 있으면 처리 후 vCPU 를 즉시 게스트 모드로
  복귀시키며, 그렇지 못한 경우, 실제 I/O 의 경우에는 QEMU 의 I/O 스레드가 처리합니다.
* 완료된 작업은 게스트에 인터럽트로 전달됩니다.


격리는 어떻게 이루어지는가
---------------------------

VM 격리는 두 층위에서 동시에 작동합니다.

첫 번째는 **하드웨어 수준의 격리** 입니다. 게스트 OS 가 허용되지 않은 메모리
주소나 CPU 특권 레지스터를 건드리는 순간, CPU 가 명령 실행을 즉시 거부하고
VM-Exit(하드웨어 트랩)를 발생시켜 제어권을 KVM 으로 강제 복귀시킵니다.
KVM 과 QEMU 는 정상적인 I/O 요청만 처리하고, 허용되지 않은 접근은 게스트
내부의 에러(Page Fault 등)로 되돌려 호스트를 보호합니다.

두 번째는 **호스트 OS 수준의 격리** 입니다. QEMU 프로세스 자체에도 파일 접근
제한(sVirt), 마운트 네임스페이스, 시스템 콜 제한(Seccomp),
자원 점유 제한(cgroup)을 겹쳐 걸어 둡니다. QEMU 프로세스가 침해되더라도
피해가 호스트 전체로 번지지 않도록 합니다.

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
       밖을 볼 수 없으며, 매핑 밖 접근은 EPT violation(VM-Exit)으로
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

.. note::

   베어메탈 OpenStack 에서 QEMU 는 Mount Namespace 만 부분적으로 사용하며,
   PID, Network 등 다른 네임스페이스는 쓰지 않습니다.
   K8s 환경에서 달라지는 점은 :ref:`nova-on-k8s-diff` 를 참고하세요.


.. _nova-on-k8s-diff:

OpenStack on Kubernetes 로의 흐름
=========================================

**도메인 XML 이후의 흐름 — libvirtd 의 fork/exec, QEMU 와 KVM 의 상호작용,
vCPU 루프, EPT — 은 앞 절과 완전히 동일합니다.**

관련 프로세스가 Pod로 동작하면서 생기는 차이점을 위주로 다룹니다.

nova-compute 와 libvirt 가 서로 다른 Pod
-------------------------------------------

openstack-helm 은 nova-compute 와 libvirt 를 각각 별도의 DaemonSet Pod 로
띄웁니다. 그럼에도 nova-compute 는 libvirtd 에 도메인 XML 을 넘겨야 합니다.

두 Pod 는 같은 호스트 디렉터리를 공유 마운트하고, 그 위의 UNIX 소켓으로
libvirt RPC 를 주고받는 방식으로 이를 해결합니다.

libvirt Pod 의 권한과 호스트 접근
------------------------------------

컨테이너는 기본적으로 호스트 커널, 하드웨어 접근이 제한(unprivileged)되어
있습니다. 그러나 libvirt 는 QEMU 를 위해 호스트 커널, 하드웨어에 접근해야합니다.

그래서 libvirt Pod 는

* ``privileged: true`` 로 기동해 커널과 하드웨어에 접근하고,
* 호스트의 실제 디렉터리(인스턴스 경로, ``/var/lib/libvirt``, ``/dev`` 등)를
  직접 마운트해 읽고 씁니다.

libvirt Pod에서 libvirtd까지
---------------------------------------------------------------

Pod 는 기본적으로 kubelet 이 관리하는 cgroup 계층(``kubepods`` 아래)에
놓입니다. libvirtd 가 이 안에 있으면, 그 자식으로 생기는 QEMU 도 Pod 의
리소스 상한을 그대로 상속받게 되어 VM 자원 할당에 제약이 생깁니다.

openstack-helm 의 libvirt 차트는 앞에서 얻은 호스트 권한을 사용해 이
계층을 벗어납니다.

.. code-block:: console

   + cgcreate -g cpu,hugetlb,memory,rdma,misc,pids:/osh-libvirt
   + cgexec -g cpu,hugetlb,memory,rdma,misc,pids:/osh-libvirt \
       systemd-run --scope --slice=system libvirtd --listen
   Running as unit: run-r0cc5ced77b7e40db9c8767d441d96e79.scope

#. ``cgcreate`` 로 cgroup 루트 아래에 ``/osh-libvirt`` 를 직접 만듭니다.
#. ``cgexec`` 로 그 cgroup 으로 이동해 kubelet 이 만든 계층을 벗어난 뒤,
   ``systemd-run --scope --slice=system`` 으로 libvirtd 를 호스트 systemd 의
   ``system.slice`` 아래 새 scope 에 등록합니다.
#. 컨테이너의 최초 프로세스는 ``systemd-run`` 으로 남아 libvirtd 를
   감시합니다. libvirtd 가 죽으면 함께 종료되고, Kubernetes 가 Pod 를 다시
   띄웁니다.

결과적으로 libvirtd 는 베어메탈에서와 동일하게 ``system.slice`` 에 속한
프로세스가 되면서도, 수명 주기는 Kubernetes 의 선언적 관리 아래 남습니다.

.. code-block:: console

   # libvirtd PID로 cgroup 경로를 확인합니다.
   $ cat /proc/<libvirtd PID>/cgroup
   0::/system.slice/run-rd2beada6c25e4baf90db578cc514c194.scope

libvirtd에서 QEMU까지
------------------------------------------------

Openstack on Kubernetes에서 libvirtd 가 QEMU 를 생성할 때는 베어메탈과 다른 점과 같은 점이 있습니다.

* **부모 프로세스가 libvirtd 가 아니다.** libvirtd 는 QEMU 를 double fork해서 띄웁니다.
  목적은 **libvirtd 가 재시작, 크래시해도 실행
  중인 VM 이 함께 죽지 않게** 하는 것입니다. double fork 과정에서 중간 프로세스가
  종료되면서 QEMU 는 고아 프로세스가 되고, 가장 가까운 서브리퍼(subreaper)가 새로운 부모 프로세스가 됩니다.
  libvirt Pod 안에서 그 서브리퍼가 ``containerd-shim`` 로 관측됩니다.
  이는 베어메탈과는 다르게 적용되는 점입니다.( 베어메탈에서는 systemd 가 QEMU 의 부모 프로세스입니다.)

* **cgroup 이 libvirtd 와 다르다.** libvirtd 는 ``system.slice`` 에 있지만
  QEMU 는 가상화 전용 구역인 machine 계층으로 옮겨집니다.
  ``system.slice`` 에는 sshd, journald 등 OS 운용에 필수적인 서비스가 함께
  있어, VM 이 자원을 폭주시켰을 때 이들이 함께 영향을 받는 것을 피하기
  위함입니다. 이는 베어메탈 libvirt 도 동일하게 적용하는 점 입니다.

.. code-block:: console

   # QEMU PID 를 조회해 부모 PID 를 확인합니다.
   $ ps -o pid,ppid,comm -p <QEMU PID>
       PID    PPID COMMAND
     82518   40593 qemu-system-x86

   # QEMU 의 부모 PID(40593)로 부모 프로세스를 조회합니다.
   $ ps -o pid,ppid,comm,args -p 40593
       PID    PPID COMMAND         COMMAND
     40593       1 containerd-shim /usr/bin/containerd-shim-runc-v2 ...

   # QEMU 의 cgroup 경로를 확인합니다.
   $ cat /proc/<QEMU PID>/cgroup
   0::/machine/qemu-1-instance-00000001.libvirt-qemu/emulator

.. note::

   위 경로는 ``machine.slice`` 가 아니라 cgroup 루트 바로 아래의
   ``machine`` 계층입니다(``0::`` 접두사에서 보듯 cgroup v2 단일 계층).
   libvirt 가 systemd cgroup 백엔드 대신 자체 cgroupfs 백엔드로 동작할 때
   나타나는 형태로, 역할(가상화 전용 구역)은 같지만 systemd 가 관리하는
   scope 는 아닙니다. systemd 백엔드였다면
   ``/machine.slice/machine-qemu\x2d1\x2d....scope`` 로 보입니다.

여기까지의 과정을 통해 QEMU 프로세스는 권한, cgroup, 부모 관계 모두 베어메탈에서 뜬
QEMU 와 사실상 동일한 상태가 됩니다. 이후 KVM 과의 상호작용은 앞 절에서
설명한 것과 완전히 같습니다.


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
  들어가며, 커널은 그 결과로 VM 제어용 fd 를 돌려줍니다.
* ``anon_inode:kvm-vm`` — 그 VM 하나에 대한 제어기. 메모리 슬롯 등록도
  이 fd 로 합니다.
* ``anon_inode:kvm-vcpu:0`` — vCPU 단위 제어. ``ioctl(KVM_RUN)`` 이 호출되는
  대상이며, vCPU 마다 fd 가 따로 있습니다.

KVM을 통한 CPU 모드 전환 관찰
--------------------------------------------

커널 트레이서로 실제 VM-Entry/Exit 를 볼 수 있습니다.

.. code-block:: console

   $ sudo cat /sys/kernel/debug/tracing/trace | grep -v '^#' | head -20
   CPU 0/KVM-82557 [002] ... kvm_entry: vcpu 0, rip 0xffffffffae1b603b
   CPU 0/KVM-82557 [002] ... kvm_exit: vcpu 0 reason msr rip 0xffffffffad496104

``kvm_entry`` / ``kvm_exit`` 쌍이 게스트 모드 진입과 이탈이고, ``reason``
필드가 이탈 사유입니다. 위 예의 ``msr`` 은 게스트가 MSR(Model Specific
Register)을 읽거나 쓰려 해서 발생한 VM-Exit 입니다.


참고
=====

* :ref:`nova-hypervisor-registration` — 노드가 하이퍼바이저로 등록되는 과정
* :doc:`../foundations/vm-vs-container` — VM 과 컨테이너의 격리 방식 비교
