===============================
가상화 기초: VM vs 컨테이너
===============================

가상 머신(Virtual Machine, VM)과 컨테이너는 하나의 물리 호스트에서
여러 워크로드를 실행할 수 있게 한다. 그러나 워크로드를 격리하는 위치와
관리 계층이 다르기 때문에 격리 수준, 시작 오버헤드, 자원 사용량 및
운영 방식에서 차이가 발생한다.


격리 수준의 차이
================

OpenStack Nova에서 일반적으로 사용하는 KVM 기반 VM은 하이퍼바이저를
경계로 호스트와 분리된다. 각 VM은 자체 게스트 커널을 실행하며,
가상 CPU, 메모리, 디스크 및 네트워크 장치를 할당받는다.

일반적인 Linux 컨테이너는 호스트 커널을 공유한다. 프로세스, 네트워크,
마운트 지점 등의 가시 범위는 Linux 네임스페이스(namespace)로 분리하고,
CPU와 메모리 같은 자원 사용량은 컨트롤 그룹(cgroup)으로 제한한다.

.. list-table:: VM과 컨테이너 비교
   :header-rows: 1
   :widths: 18 41 41

   * - 구분
     - VM(Nova/KVM)
     - 컨테이너(Kubernetes)
   * - 기본 격리 방식
     - KVM 하이퍼바이저와 하드웨어 가상화를 이용해 VM별 실행 환경을
       분리한다.
     - Linux 네임스페이스, cgroup, capabilities, seccomp 등의
       커널 기능으로 프로세스를 분리한다.
   * - 커널 사용 방식
     - VM마다 별도의 게스트 커널을 실행한다.
     - 같은 노드의 컨테이너가 호스트 커널을 공유한다.
   * - 주요 격리 경계
     - 게스트 운영체제와 하이퍼바이저 사이가 주요 경계이다.
     - 컨테이너 프로세스와 공유 호스트 커널 사이가 주요 경계이다.
   * - 일반적인 격리성
     - 게스트 커널이 호스트 커널과 분리되므로 비교적 강한 격리를
       제공한다.
     - VM보다 격리 경계가 얇다. 호스트 커널 취약점의 영향을 공유할
       가능성이 있다.
   * - 운영체제 선택
     - 호스트와 다른 종류 또는 버전의 게스트 운영체제를 실행할 수 있다.
     - 기본적으로 호스트 커널과 호환되는 사용자 공간이 필요하다.
   * - 시작 과정
     - 가상 하드웨어 초기화, 게스트 커널 부팅 및 시스템 서비스 시작이
       필요하다.
     - 기존 호스트 커널 위에 격리 환경을 구성하고 프로세스를 시작한다.
   * - 시작 오버헤드
     - 일반적으로 컨테이너보다 크다.
     - 일반적으로 VM보다 작다.
   * - 자원 오버헤드
     - 게스트 커널과 운영체제 구성 요소를 VM마다 포함하므로 상대적으로
       크다.
     - 호스트 커널을 공유하므로 상대적으로 작다.
   * - 주요 관리 단위
     - Nova 서버 또는 인스턴스
     - Kubernetes Pod
   * - 주요 관리 주체
     - ``nova-api``, ``nova-scheduler``, ``nova-compute``,
       libvirt 및 KVM
     - Kubernetes API 서버, 스케줄러, 컨트롤러, kubelet 및
       컨테이너 런타임
   * - 대표 사용 사례
     - 테넌트 간 강한 격리, 서로 다른 운영체제, 기존 VM 워크로드
     - 빠른 배포, 높은 배치 밀도, 마이크로서비스 및 선언적 운영

컨테이너가 반드시 안전하지 않다는 뜻은 아니다. 컨테이너에는
SELinux, AppArmor, seccomp, Linux capabilities, 사용자 네임스페이스,
읽기 전용 루트 파일시스템 등의 기능을 추가로 적용할 수 있다.

다만 VM과 일반 컨테이너의 가장 근본적인 차이는 **호스트 커널의 공유
여부**\ 이다. 일반 컨테이너의 애플리케이션은 호스트 커널의 시스템 호출
인터페이스를 사용하지만, VM에서는 별도의 게스트 커널과 하이퍼바이저가
추가 격리 경계를 형성한다.

