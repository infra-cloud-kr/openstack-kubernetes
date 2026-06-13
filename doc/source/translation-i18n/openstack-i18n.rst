==============
OpenStack i18n
==============

OpenStack 의 국제화는 **i18n SIG** 가 주도합니다
(:doc:`../introduction/history-and-sigs` 참고). 이 문서는 OpenStack 번역
워크플로우와 본 프로젝트의 한글화 작업을 연결합니다.

.. note::

   기여자 작업용 골격입니다. i18n SIG 의 현행 도구·프로세스를 확인하며
   보강해 주세요.


핵심 출처
=========

* OpenStack I18n Contributor Guide —
  https://docs.openstack.org/i18n/


번역 파이프라인 개요
====================

* 소스 문자열 추출 (gettext / ``.po`` / ``.pot``)
* 번역 플랫폼에서 번역 (:doc:`weblate`)
* 번역 결과 반영 및 빌드


Sphinx gettext 흐름
===================

Sphinx 는 ``gettext`` 빌더를 통해 번역 가능한 메시지를 추출할 수 있습니다.

.. code-block:: console

   $ sphinx-build -b gettext doc/source doc/build/gettext

추출된 ``.pot`` 을 번역 플랫폼에 올리고, 번역된 ``.po`` 를 받아 언어별 문서를
빌드하는 흐름을 정리합니다.


Weblate 마이그레이션
====================

OpenStack 커뮤니티의 번역 플랫폼 전환(예: Zanata → Weblate) 맥락과 본
프로젝트의 적용 방안은 :doc:`weblate` 에서 다룹니다.
