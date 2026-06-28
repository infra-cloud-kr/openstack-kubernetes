=======
Weblate
=======

`Weblate <https://weblate.org/>`_ 는 웹 기반 번역 플랫폼입니다.
본 프로젝트의 한글 문서는 한국어를 원문으로 하고, Weblate 를 통해
영어로 번역됩니다.

* 번역 인스턴스: https://translate.openinfra.kr
* 프로젝트 / 컴포넌트: ``openstack-kubernetes`` / ``docs``
* 원문 언어: 한국어(``ko``) → 번역 언어: 영어(``en``)

실제 번역하는 방법은 :doc:`translation-guide` 를 참고하세요.
이 문서는 **번역이 자동으로 동기화되는 구조**\를 설명합니다.


전체 흐름
=========

.. figure:: /_static/img/weblate/pipeline.svg
   :alt: GitHub 와 Weblate 사이의 양방향 번역 파이프라인
   :width: 100%

   원문/문자열은 GitHub → Weblate(①)로, 번역 결과는
   Weblate → GitHub(②)로 흐릅니다.


핵심: Weblate 는 ``.po`` 를 읽고 씁니다
=======================================

Weblate 는 RST 원문을 직접 다루지 않습니다. Sphinx 문서는 gettext
방식으로 번역되며, 번역 단위는 ``.po`` 파일입니다.

.. code-block:: text

   doc/source/**/*.rst (한국어 원문)
        |  Sphinx 로 추출 (tox -e update-po)
        v
   doc/source/locales/en/LC_MESSAGES/docs.po   <- Weblate 가 읽고 씀
        |  Sphinx 빌드 (-D language=en)
        v
   영어 HTML (/en/)

* 번역 대상 문자열은 원문에서 추출되어 ``docs.po`` 의 ``msgid`` 가
  됩니다.
* 번역 결과는 ``docs.po`` 의 ``msgstr`` 에 저장됩니다.
* 그래서 원문이 바뀌면 ``.po`` 를 다시 생성해야 새 문장이 Weblate
  에 나타납니다(아래 ① 자동화).

.. note::

   ``conf.py`` 에서 ``gettext_compact = 'docs'`` 로 설정해 모든
   문서를 하나의 ``docs.po`` 로 합칩니다. 덕분에 새 ``.rst`` 문서를
   추가해도 그 문장이 같은 카탈로그에 들어가 Weblate 컴포넌트
   하나가 자동으로 포착합니다.


① GitHub → Weblate (원문/문자열 반영)
=====================================

저장소 원문이 바뀌면 Weblate 에 반영됩니다. 두 단계로 동작합니다.

1단계 — 카탈로그 자동 재생성 (GitHub Actions)
---------------------------------------------

``doc/source/**.rst`` 또는 ``conf.py`` 가 ``main`` 에 들어오면
워크플로우 ``.github/workflows/i18n-sync.yml`` 이 실행됩니다.

.. code-block:: text

   tox -e update-po     # .pot 추출 + docs.po 갱신(기존 번역 보존)
   -> 변경이 있으면 docs.po 를 자동 커밋

``sphinx-intl update`` 는 내부적으로 ``msgmerge`` 를 수행하여 기존
번역은 유지하면서 새 문장 추가/삭제/변경을 처리합니다.

2단계 — Weblate 가 변경을 받아옴 (Webhook)
------------------------------------------

저장소의 Webhook 이 push 때마다 Weblate 알림 엔드포인트로 신호를
보냅니다.

.. code-block:: text

   GitHub(push) --POST--> translate.openinfra.kr/hooks/github/
                          -> Weblate 가 pull -> 새 문자열 노출

* 이 엔드포인트는 인증이 필요 없습니다. Weblate 는 payload 의
  저장소를 기존 컴포넌트와 대조한 뒤, 컴포넌트에 등록된 신뢰된
  URL 에서만 pull 합니다.
* 저장소가 공개라 Weblate 는 익명으로 읽습니다.


② Weblate → GitHub (번역 결과 반영)
===================================

번역가가 저장한 번역이 다시 저장소로 돌아갑니다.

.. code-block:: text

   Weblate 에서 번역 저장
        v
   Weblate 가 docs.po 커밋 (지연 커밋: 일정 시간/분량마다 묶음)
        v
   weblate-translations 브랜치로 push   (인증: GitHub PAT)
        v
   Pull Request 자동 생성/갱신
        v
   메인테이너 리뷰 후 머지
        v
   GitHub Actions 가 영어 문서 빌드 -> 배포 (/en/)

* Weblate 가 push/PR 하려면 쓰기 권한 인증이 필요하며, 서버
  환경변수의 개인 액세스 토큰(PAT)을 사용합니다.
* 번역은 묶음(지연 커밋)으로 처리되어 하나의 PR 이 점진적으로
  갱신됩니다.


인증 정리 (방향별)
==================

.. list-table::
   :header-rows: 1
   :widths: 52 26 22

   * - 동작
     - 인증
     - 비고
   * - GitHub → Weblate (Webhook)
     - 불필요
     - 공개 엔드포인트
   * - Weblate 가 저장소 읽기(pull)
     - 불필요
     - 저장소 공개
   * - Weblate → GitHub (push/PR)
     - PAT 필요
     - 서버 환경변수
   * - Actions 의 카탈로그 커밋
     - ``GITHUB_TOKEN``
     - 별도 시크릿 없음


컴포넌트 설정 요약
==================

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - 항목
     - 값
   * - 원문 언어
     - 한국어 (``ko``)
   * - 번역 언어
     - 영어 (``en``)
   * - 파일 형식
     - gettext PO (bilingual)
   * - File mask
     - ``doc/source/locales/*/LC_MESSAGES/docs.po``
   * - 버전 관리
     - ``github`` (PR 방식), merge: rebase
   * - Push 브랜치
     - ``weblate-translations``


메인테이너 메모
===============

.. note::

   * 원문을 바꿨는데 Weblate 에 안 보이면, ①의 카탈로그 재생성
     Action 이 돌아 ``docs.po`` 가 갱신됐는지, Webhook 이 전달됐는지
     확인합니다.
   * filemask 등을 바꾼 뒤 재스캔이 안 되면(이미 파싱됨으로 스킵),
     서버에서 ``weblate loadpo --force --foreground
     openstack-kubernetes/docs`` 로 강제 재로딩합니다.
   * 로컬 미반영 커밋과 원격이 어긋나면 Weblate 의 *Repository* 에서
     ``reset`` 으로 원격 상태에 맞춥니다.
