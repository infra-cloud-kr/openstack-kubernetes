=========================
Kubernetes 문서 관례
=========================

Kubernetes 공식 문서는 OpenStack 과 달리 `Hugo <https://gohugo.io/>`_ 와
Markdown 기반입니다. 본 프로젝트는 rST/Sphinx 로 작성하지만, Kubernetes
문서 기여까지 연결하려면 이 차이를 이해해야 합니다.

.. note::

   기여자 작업용 골격입니다. Kubernetes 문서 기여 가이드를 확인하며
   보강해 주세요.


핵심 출처
=========

* Kubernetes Documentation (website) — https://kubernetes.io/docs/
* Contribute to Kubernetes docs —
  https://kubernetes.io/docs/contribute/


OpenStack 방식과의 차이
=======================

.. list-table::
   :header-rows: 1
   :widths: 25 37 38

   * - 항목
     - OpenStack
     - Kubernetes
   * - 마크업
     - reStructuredText
     - Markdown
   * - 정적 사이트 생성기
     - Sphinx
     - Hugo
   * - 현지화(l10n)
     - i18n 팀 + (Weblate 전환)
     - 언어별 디렉터리 + SIG Docs Localization
   * - 리뷰
     - Gerrit (대다수)
     - GitHub PR


왜 둘 다 알아야 하는가
======================

두 생태계의 문서화 방식을 모두 경험하면, 같은 "오픈소스 문서 기여" 라도
도구·관례가 어떻게 다른지 체득할 수 있습니다. 이는 번역
작업(:doc:`../translation-i18n/index`)에서 특히 유용합니다.
