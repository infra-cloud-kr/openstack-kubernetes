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

.. todo::

   * CRD / Operator → Magnum 드라이버, Metal3 ``BareMetalHost`` 등 통합
     프로젝트의 기반 (:doc:`bridging-concepts`)


더 읽을거리
===========

.. todo::

   Kubernetes 공식 개념 문서(kubernetes.io/docs/concepts) 링크.
