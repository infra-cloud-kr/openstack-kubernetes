===================
Weblate 번역 가이드
===================

이 문서는 **멘토링 참가자(멘티)** 가 번역 플랫폼
`Weblate <https://translate.openinfra.kr>`_ 에서 계정을 발급받고
문서를 번역하는 과정을 안내합니다.

본 프로젝트 문서는 **한국어가 원문**\이며, Weblate 를 통해
**영어로 번역**\됩니다. 번역한 내용은 자동으로 GitHub Pull Request
로 만들어지고, 검토 후 병합되면 영어 사이트(``/en/``)에 반영됩니다.

동작 원리(파이프라인)는 :doc:`weblate` 를 참고하세요.


한눈에 보는 흐름
================

.. code-block:: text

   계정 생성 -> 이메일 인증 -> 로그인
        -> 프로젝트(openstack-kubernetes) -> 컴포넌트(docs)
        -> English 선택 -> 한 문장씩 번역 & 저장
        -> (Weblate 가 자동으로) GitHub PR 생성
        -> 멘토 검토 후 병합 -> 영어 사이트 반영

* 번역 사이트: https://translate.openinfra.kr
* 대상 프로젝트: ``openstack-kubernetes`` / ``docs``
* 번역 언어: 한국어(원문) → English(영어)


1. 계정 만들기
==============

#. https://translate.openinfra.kr/accounts/register/ 에 접속합니다.
#. 다음을 입력합니다.

   * **E-mail**: 인증 메일을 받을 본인 이메일
   * **Username**: 로그인용 사용자 이름(영문)
   * **Full name**: 표시될 이름(기여자 이름으로 기록)
   * **I'm not a robot**: 사람 확인(캡차)

#. **Register** 버튼을 누릅니다.

.. figure:: /_static/img/weblate/register.png
   :alt: Weblate 회원가입 화면
   :width: 100%

   회원가입 화면.

.. note::

   가입 후 입력한 이메일로 **인증 메일**\이 옵니다. 메일의 링크를
   눌러야 계정이 활성화됩니다. 안 보이면 스팸함도 확인하세요.


2. 로그인
=========

이메일 인증을 마쳤다면
https://translate.openinfra.kr/accounts/login/ 에서 로그인합니다.

.. figure:: /_static/img/weblate/login.png
   :alt: Weblate 로그인 화면
   :width: 100%

   로그인 화면.


3. 번역할 문서 찾기
===================

#. 상단 **Projects** → **openstack-kubernetes** 를 선택합니다.

   .. figure:: /_static/img/weblate/project.png
      :alt: openstack-kubernetes 프로젝트 화면
      :width: 100%

      프로젝트 화면.

#. **docs** 컴포넌트 → 언어 목록에서 **English** 를 선택하면 번역
   현황이 나타납니다.

   .. figure:: /_static/img/weblate/language.png
      :alt: English 번역 현황 화면
      :width: 100%

      번역 현황. **Translate** 로 편집기에 들어갑니다. *Unfinished
      strings* 를 누르면 미번역 문장만 모아 볼 수 있습니다.

.. tip::

   처음에는 **Unfinished strings → Translate** 로 시작하면 번역이
   필요한 문장만 순서대로 보여 줍니다.


4. 번역 편집기 사용법
=====================

.. figure:: /_static/img/weblate/editor.png
   :alt: Weblate 번역 편집기
   :width: 100%

   번역 편집기. 위에 한국어 원문, 아래에 영어 입력칸이 있습니다.

* **Korean** (위): 번역할 원문(한국어)
* **English** (아래): 영어 번역을 입력
* **Glossary** (오른쪽): 용어집(등록된 통일 번역어)
* **Nearby strings** (아래): 앞뒤 문맥 문장

저장 버튼:

* **Save and continue**: 저장하고 다음 문장으로 (가장 많이 사용)
* **Save and stay**: 저장하고 현재 문장에 머무름
* **Suggest**: 확정 대신 제안만 남김
* **Skip**: 저장 없이 건너뜀

.. important::

   번역을 저장하려면 **로그인**\이 되어 있어야 합니다. 비로그인
   상태에서는 "Sign in to save translations." 안내가 보입니다.


5. 마크업 보존 규칙
===================

원문에는 reStructuredText(RST) 서식이 섞여 있습니다. **서식 기호는
그대로 두고 글자만 번역**\해야 문서가 깨지지 않습니다.

.. code-block:: rst

   원문 :  **OpenStack** 과 Kubernetes
   번역 :  **OpenStack** and Kubernetes

.. code-block:: rst

   원문 :  `공식 문서 <https://docs.openstack.org/>`_ 참고
   번역 :  See the `official docs <https://docs.openstack.org/>`_

.. warning::

   * 별표(``*``), 백틱, 밑줄(``_``) 같은 서식 기호를 지우거나
     추가하지 마세요.
   * URL, 제품명(OpenStack, Kubernetes 등)은 번역하지 않습니다.
   * 문제가 있으면 Weblate 가 **Checks** 경고로 알려 줍니다.


6. 내 번역은 어떻게 반영되나요?
===============================

저장한 번역은 다음 과정을 거쳐 사이트에 반영됩니다. **이 과정은
자동**\이므로 번역가가 Git 을 직접 다룰 필요는 없습니다.

#. Weblate 가 번역을 모아 GitHub 로 **Pull Request** 를 생성/갱신
#. 멘토(메인테이너)가 PR 을 검토하고 병합
#. GitHub Actions 가 영어 문서를 빌드/배포

.. note::

   번역되지 않은 문장은 영어 사이트에서 원문(한국어)으로
   표시되며, 번역이 쌓일수록 영어로 채워집니다.


도움이 필요하면
===============

* 막히는 부분은 **멘토에게 문의**\하세요.
* Weblate 사용법:
  `Translating using Weblate
  <https://docs.weblate.org/en/latest/user/translating.html>`_
