====================
OVN / OVS
====================

OVN(Open Virtual Network)과 OVS(Open vSwitch)는 Neutron 의 대표적인 SDN
백엔드입니다. 최근 배포에서 기본값으로 자리 잡은 OVN 을 중심으로 정리합니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


OVS 와 OVN 의 관계
==================

* OVS — 호스트 단의 가상 스위치(데이터 평면)
* OVN — OVS 위에 논리 네트워크(라우팅/L2/L3)를 얹는 컨트롤 평면

.. todo::

   OVN 도입으로 기존 Neutron 에이전트 구조가 어떻게 단순화되는지 정리.


더 읽을거리
===========

.. todo::

   OVN / ovn-kubernetes 참고 링크 보강.
