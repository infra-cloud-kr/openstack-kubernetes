===============================================
openstack-helm 으로 구축한 환경의 네트워크 구조
===============================================

개요
====

해당 문서는 ``openstack-on-kubernetes-terraform`` 을 사용하여 처음 OpenStack 을
설치한 사용자가 전체 네트워크 구조의 뼈대를 잡을 수 있도록 돕기 위한 목적으로
작성되었습니다.

`openstack-on-kubernetes-terraform`_ 에 작성된 단계에 따라 OpenStack 서비스를
Kubernetes 로 배포한 환경을 전제하고 있으며,
``make init → make up → make ready → make osh-deploy → make osh-vm`` 을
완료한 시점을 기준으로 네트워크 구조와 주요 구성 요소의 역할을 설명합니다.

.. _openstack-on-kubernetes-terraform:
   https://github.com/infra-cloud-kr/openstack-on-kubernetes-terraform

설치 절차보다는 각 네트워크가 어디에 존재하고, 무엇과 연결되며,
어떤 구성 요소가 이를 관리하는지에 집중하여 작성되었습니다.
CNI 와 Neutron 이 한 노드에서 공존하는 구조는
:doc:`cni-and-neutron` 에서 개념으로 다룹니다.

또한 openstack-helm 을 통해 구축된 인프라의 전체 네트워크를
총 다섯 개의 하위 네트워크로 나누어서 구분하였습니다.

.. code-block:: text

   배포 결과로 생성된 네트워크 인프라
   │
   ├── AWS Network
   ├── EC2 Host Network
   ├── Kubernetes Network
   ├── OpenStack Service Network
   └── Neutron Tenant VM Network

전체 네트워크
=============

전체 네트워크의 구조를 간략하게 나타내면 다음과 같습니다.

.. code-block:: text

   AWS VPC
   └── EC2 Host
       ├── Kubernetes Network
       │   └── OpenStack Service Pods
       │       ├── Nova
       │       ├── Keystone
       │       └── ...
       │
       └── Open vSwitch Data Plane
           └── Neutron Tenant Network
               └── test-vm

하나의 EC2 Host 안에는 OpenStack 서비스를 실행하는 Kubernetes Network 와
Tenant VM 의 패킷을 전달하는 Open vSwitch Data Plane 이 함께 구성됩니다.

**OpenStack API 를 호출하는 요청** 은 Kubernetes Service 를 통해 Nova,
Keystone 등의 OpenStack Service Pod 로 전달됩니다.
OpenStack 서비스 사이의 API 요청과 내부 메시지도 Kubernetes Network 를
통해 전달됩니다.

반면 Tenant VM 으로 향하거나 Tenant VM 에서 나오는 패킷은
OpenStack API Pod 를 통과하지 않습니다.
Neutron 이 정의한 Network 와 Port 상태가 Open vSwitch 에 반영되면,
``test-vm`` 이 송수신하는 패킷은 Open vSwitch Data Plane 을 통해
Neutron Tenant Network 내부로 전달됩니다.

AWS Network
===========

OpenStack 과 Kubernetes 가 실행되는 EC2 는 ``10.0.0.0/16`` VPC 의
``10.0.1.0/24`` Public Subnet 에 배치됩니다. EC2 의 Primary ENI 에는
해당 Subnet 의 Private IPv4 가 할당됩니다.

AWS Cloud 는 사용자가 구성하는 VPC 영역과 AWS 가 운영하는 관리형 서비스
영역으로 구분할 수 있습니다.

.. code-block:: text

   AWS Cloud
   ├── 사용자 VPC (10.0.0.0/16)
   │   ├── Internet Gateway
   │   └── Public Subnet (10.0.1.0/24)
   │       └── EC2 Primary ENI
   │           └── Private IPv4: 10.0.1.x
   │
   └── AWS 관리형 서비스
       └── AWS Systems Manager

Public Subnet 의 Route Table 에는
``0.0.0.0/0 → Internet Gateway`` 경로가 설정됩니다.
EC2 는 이 경로를 통해 패키지와 컨테이너 이미지를 내려받습니다.

본 배포에서 EC2 의 Security Group 은 **아웃바운드 통신만 허용** 하고 있으며
인바운드 통신은 허용하고 있지 않습니다. 따라서 사용자는 EC2 의
Public IPv4 나 SSH 를 통해 직접 접속하지 않습니다.

