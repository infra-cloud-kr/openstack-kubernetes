=======================
OpenStack on Kubernetes
=======================

OpenStack 의 각 서비스(Nova, Neutron, Keystone, Glance, Swift 등)를 컨테이너로
패키징해 Kubernetes 위에서 운영하는 방식입니다.
:doc:`../introduction/history-and-sigs` 에서 말한 "인프라 컨테이너" 시나리오에
해당합니다.

올리는 방법은 하나가 아니지만(:doc:`approaches`), 이 섹션은 그 기반이 되는
openstack-helm 을 중심으로 준비부터 운영까지 짚습니다.

.. toctree::
   :maxdepth: 1
   :caption: 개념·설계

   concepts
   approaches
   reference-architecture

.. toctree::
   :maxdepth: 1
   :caption: K8s 네트워킹 준비

   cni-and-neutron
   gateway-api
   metallb

.. toctree::
   :maxdepth: 1
   :caption: 배포

   openstack-helm
   kolla
   comparison

.. toctree::
   :maxdepth: 1
   :caption: 운영

   operations