.. note::

   시작 시간과 자원 오버헤드는 일반적인 경향이 그렇다는 것이다.
   실제로는 이미지 크기, 스토리지와 네트워크 구성, 초기화 작업,
   런타임 구현 및 하드웨어에 따라 값이 달라진다.


Data Plane vs Control Plane
===========================

OpenStack과 Kubernetes를 함께 구성할 때는 각 구성 요소가 어느 관리
영역에 속하는지 구분해야 한다.

이 문서에서 **Control Plane**\ 은 원하는 상태를 저장하고 워크로드의 배치와
생명주기를 결정하는 관리 영역을 의미한다. **Data Plane**\ 은 이러한 결정에
따라 실제 사용자 워크로드가 실행되고 트래픽이 처리되는 영역을 의미한다.

OpenStack Control Plane 서비스를 Kubernetes 위에 배포하더라도, Nova가
생성한 VM이 Kubernetes 워크로드로 바뀌는 것은 아니다. Kubernetes는
컨테이너로 실행되는 OpenStack API와 관리 서비스를 관리하고, Nova는
별도의 API와 스케줄링 체계를 통해 VM의 생명주기를 관리한다.


통합의 경계
-----------

OpenStack Control Plane을 Kubernetes 위에 배포하는 구성에서는 관리
경계가 다음과 같이 나뉜다.

* Kubernetes는 ``nova-api``, ``nova-scheduler``,
  ``neutron-server``, ``keystone`` 등 컨테이너로 실행되는
  OpenStack 서비스의 배치, 재시작 및 복구를 관리한다.
* Nova는 사용자가 요청한 VM의 스케줄링, 생성, 중지, 삭제 및 마이그레이션을
  관리한다.
* ``nova-compute``\ 는 Nova Control Plane의 요청을 받아 libvirt와 KVM을
  통해 Compute Node의 VM을 제어한다.
* VM은 Kubernetes Pod가 아니므로 Kubernetes 스케줄러나 Deployment
  컨트롤러가 직접 관리하지 않는다.
* OpenStack Control Plane Pod가 재시작되더라도 이미 실행 중인 VM이
  곧바로 삭제되는 것은 아니다.
* 반대로 Nova에서 VM을 삭제해도 Kubernetes는 이를 Pod 삭제로 처리하지
  않는다.

따라서 이 구조는 OpenStack 전체를 Kubernetes가 직접 관리하는 구조라기보다,
**OpenStack의 관리 서비스를 Kubernetes가 호스팅하고 OpenStack이 VM
워크로드를 관리하는 구조**\ 로 이해하는 것이 정확하다.


Control Plane과 Data Plane 경계
-------------------------------

다음 다이어그램은 관리 주체에 따른 논리적 경계를 나타낸다.

.. code-block:: text

   사용자 / 운영자
          |
          | OpenStack API 요청
          v
   +-----------------------------------------------------------+
   | Kubernetes 클러스터                                      |
   |                                                           |
   |  +---------------- Kubernetes Control Plane ------------+ |
   |  | kube-apiserver / scheduler / controllers             | |
   |  +---------------------------+---------------------------+ |
   |                              | Pod 배치·복구              |
   |                              v                            |
   |  +------------- OpenStack Control Plane Pods -----------+ |
   |  | Keystone | nova-api | nova-scheduler | Neutron ...   | |
   |  +---------------------------+---------------------------+ |
   +------------------------------|----------------------------+
                                  | VM 생성·삭제 및 호스트 선택
                                  v
   +-----------------------------------------------------------+
   | OpenStack Compute / Data Plane                            |
   |                                                           |
   |  nova-compute -> libvirt -> KVM/QEMU                      |
   |                              |                            |
   |                     +--------+--------+                   |
   |                     |                 |                   |
   |                   VM A              VM B                  |
   |             Guest Kernel      Guest Kernel                |
   |             + Workload        + Workload                  |
   +-----------------------------------------------------------+

위 다이어그램에서 Kubernetes의 직접적인 관리 대상은 OpenStack 서비스가
실행되는 Pod까지이다. VM은 Kubernetes 바깥의 별도 워크로드이며 Nova와
하이퍼바이저가 관리한다.