EC2 내부의 SSM Agent 가 AWS Systems Manager 에 아웃바운드 관리 채널을
생성하며, ``make ssm`` 과 OpenStack 배포 명령도 이 채널을 통해 전달됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 구성 요소
     - 역할
   * - VPC
     - EC2 가 배치되는 10.0.0.0/16 AWS 가상 네트워크
   * - Public Subnet
     - EC2 의 Primary ENI 가 배치되는 10.0.1.0/24 주소 대역
   * - Internet Gateway
     - Public Subnet 과 외부 네트워크 사이의 통신 경로
   * - Primary ENI
     - AWS Network 와 EC2 Host Network 간 연결
   * - Security Group
     - 인바운드 차단 및 모든 아웃바운드 통신 허용
   * - AWS Systems Manager
     - SSH 없는 EC2 명령 전달 및 관리 세션 생성

EC2 Host Network
================

EC2 Host Network 는 AWS Network, Kubernetes Network 및
Neutron Tenant VM Network 가 함께 존재하는 호스트 내부 네트워크입니다.

본 프로젝트에서는 하나의 EC2 가 ``Kubernetes Node`` 이자
``OpenStack Compute Host`` 역할을 수행합니다.

.. code-block:: text

   EC2 Instance
   ├── Linux Network Stack
   │   ├── Primary Network Interface
   │   │   └── Private IPv4: 10.0.1.x
   │   ├── br_netfilter
   │   └── IPv4 Forwarding
   │
   └── Open vSwitch Data Plane
       ├── br-int
       │   └── VM Port와 Tenant Network 연결
       ├── br-tun
       │   └── VXLAN 처리
       └── br-ex
           └── provider1
               └── Linux Dummy Interface

``Primary Network Interface`` 는 AWS 의 Primary ENI 에 대응하며,
EC2 운영체제와 AWS VPC 를 연결합니다.

``Open vSwitch`` 는 여러 VM 이 같은 Tenant Network 에서 통신할 수 있도록
EC2 Host 안에 가상 스위치 구조를 만듭니다.
Neutron OVS Agent 는 Neutron 에 정의된 Network 와 Port 정보를 바탕으로
Open vSwitch 의 Bridge 와 연결 상태를 구성합니다.

``br-int`` 는 여러 VM 의 Virtual NIC 가 연결되는 중심 Bridge 입니다.
같은 Tenant Network 에 속한 VM 과 DHCP Port 사이의 패킷을 전달합니다.

``br-tun`` 은 서로 다른 Compute Host 사이에서 Tenant Network 의 패킷을
:term:`VXLAN` 으로 전달할 때 사용됩니다. 현재는 단일 Compute Host 환경이므로
실제 Host 간 VXLAN Tunnel 트래픽은 발생하지 않습니다.

``br-ex`` 는 VM 이 Provider Network 나 외부 네트워크로 접근할 때 사용하는
Bridge 입니다. 본 배포에서는 실제 외부 NIC 대신 ``provider1`` Dummy
Interface 가 연결되므로 AWS VPC 나 인터넷으로 이어지는 외부 경로는 구성되지
않습니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 구성 요소
     - 역할
   * - Primary Network Interface
     - AWS VPC 와 EC2 Host Network 간 연결
   * - Linux Network Stack
     - Host 의 Routing 및 패킷 전달 처리
   * - Neutron OVS Agent
     - Neutron Network 상태의 OVS Bridge·Port·Flow 구현
   * - br-int
     - VM Port 와 Neutron Tenant Network 간 연결
   * - br-tun
     - VXLAN Segment 및 다중 Compute Host 간 Tunnel 처리
   * - br-ex
     - Neutron Provider Network 의 Host 측 연결 지점
   * - provider1
     - 실제 외부 NIC 를 대신해 br-ex 에 연결된 Dummy Interface

``br_netfilter`` 와 ``net.ipv4.ip_forward = 1`` 은 별도의 Network Interface 가
아니라 Linux Kernel 의 패킷 처리 설정입니다.

.. code-block:: text

   br_netfilter
   └── Bridge를 통과하는 패킷에 Netfilter 규칙 적용

   net.ipv4.ip_forward = 1
   └── 서로 다른 Interface와 Network Namespace 사이의 패킷 전달 허용

Kubernetes Network
==================

Kubernetes Network 는 Node Communication, Pod Network, Service Network 라는
서로 다른 역할의 영역으로 나누어 이해할 수 있습니다.

Node Communication 은 Kubernetes Node 자체의 통신을 담당하고,
Pod Network 는 일반 Pod 에 독립된 IP 와 통신 환경을 제공합니다.
Service Network 는 여러 Pod 를 하나의 고정된 가상 주소로 연결합니다.

본 프로젝트에서는 하나의 EC2 가 단일 Kubernetes Node 로 사용되므로
Node 간 통신은 발생하지 않습니다.

