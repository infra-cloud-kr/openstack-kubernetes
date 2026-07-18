=====================
Kubernetes 핵심 개념
=====================

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


선언적(Declarative) 관리
========================

.. todo::

   원하는 상태(desired state) 선언과 컨트롤러의 조정(reconciliation loop)
   개념 설명 보강.


주요 오브젝트
=============

.. todo::

   Deployment / StatefulSet / Service / ConfigMap / Secret 등 주요 오브젝트와
   역할을 표로 정리.


자동화 3종
==========

.. todo::

   Self-healing / Rolling Update / Auto-scaling(HPA) 설명 보강.


CRD (Custom Resource Definition)
================================

.. todo::

   * Kubernetes API 확장 메커니즘으로서의 CRD 와, 이것이
     :doc:`bridging-concepts` 의 여러 통합 프로젝트(Magnum 드라이버,
     Metal3 ``BareMetalHost`` 등)의 공통 기반이 되는 점 설명 보강
   * kubectl 로 오브젝트를 조회/생성하는 기본 흐름 예시 추가
   * Operator 패턴(CRD + 컨트롤러)과의 연결 보강


실습 전 기본 명령
=================

.. todo::

   기본 오브젝트 조회 등 ``kubectl`` 명령 예시 보강.


더 읽을거리
===========

.. todo::

   참고 링크 보강.
