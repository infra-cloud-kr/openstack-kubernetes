====================
OVN / OVS
====================

OVN(Open Virtual Network)과 OVS(Open vSwitch)는 OpenStack Neutron에서
사용되는 대표적인 네트워크 기술입니다. OVS는 호스트에서 실제 네트워크
패킷을 전달하는 가상 스위치 역할을 하며, OVN은 OVS를 데이터 평면으로
사용하여 논리적인 네트워크를 구성하고 관리합니다.

최근 OpenStack 배포에서는 Neutron의 네트워크 백엔드로 ML2/OVN 구성이
널리 사용되고 있습니다.


OVS와 OVN의 관계
----------------

OVS는 호스트 단에서 동작하는 가상 스위치입니다.
VM의 가상 NIC, 물리 NIC, 터널 인터페이스 등을 연결하고 실제 패킷을
전달하는 데이터 평면(Data Plane) 역할을 담당합니다.

OVN은 OVS를 데이터 평면으로 사용하면서
논리적인 네트워크를 정의하고 관리하는 네트워크 제어 계층(Control Plane)
역할을 합니다. 논리 스위치, 논리 라우터, ACL 등의 네트워크
기능을 논리적인 객체로 표현할 수 있습니다.

OVN과 OVS는 다음과 같이 역할을
나누어 사용합니다.

.. code-block:: text

   Neutron Server
      |
      | ML2/OVN
      v
     OVN
      |
      | 네트워크 상태 반영
      v
   ovn-controller
      |
      v
     OVS
      |
      | 실제 패킷 전달
      v
     VM

간단하게 정리하면 다음과 같습니다.

* **OVS**: 호스트 단의 가상 스위치(데이터 평면)
* **OVN**: OVS 위에 논리 네트워크(라우팅/L2/L3)를 얹는 컨트롤 평면
* **ML2/OVN**: Neutron과 OVN을 연결
* **ovn-controller**: OVN의 네트워크 상태를 호스트의 OVS에 반영


OVN 도입에 따른 Neutron Agent 구조 단순화
-----------------------------------------

기존 ML2/OVS 구조에서는 네트워크 기능별로 여러 Neutron Agent가
사용되었습니다.

.. code-block:: text

   Neutron Server
        |
        +---- OVS Agent
        |
        +---- L3 Agent
        |
        +---- DHCP Agent
        |
        v
       OVS

OVS Agent는 OVS 브리지와 Flow를 관리하고, L3 Agent와 DHCP Agent는
각각 라우팅과 DHCP 기능을 담당합니다.

네트워크 기능별로 Agent가 구성되기 때문에 여러 Agent의 상태와
통신을 함께 관리해야 합니다.

ML2/OVN에서는 OVN이 논리 네트워크 모델을 통해 주요 네트워크 기능을
처리하므로 구조가 다음과 같이 단순화됩니다.

.. code-block:: text

   Neutron Server
        |
      ML2/OVN
        |
        v
      OVN DB
        |
        v
   ovn-controller
        |
        v
       OVS

OVN은 논리적인 네트워크 객체로 관리하고, :code:`ovn-controller` 프로세스가
이를 각 호스트의 OVS 데이터 평면에 반영합니다.

이에 따라 기존의 OVS Agent, L3 Agent, DHCP Agent가 담당하던
주요 네트워크 기능을 OVN으로 통합할 수 있으며, Neutron의
Agent 중심 구조가 단순해집니다.

.. note::

   OVN을 사용한다고 해서 모든 Neutron Agent가 사라지는 것은 아닙니다.
   일부 기능에서는 여전히 Neutron Agent가 사용될 수 있습니다.
   따라서 OVN은 기존 Agent를 완전히 제거한다기보다, 핵심 네트워크
   기능을 OVN으로 이동하여 Agent 구조를 단순화한 것입니다.


더 읽을거리
-----------

* `OVN Features
  <https://docs.openstack.org/neutron/latest/admin/ovn/features.html>`_

* `OVN Documentation
  <https://docs.ovn.org/en/latest/>`_

* `OVN-Kubernetes
  <https://ovn-kubernetes.io/>`_

* `Open vSwitch Documentation
  <https://docs.openvswitch.org/en/latest/>`_

* `Neutron OVN Design
  <https://docs.openstack.org/neutron/latest/contributor/internals/ovn/index.html>`_
