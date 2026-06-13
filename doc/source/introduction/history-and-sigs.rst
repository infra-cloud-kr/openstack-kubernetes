==========================================
두 커뮤니티의 만남: SIG 활동의 역사와 현재
==========================================

OpenStack 과 Kubernetes 의 통합은 어느 날 갑자기 등장한 것이 아니라, 두
커뮤니티가 오랜 기간 협력하며 형성해 온 흐름입니다. 이 절에서는 그 역사를
SIG(Special Interest Group, 특별 관심 그룹) 활동을 중심으로 살펴보고, 현재의
통합 지형이 어떻게 정리되었는지 정리합니다.

.. note::

   이 문서는 본문 내용을 단계적으로 확장하는 것을 전제로 한 초기
   골격입니다. 각 절에는 참조해야 할 1차 출처를 함께 명시했으므로,
   기여자는 출처를 직접 확인하며 내용을 보강하시기 바랍니다.


배경: VM, bare metal, container 가 공존하는 인프라 현실
=======================================================

현실의 인프라는 단일 추상화로 수렴하지 않습니다. 가상 머신(VM), 베어메탈
(bare metal), 컨테이너(container)가 같은 데이터센터 안에서 공존하며, 각각이
가장 잘 맞는 워크로드를 담당합니다. OpenStack 은 이 이종(heterogeneous)
리소스를 풀링하여 클라우드로 제공하는 데 강하고, Kubernetes 는 그 위에서
컨테이너화된 애플리케이션의 수명주기를 관리하는 데 강합니다.

Open Infrastructure Foundation 의 컨테이너 백서
(`Leveraging Containers and OpenStack
<https://www.openstack.org/use-cases/containers/leveraging-containers-and-openstack/>`_)
는 OpenStack 과 컨테이너가 만나는 지점을 크게 세 가지 시나리오로 정리합니다.

#. **인프라 컨테이너 (Infrastructure Containers)** — OpenStack 서비스 자체를
   컨테이너로 패키징하여, 배포·업그레이드·운영 수명주기 전체를 오케스트레이션
   도구와 컨테이너화된 서비스로 관리하는 방식. openstack-helm, Kolla,
   OpenStack-Ansible 등이 여기에 해당합니다.
#. **컨테이너 애플리케이션 프레임워크 (Containerized Application
   Frameworks)** — Kubernetes, Docker Swarm 같은 컨테이너 오케스트레이션
   엔진을 OpenStack 클라우드 인프라 위에서 호스팅하는 방식. Nova(compute),
   Neutron(networking), Cinder(storage)가 그 기반을 제공합니다.
#. **나란히 통합 (Side-by-Side Integrations)** — 독립적으로 배포된 OpenStack
   과 Kubernetes 가 표준 API 를 통해 협력하는 방식. Kubernetes 가 스토리지,
   로드밸런싱, 인증 등을 위해 OpenStack 서비스를 호출합니다.

이 세 가지 시나리오는 오늘날 우리가 :doc:`../openstack-on-kubernetes/index`
(첫 번째 시나리오)와 :doc:`../kubernetes-on-openstack/index` (두 번째·세 번째
시나리오)로 부르는 구조의 원형입니다.


참고 자료
=========

* Introducing the Kubernetes OpenStack SIG (2016) —
  https://kubernetes.io/blog/2016/04/introducing-kubernetes-openstack-sig/
* OpenStack SIGs (거버넌스) —
  https://governance.openstack.org/tc/reference/sigs/
* Leveraging Containers and OpenStack (백서) —
  https://www.openstack.org/use-cases/containers/leveraging-containers-and-openstack/