.. code-block:: text

   Kubernetes Node
   (= EC2 Instance)
   │
   └── Kubernetes Network
       ├── Node Communication
       │   └── Node InternalIP: 10.0.1.x
       │
       ├── Pod Network
       │   ├── Pod CIDR: 192.168.0.0/16
       │   └── Pod Network Namespace
       │       └── eth0: 192.168.x.x
       │
       └── Service Network
           ├── Service CIDR: 10.96.0.0/12
           │   └── kubeadm 기본값
           └── ClusterIP
               └── Endpoint Pod IP로 전달

``Node Communication`` 에서는 EC2 의 Primary Private IPv4 인 ``10.0.1.x`` 가
Node InternalIP 로 사용됩니다. Kubernetes 전체를 대표하는 별도의
Network Interface 가 생성되는 것은 아닙니다.

``Pod Network`` 에서는 일반 Pod 에 독립된 Network Namespace 와 ``eth0`` 이
구성되고, ``192.168.0.0/16`` 범위에서 개별 IP 가 할당됩니다.
본 프로젝트에서는 :term:`Calico` CNI 가 Pod Network 를 구성합니다.

``Service Network`` 는 Pod IP 가 변경되더라도 동일한 주소로 접근할 수 있도록
ClusterIP 를 제공합니다. 본 프로젝트는 Service CIDR 을 별도로 지정하지
않으므로 kubeadm 기본값인 ``10.96.0.0/12`` 를 사용합니다.

``kube-proxy`` 는 ClusterIP 로 들어온 요청을 실제 Endpoint Pod IP 와 Port 로
전달하는 규칙을 구성합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 구성 요소
     - 역할
   * - Node InternalIP
     - Kubernetes 의 Node 식별 주소
   * - Primary Network Interface
     - Node InternalIP 의 기반이 되는 Private IPv4 보유 EC2 Host Interface
   * - Pod CIDR
     - 일반 Pod IP 할당을 위한 192.168.0.0/16 주소 범위
   * - Calico CNI
     - 일반 Pod 의 Network Namespace·Interface·IP·통신 경로 구성
   * - Pod eth0
     - 일반 Pod 의 기본 패킷 송수신 Network Interface
   * - Service CIDR
     - ClusterIP 할당을 위한 10.96.0.0/12 주소 범위(kubeadm 기본값)
   * - ClusterIP
     - 여러 Endpoint Pod 를 대표하는 고정 가상 주소
   * - kube-proxy
     - ClusterIP 요청의 Endpoint Pod 전달 규칙 구성

.. note::

   ClusterIP 는 특정 Network Interface 에 직접 할당되는 실제 IP 가 아닙니다.
   kube-proxy 가 전달 규칙을 구성하고, 실제 패킷 변환과 전달은
   Linux Kernel 이 수행합니다.


OpenStack Service Network
=========================

OpenStack Service Network 는 OpenStack API Service 와
Kubernetes Pod 위에 배포된 openstack Service 가 통신하는 네트워크 영역입니다.

.. code-block:: text

   Kubernetes Network
   └── Namespace: openstack
       ├── osc Pod
       │
       ├── Keystone Service
       │   └── Keystone API Pod
       │
       ├── Glance Service
       │   └── Glance API Pod
       │
       ├── Nova Service
       │   └── Nova API Pod
       │
       ├── Neutron Service
       │   └── Neutron Server Pod
       │
       └── ...

``openstack Namespace`` 는 OpenStack 관련 Kubernetes Resource 를
구분하고 관리하는 논리적 범위입니다.

각 OpenStack API 는 Kubernetes Service 를 통해 노출됩니다.
Service 는 고정된 DNS 이름과 ClusterIP 를 제공하며,
해당 Service 로 전달된 요청을 연결된 API Pod 로 전달합니다.

``osc`` Pod 는 Keystone, Glance, Nova 및 Neutron Service 에
API 요청을 보냅니다.

.. code-block:: text

   osc Pod
   └── OpenStack Service
       └── OpenStack API Pod

이 과정에서 Service 의 ClusterIP 로 전달된 요청은
Node 의 Linux Network Stack 에서 kube-proxy 가 구성한 전달 규칙에 따라
해당 Service 의 Endpoint Pod IP 로 변환됩니다.

변환된 패킷은 Kubernetes Pod Network 를 통해 대상 Pod 로 전달됩니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 구성 요소
     - 역할
   * - openstack Namespace
     - OpenStack 관련 Kubernetes Resource 의 논리적 관리 범위
   * - osc Pod
     - OpenStack API 요청을 보내는 Client Pod
   * - OpenStack Service
     - OpenStack API 접근을 위한 DNS 이름과 ClusterIP 제공
   * - OpenStack API Pod
     - Service 를 통해 전달된 OpenStack API 요청 처리

