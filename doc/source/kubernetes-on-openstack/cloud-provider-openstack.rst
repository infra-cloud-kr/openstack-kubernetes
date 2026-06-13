========================================
cloud-provider-openstack (CCM)
========================================

`cloud-provider-openstack
<https://github.com/kubernetes/cloud-provider-openstack>`_ 는 Kubernetes 의
Cloud Controller Manager(CCM) 및 관련 컴포넌트를 통해 Kubernetes 를 OpenStack
서비스와 통합합니다.

.. note::

   기여자 작업용 골격입니다. 공식 저장소 문서를 바탕으로 보강해 주세요.


제공 기능
=========

* **노드 수명주기** — OpenStack 인스턴스와 Kubernetes 노드의 연동
* **로드밸런서** — Octavia 기반 ``Service type=LoadBalancer`` 프로비저닝
  (:doc:`octavia-load-balancer`)
* **라우팅 / 네트워크** — Neutron 연동
* **인증** — Keystone 기반 인증/인가(webhook)


in-tree 에서 out-of-tree 로
===========================

Kubernetes 는 클라우드별 통합 코드를 코어(in-tree)에서 분리하여 별도
프로바이더(out-of-tree)로 옮겨 왔습니다. OpenStack 통합 역시 CCM 으로
제공되며, 이것이 현재 권장되는 방식입니다.


참고
====

* cloud-provider-openstack —
  https://github.com/kubernetes/cloud-provider-openstack
