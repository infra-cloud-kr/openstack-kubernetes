======
Magnum
======

`Magnum <https://docs.openstack.org/magnum/>`_ 은 OpenStack 에서 컨테이너
오케스트레이션 엔진(주로 Kubernetes)을 Container-as-a-Service 형태로 제공하는
프로젝트입니다.

.. note::

   기여자 작업용 골격입니다. 특히 Heat → CAPI 드라이버 전환을 정확히
   반영하여 보강해 주세요. 기존 한국어 자료 대부분이 Heat 기반이라
   outdated 상태입니다.


개요
====

* 클러스터 템플릿(cluster template) 기반 클러스터 프로비저닝
* Keystone 인증과 통합된 멀티테넌시
* OpenStack 사용자에게 익숙한 API/CLI 경험


드라이버 변화: Heat 에서 Cluster API 로
=======================================

* **과거**: Heat 기반 드라이버로 스택을 생성하여 클러스터를 프로비저닝
* **현재**: Cluster API(CAPI) 기반 드라이버로 무게중심 이동

.. warning::

   온라인의 많은 Magnum 튜토리얼이 Heat 기반 구조를 전제로 작성되어
   있습니다. 본 프로젝트에서 한글화 대상을 선정할 때는 CAPI 기반 최신
   문서를 우선 검토하세요. 자세한 역사적 맥락은
   :doc:`../introduction/history-and-sigs` 를 참고하세요.


참고
====

* Magnum 공식 문서 — https://docs.openstack.org/magnum/
