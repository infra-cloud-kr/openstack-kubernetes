========================
로드 밸런싱 (Octavia)
========================

Octavia 는 OpenStack 의 로드 밸런싱(LBaaS) 서비스입니다. 이 문서는 서비스
자체의 개념을 다루며, Kubernetes ``Service`` 의 백엔드로 쓰는 관점은
:doc:`../kubernetes-on-openstack/octavia-load-balancer` 에서 다룹니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


개념
====

* 로드밸런서 / 리스너 / 풀 / 멤버 / 헬스 모니터
* amphora 드라이버와 OVN Octavia 드라이버

.. todo::

   각 리소스의 관계와 트래픽 흐름을 다이어그램으로 정리.


더 읽을거리
===========

.. todo::

   Octavia 공식 문서 등 참고 링크 보강.
