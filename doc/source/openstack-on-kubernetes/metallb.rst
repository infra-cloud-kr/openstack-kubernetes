================================
MetalLB (베어메탈 LoadBalancer)
================================

베어메탈/멀티노드 Kubernetes 에는 클라우드 LB 가 없어 ``LoadBalancer`` 타입
Service 가 외부 IP 를 못 받습니다. MetalLB 가 이 역할을 대신하며, OpenStack 을
Kubernetes 에 올리는(openstack-helm) 배포의 K8s 전제조건이기도 합니다
(:doc:`../labs/openstack-helm-lab`).

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


개요
====

* L2(ARP) 모드 vs BGP 모드
* IP 주소 풀 구성
* Octavia(OpenStack LBaaS)와의 역할 구분 — 계층이 다름(K8s Service ↔ OpenStack).
  OpenStack 측 로드 밸런싱 서비스는 :doc:`../networking/load-balancing` 참고

.. todo::

   L2/BGP 모드 선택 기준과 주소 풀 예시 보강.