여기서 "Kubernetes 밖"은 반드시 물리적으로 다른 서버에 있다는 뜻이 아니다.
Kubernetes 노드와 OpenStack Compute Node가 같은 물리 인프라를 공유하거나,
일부 구성 요소가 같은 호스트에서 실행될 수도 있다. 핵심은 물리적 위치가
아니라 **어떤 API와 컨트롤러가 해당 자원의 생명주기를 소유하는가**\ 이다.


VM 생성 요청의 흐름
-------------------

VM 생성 요청은 일반적으로 다음과 같이 처리된다.

#. 사용자가 Nova API에 VM 생성을 요청한다.
#. ``nova-scheduler``\ 가 VM을 실행할 Compute Node를 선택한다.
#. 선택된 노드의 ``nova-compute``\ 가 요청을 받는다.
#. ``nova-compute``\ 가 libvirt를 통해 KVM/QEMU에 VM 생성을 요청한다.
#. KVM/QEMU가 게스트 커널과 사용자 워크로드를 실행한다.

OpenStack Control Plane이 Kubernetes Pod로 실행되는 경우에도 VM 배치를
결정하는 주체는 Nova이다. Kubernetes 스케줄러는 ``nova-api``나
``nova-scheduler`` Pod가 실행될 노드를 결정하지만, Nova VM이 실행될
Compute Node를 선택하지는 않는다.


컨테이너 격리 강화와 VM의 절충점
---------------------------------

일반 컨테이너는 가볍고 빠르지만 호스트 커널을 공유한다. 반대로 VM은
강한 격리 경계를 제공하지만 별도의 게스트 커널을 실행하므로 더 많은
자원과 시작 시간이 필요하다.

gVisor와 Kata Containers 같은 샌드박스 런타임은 두 방식 사이에서
추가적인 선택지를 제공한다.

.. list-table:: 격리 방식별 특성
   :header-rows: 1
   :widths: 18 28 28 26

   * - 방식
     - 격리 구조
     - 장점
     - 고려 사항
   * - 일반 컨테이너
     - 호스트 Linux 커널을 직접 공유한다.
     - 오버헤드가 작고 시작이 빠르며 호환성이 높다.
     - 호스트 커널이 주요 보안 경계가 된다.
   * - gVisor
     - 사용자 공간 애플리케이션 커널이 시스템 호출을 가로채 처리한다.
     - 워크로드가 호스트 커널에 직접 노출되는 범위를 줄인다.
     - 일부 Linux 기능과의 호환성 또는 입출력 성능에 영향이 있을 수 있다.
   * - Kata Containers
     - Pod 또는 컨테이너를 경량 VM 내부에서 실행한다.
     - 컨테이너 운영 방식을 유지하면서 하드웨어 가상화 기반 격리를
       제공한다.
     - 일반 컨테이너보다 시작 시간과 메모리 오버헤드가 크며 가상화
       지원이 필요하다.
   * - 일반 VM
     - 완전한 게스트 운영체제와 커널을 하이퍼바이저 위에서 실행한다.
     - 강한 격리와 높은 운영체제 호환성을 제공한다.
     - 부팅, 메모리 및 스토리지 오버헤드가 가장 크다.


gVisor
~~~~~~

gVisor는 일반적인 하이퍼바이저가 아니라 사용자 공간에서 동작하는
애플리케이션 커널을 제공한다. 샌드박스 안의 애플리케이션이 시스템 호출을
실행하면 gVisor가 이를 가로채 처리한다.

일반 컨테이너에서는 애플리케이션의 시스템 호출이 호스트 Linux 커널에
직접 도달한다. gVisor는 Linux와 유사한 시스템 인터페이스의 상당 부분을
사용자 공간에서 구현하여 호스트 커널에 직접 도달하는 경로를 줄인다.

다만 모든 Linux 커널 기능이 동일하게 지원되는 것은 아니다. 특정 시스템
호출이나 커널 기능에 의존하는 애플리케이션에서는 호환성 검증이 필요하며,
시스템 호출 또는 파일·네트워크 입출력이 많은 워크로드에서는 성능
오버헤드가 발생할 수 있다.


