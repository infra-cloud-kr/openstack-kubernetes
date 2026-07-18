==========
네트워킹
==========

OpenStack 이 제공하는 네트워킹 서비스를 다룹니다. 가상 네트워킹(Neutron)과 SDN
백엔드(OVN/OVS), 로드 밸런싱(Octavia)이 대상입니다. 두 기술을 결합할 때의
K8s-측 네트워킹(CNI 공존, Gateway API, MetalLB 등)은 통합 패턴 섹션에서
다룹니다.

.. note::

   기여자 작업용 골격입니다. 각 문서의 세부 절을 실습 경험과 공식 문서를
   바탕으로 보강해 주세요.

.. toctree::
   :maxdepth: 1

   neutron-basics
   ovn-ovs
   load-balancing
