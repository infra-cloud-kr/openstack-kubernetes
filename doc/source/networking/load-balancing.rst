========================
로드 밸런싱 (Octavia)
========================

Octavia 는 OpenStack 의 로드 밸런싱(LBaaS) 서비스입니다. 이 문서는 서비스
자체의 개념을 다루며, Kubernetes ``Service`` 의 백엔드로 쓰는 관점은
:doc:`../kubernetes-on-openstack/octavia-load-balancer` 에서 다룹니다.


핵심 리소스 개념
================

Octavia 는 로드밸런서, 리스너, 풀, 멤버, 헬스 모니터라는 다섯 가지 리소스로
구성됩니다. 각 리소스는 트래픽이 흘러가는 순서대로 계층을 이룹니다.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 리소스
     - 역할
   * - 로드밸런서 (Load Balancer)
     - 가상 IP(VIP)를 할당받는 최상위 리소스. 하나 이상의 리스너를 가집니다.
   * - 리스너 (Listener)
     - 로드밸런서가 특정 포트·프로토콜(HTTP, HTTPS, TCP 등)로 들어오는
       요청을 받는 지점입니다. 하나의 풀과 연결됩니다.
   * - 풀 (Pool)
     - 트래픽을 분산할 백엔드 멤버들의 집합과 분산 알고리즘
       (라운드 로빈, 최소 연결 등)을 정의합니다.
   * - 멤버 (Member)
     - 실제로 트래픽을 처리하는 백엔드 서버(IP·포트)입니다. 풀에 여러
       멤버를 등록할 수 있습니다.
   * - 헬스 모니터 (Health Monitor)
     - 풀에 속한 멤버의 상태를 주기적으로 점검하고, 응답하지 않는 멤버를
       분산 대상에서 자동으로 제외합니다.

트래픽은 다음 순서로 흘러갑니다.

.. code-block:: text

   클라이언트 요청
   └─ 로드밸런서 (VIP)
      └─ 리스너 (포트·프로토콜)
         └─ 풀 (분산 알고리즘)
            ├─ 멤버 1 ─┐
            ├─ 멤버 2 ─┼─ 헬스 모니터가 상태 점검
            └─ 멤버 3 ─┘

헬스 모니터는 풀에 소속되어 각 멤버의 상태를 점검하며, 트래픽 경로 자체에는
포함되지 않습니다. 대신 점검 결과에 따라 풀이 특정 멤버로의 분산 여부를
결정합니다.


amphora 드라이버와 OVN Octavia 드라이버
========================================

Octavia 는 로드밸런서를 실제로 어떻게 구현할지 여러 드라이버(provider)로
선택할 수 있습니다. 그중 가장 널리 쓰이는 두 드라이버는 구조가 크게
다릅니다.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 구분
     - amphora 드라이버
     - OVN Octavia 드라이버
   * - 구현 방식
     - 로드밸런서마다 전용 가상 머신(amphora)을 생성하고, 그 안에서
       HAProxy 가 실제 분산을 처리합니다.
     - 별도 VM 없이 OVN(Open Virtual Network)의 로드 밸런싱 기능을
       그대로 활용합니다.
   * - 리소스 사용
     - 로드밸런서마다 VM 을 띄우므로 메모리·CPU 오버헤드가 있습니다.
     - 추가 VM 이 없어 오버헤드가 낮습니다.
   * - 기능 범위
     - L7 정책, TLS 종료 등 HAProxy 가 지원하는 기능을 폭넓게 지원합니다.
     - 지원 기능이 amphora 드라이버보다 제한적입니다(L7 정책 등 일부
       미지원).
   * - 전제 조건
     - 별도 네트워크 백엔드에 의존하지 않습니다.
     - Neutron 의 SDN 백엔드가 OVN 이어야 사용할 수 있습니다
       (:doc:`../networking/ovn-ovs` 참고).

openstack-helm 배포에서는 기본값으로 amphora 드라이버를 사용하며, OVN
드라이버는 Neutron 백엔드가 OVN 으로 구성된 환경에서 선택적으로 활성화할 수
있습니다.


더 읽을거리
===========

* `Octavia 프로젝트 공식 문서 <https://docs.openstack.org/octavia/latest/>`_
* `Octavia OVN provider driver 문서
  <https://docs.openstack.org/octavia/latest/admin/providers/ovn.html>`_
* :doc:`../kubernetes-on-openstack/octavia-load-balancer` — Kubernetes
  ``Service type=LoadBalancer`` 가 Octavia 를 백엔드로 사용하는 관점
