================================================
두 한글화 공동체의 만남: I18n SIG 와 SIG Docs
================================================

:doc:`../introduction/history-and-sigs` 에서 살펴본 것처럼, OpenStack 과
Kubernetes 두 커뮤니티는 기술 통합을 위해 SIG(Special Interest Group)라는
형태로 공식적으로 만났습니다. 흥미롭게도 **문서 한글화** 영역에서도 같은
구도가 나타납니다. 두 프로젝트는 각각 번역·현지화를 책임지는 공동체를 두고
있으며, 본 프로젝트의 한글화 작업은 이 두 공동체가 만나는 지점에 서 있습니다.

* **OpenStack** — :doc:`openstack-i18n` 에서 다루는 **I18n SIG**
* **Kubernetes** — :doc:`kubernetes-localization` 에서 다루는
  **SIG Docs 의 현지화(localization) 하위 프로젝트**

.. note::

   이 문서는 두 공동체의 구조를 나란히 비교하는 도입부 골격입니다. 각
   공동체의 상세 워크플로우는 위에 링크된 개별 문서에서, 정확한 거버넌스
   현황(역할 임명, 현행 도구)은 1차 출처를 확인하며 보강해 주세요.


OpenStack 측: I18n SIG
======================

OpenStack 의 국제화는 **I18n SIG** 가 담당합니다. 언어별 번역팀(language
team)을 중심으로 운영되며, 팀 안에는 번역가(translator), 리뷰어(reviewer),
코디네이터(coordinator) 같은 역할이 정의되어 있습니다. 한국어(``ko_KR``)
번역팀도 그중 하나입니다.

번역 플랫폼은 역사적으로 Zanata 를 사용해 왔으며, 커뮤니티 차원에서 Weblate
로의 이행이 진행되어 왔습니다 (:doc:`weblate`). 자세한 내용은
:doc:`openstack-i18n` 을 참고하세요.


Kubernetes 측: SIG Docs 현지화 하위 프로젝트
============================================

Kubernetes 의 문서 현지화는 **SIG Docs** 산하의 현지화(localization) 하위
프로젝트가 담당합니다. 언어별로 GitHub 팀과 ``OWNERS`` 파일, 그리고
``language/ko`` 같은 라벨로 조직됩니다. 한국어(``ko``) 현지화 팀 역시 이
구조를 따릅니다.

OpenStack 과 달리 ``.po`` 메시지 번역이 아니라 언어별 디렉터리
(``/content/ko/``)에 Markdown 문서를 복제·번역하는 방식이며, 리뷰는 GitHub
PR 중심입니다. 자세한 내용은 :doc:`kubernetes-localization` 을 참고하세요.


나란히 비교
===========

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 항목
     - OpenStack I18n
     - Kubernetes SIG Docs 현지화
   * - 조직 형태
     - I18n SIG
     - SIG Docs 의 현지화 하위 프로젝트
   * - 한국어 단위
     - ``ko_KR`` 번역팀
     - ``ko`` 현지화 팀 (``language/ko`` 라벨)
   * - 번역 단위
     - gettext ``.po`` 메시지
     - 언어별 Markdown 파일 (``/content/ko/``)
   * - 도구/플랫폼
     - 번역 플랫폼 (Zanata → Weblate)
     - GitHub (``OWNERS`` 파일, Prow)
   * - 리뷰 방식
     - 플랫폼 + 언어팀 리뷰
     - GitHub PR (owners/reviewers)


본 프로젝트의 위치
==================

본 프로젝트는 이 두 공동체의 한글화 흐름을 모두 경험하는 것을 지향합니다.
서로 다른 두 방식(메시지 기반 번역 vs 파일 기반 현지화)을 함께 다뤄봄으로써,
같은 "한글화" 라도 프로젝트마다 도구·조직·리뷰 문화가 어떻게 다른지 체득할 수
있습니다. 이는 :doc:`../documentation/kubernetes-doc-conventions` 에서 정리한
문서화 방식의 차이와도 직접 이어집니다.
