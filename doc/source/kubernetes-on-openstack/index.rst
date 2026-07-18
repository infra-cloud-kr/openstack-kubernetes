=======================
Kubernetes on OpenStack
=======================

OpenStack 의 VM 인프라 위에 Kubernetes 클러스터를 프로비저닝·운영하는 방식을
다룹니다. 이는 :doc:`../introduction/history-and-sigs` 에서 설명한 "컨테이너
애플리케이션 프레임워크" 및 "나란히 통합" 시나리오에 해당합니다.

.. toctree::
   :maxdepth: 1
   :caption: 개념

   concepts

.. toctree::
   :maxdepth: 1
   :caption: 클러스터 프로비저닝

   magnum
   cluster-api

.. toctree::
   :maxdepth: 1
   :caption: OpenStack 자원 연동

   cloud-provider-openstack
   cinder-csi
   octavia-load-balancer
