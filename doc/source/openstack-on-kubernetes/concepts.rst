===================================
핵심 개념 (OpenStack on Kubernetes)
===================================

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
     - 컨트롤 컴포넌트는 Pod, 하이퍼바이저 노드는 별도 관리.
       :ref:`nova-hypervisor-registration` 에서 자세히 다룹니다.
   * - Neutron (network)
     - Deployment/DaemonSet 조합
   * - Glance (image)
     - Deployment + 오브젝트 스토리지 백엔드
   * - 데이터베이스 / 메시지 큐
     - Operator 또는 StatefulSet (MariaDB, RabbitMQ 등)


.. _nova-hypervisor-registration:

Kubernetes 노드의 Nova 하이퍼바이저 등록
========================================

:term:`Nova` 가 VM 을 배치하려면 각 노드가 하이퍼바이저(hypervisor)로
먼저 등록되어 있어야 합니다.
OpenStack on Kubernetes 에서 이 하이퍼바이저는 별도의 물리 서버가 아니라
nova-compute 가 실행되는 Kubernetes 노드 자신입니다.

* Kubernetes 노드 1대 = Nova 하이퍼바이저 1대 (nova-compute Pod 가 노드마다 하나)
* 전체 흐름: nova-compute 기동 → 서비스 레코드 → 컴퓨트 노드 레코드
  → 셀(cell) 매핑 → 스케줄러의 배치 후보

등록 과정
---------

nova-compute 가 기동하면서 수행하는 일:

#. 하이퍼바이저 드라이버(libvirt)에서 CPU/메모리/디스크 자원 정보 수집
#. 서비스(service) 레코드 등록 — "이 호스트의 nova-compute 가 살아 있다"
   는 생존 신고, 이후 주기적인 하트비트로 갱신
#. 컴퓨트 노드(compute node) 레코드 생성 — 하이퍼바이저의 자원 현황표,
   스케줄러가 VM 배치를 결정할 때 참조

등록 이름은 노드의 호스트명(hostname)에서 옵니다 — nova-compute Pod 는
호스트 네트워크를 사용하므로 Pod 호스트명이 곧 Kubernetes 노드
호스트명이고, 그 이름이 하이퍼바이저 이름으로 그대로 등록됩니다.

등록 확인
---------

.. code-block:: console

   $ openstack compute service list --service nova-compute
   $ openstack hypervisor list

* 첫 번째 명령 — 호스트별 nova-compute 서비스 상태. State 가 up 이면
  생존 신고(하트비트) 정상
* 두 번째 명령 — Hypervisor Hostname 열에 Kubernetes 노드의 호스트명이
  그대로 표시

셀 매핑 개요
------------

* 등록된 호스트는 셀(cell)에 매핑되어야 스케줄러의 배치 대상이 됨
* 매핑은 ``nova-manage cell_v2 discover_hosts`` 가 수행 — 배포 도구가
  주기적 실행을 자동화하는 것이 일반적
* 셀 내부 구조는 이 절의 범위 밖 (후속 문서에서 다룰 수 있음)

등록을 마친 노드에서 Nova 가 실제로 VM 을 만들고 격리하는 과정은
:doc:`nova-libvirt-kvm` 에서 이어집니다.


배포 방식 비교
==============

컨테이너화된 OpenStack 을 올리는 배포 방식은 크게 둘입니다.

* :doc:`openstack-helm` — Helm chart 기반, Kubernetes 위 배포
* Kolla-Ansible — Ansible + Docker 기반(Kubernetes 아님)

두 방식의 상세 비교와 선택 기준은 :doc:`comparison` 에서 다룹니다. 두 방식이
공통으로 사용하는 컨테이너 이미지 레이어는 :doc:`kolla` 를 참고하세요.
