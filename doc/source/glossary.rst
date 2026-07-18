======
용어집
======

본 프로젝트에서 자주 쓰는 용어를 정리합니다. 새 용어를 추가할 때는 가나다/
알파벳 순서를 유지하고, 번역 시 일관된 표기를 위해 이 용어집을 참조하세요.

아래 색인에서 글자를 누르면 해당 그룹으로 이동합니다.

.. rubric:: 색인

:ref:`C <glossary-c>` · :ref:`D <glossary-d>` · :ref:`G <glossary-g>` ·
:ref:`H <glossary-h>` · :ref:`I <glossary-i>` · :ref:`K <glossary-k>` ·
:ref:`M <glossary-m>` · :ref:`N <glossary-n>` · :ref:`O <glossary-o>` ·
:ref:`P <glossary-p>` · :ref:`R <glossary-r>` · :ref:`S <glossary-s>` ·
:ref:`V <glossary-v>` · :ref:`W <glossary-w>`


.. _glossary-c:

.. rubric:: C

.. glossary::
   :sorted:

   CAPI
      Cluster API. Kubernetes 클러스터의 수명주기를 선언적으로 관리하기 위한
      프로젝트. Magnum 의 최신 드라이버가 CAPI 기반으로 이동하고 있다.

   CAPO
      Cluster API Provider OpenStack. Cluster API 의 OpenStack 프로바이더로,
      OpenStack(Nova/Neutron 등) 위에 Kubernetes 클러스터를 프로비저닝한다.

   CCM
      Cloud Controller Manager. 클라우드별 통합(노드 수명주기, 로드밸런서,
      라우팅 등)을 코어에서 분리하여 제공하는 Kubernetes 컴포넌트.
      OpenStack 통합은 cloud-provider-openstack 으로 제공된다.

   CNI
      Container Network Interface. Kubernetes 의 Pod 네트워킹을 위한 표준
      인터페이스. Calico, Flannel 등이 구현체이며, OVN 은 ovn-kubernetes 로
      CNI 역할을 겸할 수 있다.

   CRD
      Custom Resource Definition. Kubernetes API 를 확장해 커스텀 리소스를
      등록하는 메커니즘. Operator, Cluster API, Metal3 등이 이를 기반으로 한다.

   CSI
      Container Storage Interface. 컨테이너 오케스트레이터에 스토리지를
      연결하기 위한 표준 인터페이스. Cinder CSI 드라이버가 대표적이다.

   Ceph
      블록·오브젝트·파일 스토리지를 모두 제공하는 분산 스토리지 플랫폼.
      OpenStack 과 Kubernetes 가 같은 백엔드를 공유하는 구성에 널리 쓰인다.

   Cinder
      OpenStack 의 블록 스토리지 서비스.

   Control Plane / Data Plane
      제어 평면(오케스트레이션·API·스케줄링)과 데이터 평면(실제 워크로드)을
      가리키는 구분. Nova 가 관리하는 VM 은 Kubernetes 밖의 데이터 평면에
      남는다.


.. _glossary-d:

.. rubric:: D

.. glossary::
   :sorted:

   DaemonSet
      각 노드마다 하나씩 Pod 를 실행하는 Kubernetes 오브젝트. 노드 단위
      에이전트(네트워크·스토리지 플러그인 등)에 쓰인다.

   Deployment
      무상태(stateless) 애플리케이션의 배포·롤아웃·스케일링을 관리하는
      Kubernetes 오브젝트.

   DevStack
      개발·학습용으로 단일 노드에 OpenStack 을 올인원으로 설치하는 도구.


.. _glossary-g:

.. rubric:: G

.. glossary::
   :sorted:

   Gateway API
      Kubernetes 의 트래픽 진입(라우팅) 표준. 기존 Ingress 의 후속 격이다.

   Glance
      OpenStack 의 이미지 서비스.

   GitOps
      Git 저장소를 단일 진실 공급원(source of truth)으로 삼아 인프라/배포를
      선언적으로 관리하는 운영 방식. FluxCD, ArgoCD 가 대표적이다.


.. _glossary-h:

.. rubric:: H

.. glossary::
   :sorted:

   Helm
      Kubernetes 용 패키지 매니저. Chart(템플릿) + Values(설정) + Release(배포
      인스턴스)로 구성된다.

   HPA
      Horizontal Pod Autoscaler. 부하에 따라 Pod 수를 자동으로 조절하는
      Kubernetes 오토스케일링 기능.


.. _glossary-i:

.. rubric:: I

.. glossary::
   :sorted:

   i18n / l10n
      국제화(internationalization, i18n)와 지역화(localization, l10n). i18n 은
      다국어 지원 구조를, l10n 은 특정 언어로의 번역·현지화를 가리킨다.

   Ingress
      Kubernetes 서비스를 외부에 노출하는 (구) 표준. Gateway API 로 대체되고
      있다.

   Ironic
      물리 서버(Bare Metal)를 프로비저닝·관리하는 OpenStack 서비스. Metal3 가
      이를 Kubernetes 에서 다루는 데 활용한다.


