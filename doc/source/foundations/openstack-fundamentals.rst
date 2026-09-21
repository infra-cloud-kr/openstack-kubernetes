====================
OpenStack 주요 특징
====================

주요 서비스
=============


OpenStack의 주요 서비스는 다음의 표와 같다.

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :align: left

   * - 서비스
     - 역할
   * - **Keystone(키스톤)** — 인증 서비스
     - OpenStack의 모든 서비스 중앙 인증, 사용자 자격 증명, 역할 기반
       접근 제어(role-based access control, RBAC) 및
       서비스 카탈로그(service catalog) 관리 담당
   * - **Nova(노바)** — 컴퓨팅 서비스
     - 가상 머신(virtual machine, VM) 및 컴퓨팅 자원의
       프로비저닝(provisioning), 스케줄링(scheduling),
       수명 주기(lifecycle)를 담당
   * - **Placement(플레이스먼트)** — 리소스 추적 서비스
     - 컴퓨팅 리소스의 인벤토리(inventory)와 할당 정보를 추적하여
       Nova 스케줄러가 적절한 호스트를 선택할 수 있도록 지원
   * - **Neutron(뉴트론)** — 네트워킹 서비스
     - 가상 네트워크, IP 주소 관리, L2/L3 라우팅, 테넌트 간 네트워크 격리,
       소프트웨어 정의 네트워킹(software-defined networking, SDN) 통합 등
       네트워킹 전반 담당
   * - **Cinder(신더)** — 블록 스토리지 서비스
     - 인스턴스에 연결하여 사용할 수 있는 영구적 블록 스토리지 생성,
       연결, 스냅샷 관리 담당
   * - **Swift(스위프트)** — 오브젝트 스토리지 서비스
     - 이미지, 백업 등 대규모 비정형 데이터를 오브젝트 단위로 분산 저장하고
       REST API로 제공
   * - **Glance(글랜스)** — 이미지 서비스
     - VM에 사용될 디스크 이미지 및 메타데이터(metadata) 등록, 검색,
       카탈로그화 및 배포 담당
   * - **Horizon(호라이즌)** — 웹 대시보드
     - 사용자와 관리자가 클라우드 자원을 시각적으로 관리할 수 있는
       그래픽 사용자 인터페이스(graphical user interface, GUI) 대시보드


OpenStack의 서비스 구조와 컨테이너 배포
=======================================

앞에서 소개한 Nova, Neutron, Cinder와 같은 OpenStack 서비스는 각각
단일 프로세스로 실행되지 않는다.
각 서비스는 외부 요청을 받는 API 프로세스와 스케줄러(scheduler),
컨덕터(conductor), 컴퓨트(compute), 에이전트(agent) 등 내부 작업을
담당하는 여러 프로세스로 구성된다.
이들 프로세스는 데이터베이스와 메시지 브로커(message broker) 같은
공용 인프라를 사용한다.

API 접근과 서비스 간 통신
----------------------------

사용자나 클라이언트가 OpenStack 서비스 API를 호출하려면 먼저 인증하고
API 엔드포인트(endpoint)를 확인해야 한다.
Keystone은 공통 인증을 처리하고 토큰과 서비스 카탈로그를 제공한다.
사용자나 클라이언트는 카탈로그에 등록된 Nova, Neutron, Cinder 등의
API 엔드포인트를 확인한 뒤 각 서비스의 API를 직접 호출한다.

OpenStack 서비스 간 기능 호출도 주로 각 서비스가 제공하는 HTTP API를
통해 이루어진다.
같은 서비스에 속한 분산 프로세스 사이에서는 ``oslo.messaging`` 기반
원격 프로시저 호출(remote procedure call, RPC)과 알림을 사용한다.
리소스 메타데이터와 제어 상태는 일반적으로 SQL 데이터베이스에 저장된다.

다음은 이러한 구조를 단순화한 것이다.

.. code-block:: text

   사용자 · CLI · SDK
          │
          ├── 인증 · 서비스 검색 ──> Keystone
          │                          └─ 토큰 · 서비스 카탈로그
          │
          └── 토큰으로 각 서비스 API 호출
                          │
               Nova · Neutron · Cinder API
                          │
               ┌──────────┴──────────┐
               ▼                     ▼
       서비스별 SQL 데이터베이스   메시지 브로커
                                      │
                                      ▼
                              RPC · 알림 처리
                         Scheduler · Conductor
                         Compute · Agent 등

