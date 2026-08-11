=====================
Kubernetes 핵심 개념
=====================

통합 패턴(:doc:`../integration-patterns`)에서 OpenStack 을 K8s 위에 올릴 때, 각
OpenStack 컴포넌트가 어떤 K8s 리소스로 동작하는지를 미리 짚습니다. K8s 개념
자체의 상세는 공식 문서로 링크하고, 여기서는 "이 리소스가 OpenStack 의 무엇에
쓰이는가"에 초점을 둡니다.

.. note::

   기여자 작업용 골격입니다. K8s 개념을 재설명하지 말고, 각 리소스가 OpenStack
   컴포넌트에 어떻게 대응되는지(왜 알아야 하는지)를 한 줄로 유지하세요. 상세는
   공식 문서와 통합 패턴 섹션으로.


Workloads
=========

.. todo::

   * Deployment / ReplicaSet → 무상태 OpenStack API 서비스 (Keystone, Nova,
     Glance API 등)
   * StatefulSet → 상태 유지 컴포넌트 (DB, 메시지 큐)
   * 매핑 상세: :doc:`../openstack-on-kubernetes/openstack-helm`


네트워킹
========

.. todo::

   * Service (``type=LoadBalancer``) → OpenStack API 엔드포인트 노출, Octavia
     매핑 (:doc:`../kubernetes-on-openstack/octavia-load-balancer`)
   * Ingress / Gateway API → 외부 트래픽 진입
   * CNI → Pod 네트워킹, Neutron 공존
     (:doc:`../openstack-on-kubernetes/cni-and-neutron`)


스토리지
========

.. todo::

   * PV / PVC → OpenStack 스토리지(Cinder 볼륨) 소비
   * StorageClass → 동적 프로비저닝, Cinder CSI
     (:doc:`../kubernetes-on-openstack/cinder-csi`)


선언적 관리와 CRD
=================

Kubernetes에서는 원하는 상태(desired state)를 리소스에 선언하고,
컨트롤러(Controller)가 현재 상태(current state)와 비교하여 두 상태가
일치하도록 지속적으로 조정(reconciliation)합니다.

OpenStack과 Kubernetes를 연동하는 일부 프로젝트에서는 이러한 선언적 관리
방식을 사용하여 OpenStack API로 관리되는 인프라의 원하는 상태를 Kubernetes
리소스로 표현합니다.

이때 사용자 정의 리소스 정의(CustomResourceDefinition, :term:`CRD`)는
Kubernetes 기본 리소스로 표현하기 어려운 OpenStack 연동 대상을 새로운
리소스 종류로 정의하는 데 사용됩니다.
사용자는 CRD를 통해 추가된 사용자 정의 리소스(Custom Resource)에 원하는
상태를 선언합니다.

이 연동 구조에서 컨트롤러나 :term:`오퍼레이터(Operator) <operator>` 는
사용자 정의 리소스를 감시하고, OpenStack API를 호출하여 선언된 상태가 실제
인프라에 반영되도록 조정합니다.
CRD 자체가 OpenStack API를 호출하는 것이 아니라, 해당 리소스의 수명주기
관리 로직을 가진 컨트롤러나 오퍼레이터가 상태 조정을 수행합니다.

.. code-block:: text

   Custom Resource
     -> Controller/Operator
     -> OpenStack API
     -> 실제 인프라

대표 사례
---------

이 패턴을 OpenStack 연동에 적용한 대표 사례는 다음과 같습니다.
전체 연동 구조에서는 다음 영역에 해당합니다.

* **Magnum과 Cluster API(CAPI)·Cluster API Provider OpenStack(CAPO)** —
  :ref:`배포·프로비저닝 <bridging-concepts-provisioning>`
* **Metal3와 Ironic** —
  :ref:`베어메탈 (물리 서버) <bridging-concepts-baremetal>`


Magnum CAPI 드라이버와 CAPO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Magnum의 CAPI 기반 드라이버는 CAPI와 CAPO의 사용자 정의 리소스를 생성하고,
CAPO 컨트롤러는 OpenStack API를 호출하여 Nova·Neutron 등의
인프라를 조정합니다.

.. code-block:: text

   Magnum CAPI 드라이버
     -> Cluster API/CAPO 사용자 정의 리소스
     -> CAPI/CAPO 컨트롤러
     -> OpenStack API(Nova·Neutron 등)
     -> Kubernetes 클러스터 인프라

이 대응 관계를 알면 Magnum API로 받은 클러스터 생성 요청이 CAPI 리소스로
변환되는 단계와 CAPO가 실제 OpenStack 인프라를 조정하는 역할을 구분할 수
있습니다.

자세한 내용은 :doc:`../kubernetes-on-openstack/magnum` 과
:doc:`../kubernetes-on-openstack/cluster-api` 를 참고합니다.


.. _kubernetes-fundamentals-metal3-ironic:

Metal3와 Ironic
~~~~~~~~~~~~~~~~

:term:`Metal3` 는 ``BareMetalHost`` 리소스를 CRD로 제공합니다.
``BareMetalHost`` 는 OpenStack :term:`Ironic` 이 관리하는 물리 서버의
원하는 상태를 표현합니다.

Metal3의 Bare Metal Operator(BMO)는 Kubernetes 컨트롤러로서
``BareMetalHost`` 를 감시하고 Ironic API를 호출하여 물리 서버의 검사와
프로비저닝을 조정합니다.

.. code-block:: text

   BareMetalHost -> BMO -> Ironic API -> 물리 서버

이 대응 관계를 알면 Kubernetes에 선언된 물리 서버의 상태와 Ironic이
수행하는 실제 하드웨어 작업의 경계를 구분할 수 있습니다.

더 읽을거리
===========

* `Kubernetes 객체 공식 문서
  <https://kubernetes.io/docs/concepts/overview/working-with-objects/>`_
* `컨트롤러 공식 문서
  <https://kubernetes.io/docs/concepts/architecture/controller/>`_
* `Custom Resources 공식 문서
  <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>`_
* `Operator 패턴 공식 문서
  <https://kubernetes.io/docs/concepts/extend-kubernetes/operator/>`_