.. _glossary-k:

.. rubric:: K

.. glossary::
   :sorted:

   Keystone
      OpenStack 의 인증(identity) 서비스.

   Kolla
      OpenStack 서비스의 프로덕션용 컨테이너 이미지를 제공하는 프로젝트.
      openstack-helm 과 Kolla-Ansible 이 모두 이 이미지를 사용한다.

   Kolla-Ansible
      Kolla 컨테이너 이미지를 Ansible + Docker 로 배포·운영하는 도구.
      Kubernetes 위가 아니라 컨테이너로 직접 배포한다.

   Kubernetes
      컨테이너화된 애플리케이션을 자동으로 배포·스케일링·관리하는 오픈소스
      프로젝트. CNCF 의 핵심 프로젝트.


.. _glossary-m:

.. rubric:: M

.. glossary::
   :sorted:

   Magnum
      OpenStack 에서 컨테이너 오케스트레이션 엔진(주로 Kubernetes)을
      Container-as-a-Service 형태로 제공하는 프로젝트.

   Metal3
      Kubernetes 가 물리 서버(Bare Metal)를 ``BareMetalHost`` 등 커스텀
      리소스로 선언적으로 관리하게 해주는 프로젝트. 내부적으로 Ironic 을
      사용한다.

   MetalLB
      베어메탈·온프레미스 Kubernetes 에서 ``LoadBalancer`` 타입 Service 에
      외부 IP 를 제공하는 구현체.


.. _glossary-n:

.. rubric:: N

.. glossary::
   :sorted:

   Neutron
      OpenStack 의 네트워킹 서비스.

   Nova
      OpenStack 의 컴퓨트(compute) 서비스.


.. _glossary-o:

.. rubric:: O

.. glossary::
   :sorted:

   OVN
      Open Virtual Network. OVS 위에 논리 네트워크(L2/L3/라우팅)를 얹는 SDN.
      Neutron 의 대표적인 백엔드다.

   OVS
      Open vSwitch. 호스트 단의 가상 스위치(데이터 평면).

   Octavia
      OpenStack 의 로드밸런싱 서비스.

   OpenStack
      풀링된 가상 리소스로 프라이빗·퍼블릭 클라우드를 구축·관리하는 오픈소스
      프로젝트. Open Infrastructure Foundation 의 핵심 프로젝트.

   openstack-helm
      OpenStack 서비스를 Helm chart 로 패키징하여 Kubernetes 위에 배포하는
      프로젝트.

   operator
      CRD + 컨트롤러로 애플리케이션의 운영 지식을 코드화하는 Kubernetes 패턴.
      openstack-k8s-operators(RHOSO)가 이 방식으로 OpenStack 을 배포한다.


.. _glossary-p:

.. rubric:: P

.. glossary::
   :sorted:

   Pod
      Kubernetes 의 최소 배포 단위. 하나 이상의 컨테이너를 함께 실행한다.

   PV / PVC
      PersistentVolume / PersistentVolumeClaim. 각각 실제 스토리지 자원과 그
      자원에 대한 사용 요청. CSI 드라이버(예: Cinder CSI)로 연결된다.


.. _glossary-r:

.. rubric:: R

.. glossary::
   :sorted:

   Rook
      Ceph 등의 스토리지를 Kubernetes 오퍼레이터로 운영·관리하는 프로젝트.

   reconciliation loop
      선언된 원하는 상태(desired state)와 실제 상태를 지속적으로 비교해 맞추는
      Kubernetes 컨트롤러의 동작 방식.


.. _glossary-s:

.. rubric:: S

.. glossary::
   :sorted:

   SDN
      Software-Defined Networking. 소프트웨어로 네트워크를 정의·제어하는 방식.
      OpenStack 에서는 Neutron 이 담당한다.

   SIG
      Special Interest Group. 공통 관심 주제를 중심으로 모이는 커뮤니티
      그룹. OpenStack 에서는 릴리스 산출물을 직접 책임지지 않는 형태의
      워킹 그룹을 가리킨다.

   StatefulSet
      상태 유지가 필요한 워크로드(DB 등)를 위한 Kubernetes 오브젝트. 안정적인
      네트워크 ID 와 스토리지를 보장한다.

   StorageClass
      동적 볼륨 프로비저닝의 정책·백엔드를 정의하는 Kubernetes 오브젝트.

   Swift
      OpenStack 의 오브젝트 스토리지 서비스.


.. _glossary-v:

.. rubric:: V

.. glossary::
   :sorted:

   VM
      가상 머신(Virtual Machine). 하이퍼바이저 위에서 게스트 OS 커널까지 통째로
      격리해 실행한다. OpenStack 에서는 Nova 가 관리한다.


.. _glossary-w:

.. rubric:: W

.. glossary::
   :sorted:

   Weblate
      웹 기반 번역 플랫폼. Git 연동과 번역 메모리/용어집 기능을 제공한다.
