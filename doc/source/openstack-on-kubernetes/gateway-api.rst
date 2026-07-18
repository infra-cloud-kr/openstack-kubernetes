====================
Gateway API
====================

Gateway API 는 Kubernetes 의 트래픽 진입(라우팅) 표준입니다. 기존 Ingress 의
후속 격으로, OpenStack-Helm 최신 설치에서 서비스 노출 진입점으로 쓰입니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


Ingress 와의 관계
=================

* Ingress 의 한계(확장성/역할 분리)와 Gateway API 가 이를 개선한 지점
* 리소스 모델 — GatewayClass / Gateway / HTTPRoute

.. todo::

   Ingress → Gateway API 리소스 대응 관계를 표로 정리.


openstack-helm 에서의 역할
==========================

* OpenStack 서비스 엔드포인트를 외부로 노출하는 진입점
* K8s 전제조건으로서의 설치 위치 — :doc:`../labs/openstack-helm-lab`
* MetalLB(:doc:`metallb`)와의 관계 — L4(LB) 위의 L7(라우팅)

.. todo::

   Gateway 구현체 선택과 최소 설정 예시 보강.


더 읽을거리
===========

.. todo::

   Gateway API 공식 문서 등 참고 링크 보강.
