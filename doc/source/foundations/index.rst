==========
기초 개념
==========

실습에 앞서 이해해 두면 좋은 개념 레이어를 정리합니다. 가상화 기초에서
시작해 OpenStack 핵심 개념과 그 네트워킹·스토리지 서비스, Kubernetes 핵심
개념, 두 기술을 잇는 표준 인터페이스까지 순서대로 다룹니다.

두 기술을 결합할 때의 네트워킹(CNI 공존·MetalLB·Gateway API)은 여기가 아니라
:doc:`../integration-patterns` 에서 다룹니다.

.. note::

   기여자 작업용 골격입니다. 각 문서의 세부 절을 실습 경험과 공식 문서를
   바탕으로 보강해 주세요.

.. toctree::
   :maxdepth: 1

   vm-vs-container
   openstack
   kubernetes-fundamentals
   bridging-concepts
