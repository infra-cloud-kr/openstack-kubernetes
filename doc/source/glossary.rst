======
용어집
======

본 프로젝트에서 자주 쓰는 용어를 정리합니다. 새 용어를 추가할 때는 가나다/
알파벳 순서를 유지하고, 번역 시 일관된 표기를 위해 이 용어집을 참조하세요.

.. glossary::
   :sorted:

   CAPI
      Cluster API. Kubernetes 클러스터의 수명주기를 선언적으로 관리하기 위한
      프로젝트. Magnum 의 최신 드라이버가 CAPI 기반으로 이동하고 있다.

   CCM
      Cloud Controller Manager. 클라우드별 통합(노드 수명주기, 로드밸런서,
      라우팅 등)을 코어에서 분리하여 제공하는 Kubernetes 컴포넌트.
      OpenStack 통합은 cloud-provider-openstack 으로 제공된다.

   CSI
      Container Storage Interface. 컨테이너 오케스트레이터에 스토리지를
      연결하기 위한 표준 인터페이스. Cinder CSI 드라이버가 대표적이다.

   Cinder
      OpenStack 의 블록 스토리지 서비스.

   Glance
      OpenStack 의 이미지 서비스.

   GitOps
      Git 저장소를 단일 진실 공급원(source of truth)으로 삼아 인프라/배포를
      선언적으로 관리하는 운영 방식. FluxCD, ArgoCD 가 대표적이다.

   Keystone
      OpenStack 의 인증(identity) 서비스.

   Kolla
      OpenStack 서비스의 프로덕션용 컨테이너 이미지를 제공하는 프로젝트.
      Kolla-Ansible 은 이를 Ansible 로 배포·운영한다.

   Kubernetes
      컨테이너화된 애플리케이션을 자동으로 배포·스케일링·관리하는 오픈소스
      프로젝트. CNCF 의 핵심 프로젝트.

   Magnum
      OpenStack 에서 컨테이너 오케스트레이션 엔진(주로 Kubernetes)을
      Container-as-a-Service 형태로 제공하는 프로젝트.

   Neutron
      OpenStack 의 네트워킹 서비스.

   Nova
      OpenStack 의 컴퓨트(compute) 서비스.

   Octavia
      OpenStack 의 로드밸런싱 서비스.

   OpenStack
      풀링된 가상 리소스로 프라이빗·퍼블릭 클라우드를 구축·관리하는 오픈소스
      프로젝트. Open Infrastructure Foundation 의 핵심 프로젝트.

   SIG
      Special Interest Group. 공통 관심 주제를 중심으로 모이는 커뮤니티
      그룹. OpenStack 에서는 릴리스 산출물을 직접 책임지지 않는 형태의
      워킹 그룹을 가리킨다.

   Swift
      OpenStack 의 오브젝트 스토리지 서비스.

   Weblate
      웹 기반 번역 플랫폼. Git 연동과 번역 메모리/용어집 기능을 제공한다.

   openstack-helm
      OpenStack 서비스를 Helm chart 로 패키징하여 Kubernetes 위에 배포하는
      프로젝트.
