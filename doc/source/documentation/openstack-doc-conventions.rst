========================
OpenStack 문서 관례
========================

OpenStack 은 문서 기여에 대한 체계적인 가이드를 제공합니다. 본 프로젝트는
이 관례를 학습 모델로 삼습니다.

.. note::

   기여자 작업용 골격입니다. 아래 1차 출처를 직접 확인하며 핵심 규칙을
   요약·보강해 주세요.


핵심 출처
=========

* `OpenStack Documentation Contributor Guide
  <https://docs.openstack.org/doc-contrib-guide/>`_ — 문서 기여 워크플로우,
  스타일, rST 규칙, 빌드 방식


요약할 항목 (작업 가이드)
=========================

* 저장소 구조와 ``doc/source`` 관례
* RST 컨벤션(제목 레벨, 줄 길이, admonition)
* ``tox`` 기반 빌드와 린트 (본 프로젝트는 Zuul 대신 GitHub Actions 사용)
* 리뷰 프로세스 (본 프로젝트는 Gerrit 대신 GitHub PR 사용)


본 프로젝트와의 차이
====================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 항목
     - OpenStack 표준
     - 본 프로젝트
   * - 코드 리뷰
     - Gerrit
     - GitHub Pull Request
   * - CI
     - Zuul
     - GitHub Actions
   * - 빌드 도구
     - tox
     - tox (동일)
   * - 마크업
     - reStructuredText
     - reStructuredText (동일)
