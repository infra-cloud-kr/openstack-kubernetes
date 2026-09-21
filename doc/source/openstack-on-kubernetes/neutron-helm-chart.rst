==================================
Neutron Helm Chart 구조 파악
==================================

`openstack-helm <https://opendev.org/openstack/openstack-helm>`_ 의 neutron
chart 는 OpenStack 네트워킹 서비스를 Kubernetes 위에 배포하는 Helm chart 다.
이 문서는 `차트 디렉터리 <https://github.com/openstack/openstack-helm/tree/master/neutron>`_
의 파일 구성과 각 항목이 실제 Kubernetes 리소스로 어떻게 구현되는지를 정리한다.


차트 최상위 파일
================

.. code-block:: text

   neutron/
   ├── Chart.yaml        # 차트 메타데이터
   ├── values.yaml       # 기본값 정의
   ├── requirements.yaml # 의존 차트 선언
   └── templates/        # Kubernetes 리소스 템플릿

**Chart.yaml** 은 차트 이름, 버전(``2026.1.0``), appVersion(``28.0.0``)을 선언하며,
``helm-toolkit`` 을 라이브러리 의존성으로 등록한다.
helm-toolkit 은 openstack-helm 전체에서 공통 스니펫(snippet)을 제공하는 내부 라이브러리
차트로, 실제 Kubernetes 리소스를 직접 생성하지는 않는다.

**values.yaml** 은 배포 시 오버라이드할 수 있는 기본값 전체를 담는다.
주요 최상위 블록은 아래 표와 같다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 블록
     - 역할
   * - ``images``
     - 컴포넌트별 컨테이너 이미지 태그
   * - ``labels``
     - 각 Deployment/DaemonSet 의 ``nodeSelector`` 키값
   * - ``network``
     - ``backend`` 리스트로 ``openvswitch`` 또는 ``ovn`` 선택
   * - ``conf``
     - ``neutron.conf``, ``ml2_conf.ini`` 등 설정 파일 내용 (INI 형식)
   * - ``endpoints``
     - Keystone/MariaDB/RabbitMQ 등 외부 서비스 URL 과 자격증명
   * - ``dependencies``
     - 각 컴포넌트의 기동 선행 조건 (Job 완료 여부, 서비스 Ready 여부)
   * - ``manifests``
     - 리소스별 ``true``/``false`` 토글 — 원하지 않는 컴포넌트를 비활성화


templates/ 디렉터리 구성
=========================

templates/ 아래 파일들은 역할에 따라 다음과 같이 묶인다.

설정 관련
---------

``bin/`` 디렉터리에는 각 컴포넌트의 기동 스크립트가 ``_*.sh.tpl`` 형식으로
들어 있다.
Helm 이 렌더링하면 ``configmap-bin.yaml`` 에 의해
단일 ConfigMap 으로 묶여 각 Pod 의 ``/tmp/`` 경로에 마운트된다.

``configmap-etc.yaml`` 은 ``values.yaml`` 의 ``conf`` 블록 값을
``neutron.conf``, ``ml2_conf.ini``, ``l3_agent.ini`` 등 설정 파일로 렌더링한다.
특이한 점은 이 템플릿 내부에서 ``endpoints`` 블록을 참조해 DB 접속 URL,
RabbitMQ transport URL, Keystone auth_url 등을 자동으로 채워 넣는다는 것이다.

.. code-block:: text

   values.yaml
     endpoints.oslo_db  ──┐
     endpoints.oslo_messaging ─┤→ configmap-etc → /etc/neutron/neutron.conf (Pod 마운트)
     endpoints.identity ──┘

워크로드 관련
-------------