이 그림은 일반적인 구조를 단순화한 것이다.
서비스마다 세부 구성과 통신 방식은 다를 수 있다.

컨테이너 배포
----------------

앞에서 살펴본 것처럼 OpenStack은 역할별 프로세스가 분리되어 있고,
각 프로세스는 API, 메시지 큐, 데이터베이스와 같은 명시적인 인터페이스를
통해 연결된다.
이 구조에서는 서비스 사이의 경계를 바꾸지 않고 각 프로세스의 실행 환경을
별도로 패키징할 수 있다.

패키지 기반 배포에서는 OpenStack 데몬과 의존 라이브러리를 각 호스트의
운영체제에 설치하고 ``systemd`` 서비스로 관리한다.
컨테이너 기반 배포에서는 OpenStack 데몬과 데몬 실행에 필요한 사용자 공간
의존성을 컨테이너 이미지로 묶는다.
운영자는 동일한 이미지를 여러 노드에 배포해 호스트별 패키지 상태에 대한
의존성을 줄이고 일관된 실행 환경을 구성할 수 있다.

컨테이너화는 OpenStack의 서비스 구조를 새로 만드는 것이 아니라 기존의
역할 구분과 통신 구조를 유지하면서 실행 환경을 표준화하는 방법이다.
이러한 특성 때문에 OpenStack의 서비스 구조는 컨테이너 기반 배포와 잘 맞는다.

구성 요소별 배포 고려사항
-------------------------

컨테이너 이미지는 실행 환경을 표준화하지만 구성 요소의 실행 위치,
호스트 접근, 데이터 영속성에 대한 요구사항까지 없애지는 않는다.
따라서 각 구성 요소의 역할과 의존성에 맞게 배포 방식을 설계해야 한다.

.. list-table::
   :header-rows: 1
   :widths: 22 30 48

   * - 구분
     - 예
     - 배포 시 고려사항
   * - 중앙 제어 평면 프로세스
     - ``nova-api``, ``nova-scheduler``,
       ``nova-conductor``, ``neutron-server``
     - 중앙 제어 노드에 여러 인스턴스로 배치할 수 있다.
       데이터베이스, 메시지 브로커 및 다른 서비스의 API와
       연결되어야 한다.
   * - 호스트 종속 프로세스
     - ``nova-compute``, Neutron 네트워크 에이전트
     - 자신이 관리하는 하이퍼바이저(hypervisor), Open vSwitch, 네트워크
       인터페이스 등이 있는 노드에서 실행되어야 한다.
       컨테이너로 실행하더라도 임의의 노드로 이동할 수 없다.
   * - 상태 저장 지원 인프라
     - MariaDB, RabbitMQ
     - 컨테이너의 실행뿐 아니라 영속 스토리지, 복제, 쿼럼(quorum),
       백업과 복구를 함께 설계해야 한다.

예를 들어 ``nova-compute`` 프로세스는 자신이 관리하는 하이퍼바이저가 있는
컴퓨트 노드에서 실행되어야 한다.
Neutron 에이전트 역시 해당 노드의 Open vSwitch, 네트워크 인터페이스,
커널 네트워크 기능에 접근해야 한다.
Kubernetes 위에 배포하더라도 이러한 노드 종속성은 유지된다.

MariaDB와 RabbitMQ도 컨테이너로 실행할 수 있다.
그러나 컨테이너를 다시 생성하는 것만으로 데이터베이스나 메시지 브로커
클러스터가 복구되는 것은 아니다.
컨테이너 런타임이나 Kubernetes는 프로세스를 다시 실행할 수 있지만,
데이터 일관성과 클러스터 복구는 각 시스템의 운영 방식에 따라 관리해야 한다.

따라서 배포 도구는 구성 요소마다 다른 호스트 종속성과 데이터 관리 요구사항을
반영해야 한다.


OpenStack 배포 방식
============================

앞 절에서는 OpenStack의 서비스 구조가 컨테이너 배포와 잘 맞는 이유를
설명했다.
실제 환경에서는 목적과 운영 기반에 따라 서로 다른 배포 방식과 도구를
선택한다.
여기서는 DevStack, Kolla-Ansible, openstack-helm의 주요 용도와
실행·관리 기반을 간단히 살펴본다.


배포 방식 비교
--------------