Kata Containers
~~~~~~~~~~~~~~~

Kata Containers는 컨테이너 관리 인터페이스를 유지하면서 실제 워크로드를
경량 VM 내부에서 실행한다. 각 샌드박스가 별도의 게스트 커널을 사용하므로
일반 컨테이너보다 강한 커널 격리 경계를 제공한다.

다음과 같은 환경에서 Kata Containers를 고려할 수 있다.

* 서로 신뢰할 수 없는 여러 테넌트의 워크로드를 같은 클러스터에서
  실행하는 경우
* 임의의 사용자 코드나 플러그인을 실행하는 경우
* Kubernetes의 Pod 운영 방식을 유지하면서 게스트 커널 단위의 격리가
  필요한 경우
* 보안 정책상 공유 커널 컨테이너보다 강한 경계가 필요한 경우

경량 VM과 게스트 커널이 추가되므로 일반 컨테이너보다 시작 시간과 메모리
사용량이 증가할 수 있다. 하드웨어 가상화 및 중첩 가상화 지원 여부도
인프라 설계 시 확인해야 한다.


Kubernetes에서 런타임 선택
~~~~~~~~~~~~~~~~~~~~~~~~~~

Kubernetes에서는 ``RuntimeClass``\ 를 사용하여 Pod별로 컨테이너 런타임
구성을 선택할 수 있다. 일반 OCI 런타임을 기본값으로 사용하면서 격리가
더 필요한 워크로드에만 gVisor 또는 Kata Containers 기반 런타임을
지정할 수 있다.

.. code-block:: yaml

   apiVersion: node.k8s.io/v1
   kind: RuntimeClass
   metadata:
     name: kata
   handler: kata
   ---
   apiVersion: v1
   kind: Pod
   metadata:
     name: sandboxed-workload
   spec:
     runtimeClassName: kata
     containers:
       - name: app
         image: example/app:1.0

``handler`` 값은 각 노드의 컨테이너 런타임에 설정된 런타임 핸들러와
일치해야 한다. ``RuntimeClass`` 리소스를 생성하는 것만으로 gVisor나
Kata Containers가 설치되는 것은 아니다. 해당 런타임을 노드에 설치하고
containerd 또는 CRI-O와 연동해야 한다.


격리 방식 선택 기준
~~~~~~~~~~~~~~~~~~~

격리 기술은 워크로드의 신뢰 수준, 성능 요구사항 및 운영 복잡도를 함께
고려하여 선택한다.

* 신뢰할 수 있는 일반 애플리케이션에는 표준 컨테이너가 적합할 수 있다.
* 신뢰 수준이 낮은 코드에는 gVisor 같은 샌드박스 런타임을 고려할 수 있다.
* Kubernetes 운영 방식을 유지하면서 커널 단위 격리가 필요하다면
  Kata Containers를 고려할 수 있다.
* 서로 다른 운영체제, 완전한 게스트 환경 또는 명확한 VM 경계가 필요하다면
  Nova/KVM 기반 VM이 적합하다.

gVisor와 Kata Containers는 VM 격리를 완전히 대체하기보다는 컨테이너의
운영 편의성과 VM에 가까운 격리 특성 사이에서 선택할 수 있는 절충안이다.


더 읽을거리
===========

* `OpenStack Nova 시스템 아키텍처
  <https://docs.openstack.org/nova/latest/admin/architecture.html>`_
* `OpenStack Nova Compute Node 설치와 KVM
  <https://docs.openstack.org/nova/latest/install/compute-install-ubuntu.html>`_
* `Kubernetes Pod
  <https://kubernetes.io/ko/docs/concepts/workloads/pods/>`_
* `Kubernetes cgroup v2
  <https://kubernetes.io/ko/docs/concepts/architecture/cgroups/>`_
* `Kubernetes Linux 커널 보안 제약
  <https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/>`_
* `Kubernetes RuntimeClass
  <https://kubernetes.io/ko/docs/concepts/containers/runtime-class/>`_
* `gVisor 개요
  <https://gvisor.dev/docs/>`_
* `Kata Containers
  <https://katacontainers.io/>`_