컴포넌트의 역할에 따라 Kubernetes 워크로드 타입이 다르게 선택된다.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 템플릿 파일
     - Kubernetes 리소스
     - 배포 이유
   * - ``deployment-server.yaml``
     - Deployment
     - API 서버는 노드 독립적/스테이트리스 → replicas 조정 가능
   * - ``deployment-rpc_server.yaml``
     - Deployment
     - RabbitMQ RPC 처리 전담. API 서버와 분리해 부하 격리
   * - ``deployment-ironic-agent.yaml``
     - Deployment
     - 베어메탈 연동. 특정 노드가 아닌 임의 노드에서 실행 가능
   * - ``daemonset-ovs-agent.yaml``
     - DaemonSet
     - OVS 브리지/포트를 호스트마다 관리해야 하므로 노드 단위 배포
   * - ``daemonset-ovn-agent.yaml``
     - DaemonSet
     - OVN logical flow 동기화. 역시 노드 단위
   * - ``daemonset-dhcp-agent.yaml``
     - DaemonSet
     - dnsmasq 가 각 노드의 네트워크 네임스페이스에서 실행
   * - ``daemonset-l3-agent.yaml``
     - DaemonSet
     - 가상 라우터/NAT/플로팅 IP 처리, 호스트 네트워크 네임스페이스 필요
   * - ``daemonset-metadata-agent.yaml``
     - DaemonSet
     - ``169.254.169.254`` 메타데이터 프록시, 노드별 실행
   * - ``daemonset-ovn-metadata-agent.yaml``
     - DaemonSet
     - OVN 환경에서의 메타데이터 프록시
   * - ``daemonset-sriov-agent.yaml``
     - DaemonSet
     - SR-IOV VF 관리, 기본 비활성 (``manifests.daemonset_sriov_agent: false``)
   * - ``daemonset-bagpipe-bgp.yaml``
     - DaemonSet
     - BGP VPN 연동, 기본 비활성
   * - ``daemonset-netns-cleanup-cron.yaml``
     - DaemonSet
     - 고아 네트워크 네임스페이스 정리 크론

``network.backend`` 값에 따라 OVS 관련 또는 OVN 관련 DaemonSet 이
동적으로 활성화된다.
사용하지 않는 에이전트는 ``manifests`` 토글로
리소스 자체가 생성되지 않는다.

Job 관련
--------

서비스 기동 전 일회성 작업은 Helm Hook(``post-install``, ``post-upgrade``)으로
등록된 Job 으로 실행된다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Job 템플릿
     - 하는 일
   * - ``job-db-init.yaml``
     - MariaDB 에 neutron DB/사용자 생성
   * - ``job-db-sync.yaml``
     - ``neutron-db-manage upgrade head`` 로 DB 스키마 마이그레이션
   * - ``job-ks-user.yaml``
     - Keystone 에 neutron 서비스 계정 생성
   * - ``job-ks-service.yaml``
     - Keystone 에 ``network`` 타입 서비스 등록
   * - ``job-ks-endpoints.yaml``
     - Keystone 에 public/internal/admin 엔드포인트 URL 등록
   * - ``job-rabbit-init.yaml``
     - RabbitMQ 에 vhost/사용자/권한 설정
   * - ``job-bootstrap.yaml``
     - 초기 네트워크 리소스 생성 (선택)
   * - ``job-db-drop.yaml``
     - DB 삭제 (차트 제거 시, 기본 비활성)

기타 리소스
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 템플릿 파일
     - 생성되는 Kubernetes 리소스
   * - ``service-server.yaml``
     - ClusterIP Service (포트 9696) — neutron API 클러스터 내 노출
   * - ``secret-db.yaml`` / ``secret-rabbitmq.yaml`` / ``secret-keystone.yaml``
     - 각 서비스 자격증명을 담은 Secret
   * - ``pdb-server.yaml``
     - PodDisruptionBudget — API 서버 롤링 업데이트 시 최소 가용 Pod 보장
   * - ``network_policy.yaml``
     - NetworkPolicy — 인그레스/이그레스 제한
   * - ``certificates.yaml``
     - TLS 인증서 Secret (TLS 활성화 시)
   * - ``extra-manifests.yaml``
     - ``values.yaml`` 의 ``manifests.extra`` 에 정의된 임의 Kubernetes 리소스 주입


값 → 리소스 반영 흐름 요약
===========================

아래는 ``helm install`` 시 values.yaml 의 값이 실제 Kubernetes 리소스로 이어지는
흐름이다.

.. code-block:: text

   values.yaml
   ├── manifests.*: false     → 해당 템플릿 파일 렌더링 자체를 스킵
   ├── labels.server.*        → Deployment nodeSelector
   ├── labels.ovs.*           → DaemonSet(ovs-agent) nodeSelector
   ├── conf.*                 → configmap-etc → /etc/neutron/ 마운트
   ├── endpoints.*            → configmap-etc 내 URL 자동 생성 + Job 에서 참조
   ├── pod.replicas.server    → Deployment replicas
   └── network.backend        → 활성화할 DaemonSet 의존 관계 동적 결정
