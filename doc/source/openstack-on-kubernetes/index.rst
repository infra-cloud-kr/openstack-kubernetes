=======================
OpenStack on Kubernetes
=======================

OpenStack 의 각 서비스(Nova, Neutron, Keystone, Glance, Swift 등)를 컨테이너로
패키징하여 Kubernetes 위에서 운영하는 방식을 다룹니다. 이는
:doc:`../introduction/history-and-sigs` 에서 설명한 "인프라 컨테이너" 시나리오에
해당하며, OpenStack 컨트롤 플레인 현대화의 대표적인 접근입니다.

.. toctree::
   :maxdepth: 1

   concepts
   openstack-helm
   kolla
   operations
