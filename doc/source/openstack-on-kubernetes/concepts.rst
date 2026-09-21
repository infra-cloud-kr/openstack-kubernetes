==============================
핵심 개념 (OpenStack on K8s)
==============================

OpenStack 을 Kubernetes 위에서 운영하기 전에 잡아 두면 좋은 핵심 개념을
모았습니다.

.. note::

   기여자 작업용 골격입니다. 각 절을 실습 경험과 공식 문서를 바탕으로
   보강해 주세요.


왜 OpenStack 을 컨테이너로 운영하는가
=====================================

* 선언적 배포와 반복 가능한 업그레이드
* 컨트롤 플레인 구성요소의 격리와 스케일링
* Kubernetes 의 자가 치유(self-healing) 및 롤아웃/롤백 활용
* GitOps 와 결합한 Day-2 운영 자동화


구성요소 매핑
=============

OpenStack 의 주요 서비스가 Kubernetes 리소스로 어떻게 매핑되는지 정리합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - OpenStack 서비스
     - Kubernetes 상의 형태 (예)
   * - Keystone (인증)
     - Deployment + Service, 외부 노출용 Ingress
   * - Nova (compute)
     - 컨트롤 컴포넌트는 Pod, 하이퍼바이저 노드는 별도 관리
   * - Neutron (network)
     - Deployment/DaemonSet 조합
   * - Glance (image)
     - Deployment + 오브젝트 스토리지 백엔드
   * - 데이터베이스 / 메시지 큐
     - Operator 또는 StatefulSet (MariaDB, RabbitMQ 등)


컨트롤 플레인과 데이터 플레인 경계
==================================

OpenStack 을 Kubernetes 위에 배포할 때는 각 구성 요소가 어느 관리 영역에
속하는지 구분해야 한다.

여기서 **컨트롤 플레인(Control Plane)**\ 은 원하는 상태를 저장하고
워크로드의 배치와 생명주기를 결정하는 관리 영역을 의미한다.
**데이터 플레인(Data Plane)**\ 은 이러한 결정에 따라 실제 사용자
워크로드가 실행되고 트래픽이 처리되는 영역을 의미한다.

OpenStack 컨트롤 플레인 서비스를 Kubernetes 위에 배포하더라도, Nova 가
생성한 VM 이 Kubernetes 워크로드로 바뀌는 것은 아니다. Kubernetes 는
컨테이너로 실행되는 OpenStack API 와 관리 서비스를 관리하고, Nova 는
별도의 API 와 스케줄링 체계를 통해 VM 의 생명주기를 관리한다.


관리 경계
---------

OpenStack 컨트롤 플레인을 Kubernetes 위에 배포하는 구성에서는 관리 경계가
다음과 같이 나뉜다.

* Kubernetes 는 ``nova-api``, ``nova-scheduler``, ``neutron-server``,
  ``keystone`` 등 컨테이너로 실행되는 OpenStack 서비스의 배치, 재시작 및
  복구를 관리한다.
* Nova 는 사용자가 요청한 VM 의 스케줄링, 생성, 중지, 삭제 및
  마이그레이션을 관리한다.
* ``nova-compute``\ 는 Nova 컨트롤 플레인의 요청을 받아 libvirt 와 KVM 을
  통해 Compute Node 의 VM 을 제어한다.
* VM 은 Kubernetes Pod 가 아니므로 Kubernetes 스케줄러나 Deployment
  컨트롤러가 직접 관리하지 않는다.
* OpenStack 컨트롤 플레인 Pod 가 재시작되더라도 이미 실행 중인 VM 이
  곧바로 삭제되는 것은 아니다.
* 반대로 Nova 에서 VM 을 삭제해도 Kubernetes 는 이를 Pod 삭제로 처리하지
  않는다.

따라서 이 구조는 OpenStack 전체를 Kubernetes 가 직접 관리하는 구조라기보다,
**OpenStack 의 관리 서비스를 Kubernetes 가 호스팅하고 OpenStack 이 VM
워크로드를 관리하는 구조**\ 로 이해하는 것이 정확하다.


논리적 경계
-----------

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
   |  +---------------------------+--------------------------+ |
   |                              | Pod 배치·복구              |
   |                              v                            |
   |  +------------- OpenStack Control Plane Pods -----------+ |
   |  | Keystone | nova-api | nova-scheduler | Neutron ...   | |
   |  +---------------------------+--------------------------+ |
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

위 다이어그램에서 Kubernetes 의 직접적인 관리 대상은 OpenStack 서비스가
실행되는 Pod 까지이다. VM 은 Kubernetes 바깥의 별도 워크로드이며 Nova 와
하이퍼바이저가 관리한다.

여기서 "Kubernetes 밖"은 반드시 물리적으로 다른 서버에 있다는 뜻이 아니다.
Kubernetes 노드와 OpenStack Compute Node 가 같은 물리 인프라를 공유하거나,
일부 구성 요소가 같은 호스트에서 실행될 수도 있다. 핵심은 물리적 위치가
아니라 **어떤 API 와 컨트롤러가 해당 자원의 생명주기를 소유하는가**\ 이다.


VM 생성 요청의 흐름
-------------------

VM 생성 요청은 일반적으로 다음과 같이 처리된다.

#. 사용자가 Nova API 에 VM 생성을 요청한다.
#. ``nova-scheduler``\ 가 VM 을 실행할 Compute Node 를 선택한다.
#. 선택된 노드의 ``nova-compute``\ 가 요청을 받는다.
#. ``nova-compute``\ 가 libvirt 를 통해 KVM/QEMU 에 VM 생성을 요청한다.
#. KVM/QEMU 가 게스트 커널과 사용자 워크로드를 실행한다.

OpenStack 컨트롤 플레인이 Kubernetes Pod 로 실행되는 경우에도 VM 배치를
결정하는 주체는 Nova 이다. Kubernetes 스케줄러는 ``nova-api`` 나
``nova-scheduler`` Pod 가 실행될 노드를 결정하지만, Nova VM 이 실행될
Compute Node 를 선택하지는 않는다.


배포 방식 비교
==============

컨테이너화된 OpenStack 을 올리는 배포 방식은 크게 둘입니다.

* :doc:`openstack-helm` — Helm chart 기반, Kubernetes 위 배포
* Kolla-Ansible — Ansible + Docker 기반(Kubernetes 아님)

두 방식의 상세 비교와 선택 기준은 :doc:`comparison` 에서 다룹니다. 두 방식이
공통으로 사용하는 컨테이너 이미지 레이어는 :doc:`kolla` 를 참고하세요.