.. list-table::
   :header-rows: 1
   :widths: 22 28 50
   :align: left

   * - 방식
     - 실행·관리 기반
     - 주요 용도와 특징
   * - DevStack
     - 셸 스크립트(shell script)
     - 개발과 학습을 위한 빠른 OpenStack 배포
   * - Kolla-Ansible
     - Docker 또는 Podman과 Ansible
     - Kubernetes 없이 컨테이너화된 OpenStack 운영
   * - openstack-helm
     - Kubernetes와 Helm
     - Helm chart를 이용한 선언적(declarative) OpenStack 배포


방식별 특징
-----------

DevStack
   개발과 테스트 환경에 OpenStack을 빠르게 구성하기 위한 스크립트 모음이다.
   학습과 기능 검증에는 유용하지만 프로덕션 운영을 목적으로 하지 않는다.

Kolla-Ansible
   Kolla가 제공하는 OpenStack 서비스 컨테이너 이미지를 Docker 또는 Podman으로
   실행하고 Ansible playbook으로 배포·설정한다.
   Kubernetes 없이 컨테이너화된 OpenStack을 운영할 때 사용할 수 있다.

openstack-helm
   OpenStack 서비스를 Helm chart로 패키징하여 Kubernetes 위에 배포한다.
   Kubernetes의 선언적 리소스 관리와 복구·롤아웃(rollout) 기능을
   OpenStack 운영에 활용한다.

이 프로젝트는 openstack-helm을 중심으로 Kubernetes 위에 OpenStack을 배포하고
운영하는 방법을 다룬다.
관련 배포 방식과 프로젝트는
:doc:`../openstack-on-kubernetes/approaches` 에서 살펴본다.
Kolla-Ansible과
openstack-helm의 상세 차이는 :doc:`../openstack-on-kubernetes/comparison` 에서
다룬다.


실습 전 기본 명령
=================

아래 예시는 리소스를 변경하지 않는 조회 명령이다.
명령을 실행하기 전에
OpenStackClient를 설치하고 ``openrc`` 파일이나 ``clouds.yaml`` 파일로
인증 정보를 설정해야 한다.

서비스 카탈로그를 조회하여 현재 인증 정보와 API 접근이 정상인지 확인한다.

.. code-block:: console

   $ openstack catalog list

컴퓨팅에 필요한 이미지와 플레이버(flavor), 현재 프로젝트의 인스턴스를
조회한다.

.. code-block:: console

   $ openstack image list
   $ openstack flavor list
   $ openstack server list

네트워크와 서브넷, 라우터를 조회한다.

.. code-block:: console

   $ openstack network list
   $ openstack subnet list
   $ openstack router list

Cinder와 Swift가 배포된 환경에서는 블록 볼륨과 오브젝트 스토리지 컨테이너를
조회할 수 있다.

.. code-block:: console

   $ openstack volume list
   $ openstack container list

목록에서 확인한 리소스의 이름이나 ID를 ``show`` 명령에 전달하면 상세 정보를
확인할 수 있다.

.. code-block:: console

   $ openstack server show <server>
   $ openstack image show <image>
   $ openstack network show <network>
   $ openstack volume show <volume>

인스턴스에 연결된 네트워크 포트와 볼륨, Swift 컨테이너에 저장된 오브젝트도
조회할 수 있다.

.. code-block:: console

   $ openstack port list --server <server>
   $ openstack server volume list <server>
   $ openstack object list <container>

자동화나 후처리가 필요하면 ``-f`` 로 출력 형식을, ``-c`` 로 출력할 열을
선택한다.

.. code-block:: console

   $ openstack server list -f yaml
   $ openstack server list -f json
   $ openstack server list -f value -c ID -c Name

``<server>``, ``<image>`` 와 같은 값은 실제 리소스의 이름이나 ID로 바꿔
실행한다.


더 읽을거리
===========

* `OpenStack 논리적 아키텍처
  <https://docs.openstack.org/ko_KR/install-guide/get-started-logical-architecture.html>`_
* `OpenStack 개념적 아키텍처
  <https://docs.openstack.org/ko_KR/install-guide/get-started-conceptual-architecture.html>`_
* `Kolla-Ansible 고급 구성
  <https://docs.openstack.org/kolla-ansible/latest/admin/advanced-configuration.html>`_
* `DevStack 공식 문서 <https://docs.openstack.org/devstack/latest/>`_
* `openstack-helm 공식 문서
  <https://docs.openstack.org/openstack-helm/latest/>`_
* `OpenStack 메시지 큐 구성
  <https://docs.openstack.org/install-guide/environment-messaging.html>`_
* `OpenStack SQL 데이터베이스 구성
  <https://docs.openstack.org/install-guide/environment-sql-database.html>`_