Neutron Tenant VM Network
=========================

Neutron Tenant VM Network 는 OpenStack VM 에 독립된 IP 와
Layer 2 통신 환경을 제공하는 Data Plane 네트워크입니다.

Tenant Network 는 OpenStack 사용자가 VM 을 연결하기 위해 생성하는
논리적인 가상 네트워크입니다.
같은 Tenant Network 에 연결된 VM 은 동일한 Layer 2 네트워크에 속하며,
다른 Network 와 분리된 환경에서 통신합니다.

Neutron Server 는 Network, Subnet 및 Port 정보를 관리하고,
Neutron Agent 는 해당 정보를 EC2 Host 의 네트워크 구조에 반영합니다.

본 환경의 ``demo-net``, ``demo-subnet`` 및 ``test-vm`` 은
VM 생성과 Tenant Network 의 동작을 확인하기 위한 테스트용 Resource 입니다.

이 절에서는 해당 구성을 기준으로 Tenant Network 의 구조와
VM 패킷 전달 경로를 설명합니다.

.. code-block:: text

   Neutron Tenant VM Network
   ├── demo-net
   │   └── demo-subnet
   │       ├── CIDR: 10.10.10.0/24
   │       ├── DHCP: Enabled
   │       └── Neutron Port
   │           ├── Fixed IP: 10.10.10.x
   │           └── test-vm Virtual NIC
   │
   └── VM Data Path

``demo-net`` 은 ``test-vm`` 이 연결되는 테스트용 Tenant Network 입니다.

Neutron Agent 가 Network 와 Port 정보를 EC2 Host 에 반영하면,
VM 패킷을 전달하기 위한 Open vSwitch Data Plane 이 구성됩니다.

``test-vm`` 은 Neutron Port 를 통해 ``demo-net`` 에 연결됩니다.
Neutron Port 에는 VM 에 할당된 Fixed IP 와 MAC Address 가 저장되며,
VM 과 Tenant Network 의 연결을 나타냅니다.

VM 의 Virtual NIC 는 EC2 Host 에 생성된 TAP Interface 와 연결됩니다.
TAP Interface 로 전달된 패킷은 ``qbr`` 와 ``qvb``·``qvo`` 를 거쳐
Open vSwitch 의 ``br-int`` 로 전달됩니다.

.. code-block:: text

   test-vm Virtual NIC
   └── TAP Interface
       └── qbr
           └── qvb / qvo
               └── br-int
                   └── demo-net의 다른 Port

이 경로는 VM 패킷에 Host Network 규칙을 적용한 뒤,
같은 Tenant Network 에 연결된 다른 Port 로 전달하기 위해 사용됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 구성 요소
     - 역할
   * - demo-net
     - VM 생성과 Tenant Network 동작 확인을 위한 테스트용 Network
   * - demo-subnet
     - 10.10.10.0/24 주소 범위와 DHCP 설정을 제공하는 테스트용 Subnet
   * - Neutron Port
     - VM 의 Fixed IP·MAC Address·Network 연결 정의
   * - TAP Interface
     - VM Virtual NIC 와 EC2 Host Network Data Plane 간 연결
   * - qbr·qvb·qvo
     - Host Network 규칙 적용 및 TAP Interface 와 br-int 사이의 연결 경로
   * - br-int
     - 같은 Tenant Network 에 연결된 Port 사이의 Layer 2 패킷 전달
   * - br-tun
     - VXLAN Segment 와 다중 Compute Host 간 Tunnel 처리
   * - DHCP Namespace
     - demo-subnet 에 연결된 VM 을 대상으로 DHCP 응답 제공

``demo-net`` 이 VXLAN Network 로 구성된 경우,
``br-tun`` 은 서로 다른 Compute Host 사이의 VXLAN Tunnel 처리에
사용됩니다.

현재는 단일 Compute Host 환경이므로
다른 Compute Host 로 전달되는 VXLAN Tunnel 트래픽은 발생하지 않습니다.

``br-ex`` 와 ``provider1`` 은 Provider Network 를 위한 Host 측 구성입니다.
현재 환경에는 External Network, Neutron Router 및 Floating IP 가 없으므로
``demo-net`` 과 ``br-ex`` 사이의 패킷 전달 경로는 구성되지 않습니다.

.. note::

   현재 ``test-vm`` 은 ``demo-net`` 내부 통신과 DHCP 를 사용할 수 있지만,
   Neutron Router 를 통한 외부 연결이 없으므로 AWS VPC 나 인터넷에는
   접근할 수 없습니다.
