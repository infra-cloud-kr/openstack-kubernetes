# -*- coding: utf-8 -*-
#
# Sphinx 빌드 설정 파일.
#
# 이 파일은 OpenStack 문서 저장소의 conf.py 관례를 참고하되,
# 우선 외부 의존성이 없는 기본 theme(alabaster)로 단순하게 시작합니다.
#
# 전체 설정 항목은 다음을 참고하세요:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- 프로젝트 정보 -----------------------------------------------------------

project = 'OpenStack & Kubernetes 한글 문서화 프로젝트'
copyright = '2026, infra-cloud-kr contributors'
author = 'infra-cloud-kr contributors'

# -- 일반 설정 ---------------------------------------------------------------

extensions = [
    'sphinx.ext.todo',
]

# 소스 파일의 기본 언어 및 인코딩.
language = 'ko'

# 문서 최상위(root) 문서.
root_doc = 'index'

# 빌드에서 제외할 파일/디렉터리 패턴.
exclude_patterns = []

# -- 국제화 (i18n) -----------------------------------------------------------
# 번역 파일(.po) 위치. Weblate 가 이 디렉터리의 .po 를 읽고 씁니다.
locale_dirs = ['locales/']
# 모든 문서를 단일 카탈로그(docs.po)로 합칩니다. 새 문서를 추가해도
# 그 문자열이 같은 카탈로그에 들어가 Weblate 컴포넌트 하나가 포착합니다.
gettext_compact = 'docs'

# todo 지시문을 출력에 표시.
todo_include_todos = True

# -- HTML 출력 옵션 ----------------------------------------------------------

# 외부 의존성 없이 동작하는 Sphinx 기본 내장 theme.
# OpenStack 공식 문서 테마(openstackdocstheme)로 전환하려면
# doc/requirements.txt 에서 해당 패키지를 설치한 뒤 아래를 교체하세요.
html_theme = 'alabaster'

html_title = 'OpenStack & Kubernetes 한글 문서화 프로젝트'

# -- 링크 검사 (linkcheck) ---------------------------------------------------
# ``tox -e linkcheck`` 로 외부 링크의 유효성을 확인합니다.
# 리다이렉트는 문서에서 최종 URL 로 바로 적는 것을 원칙으로 합니다.

# 봇 접근을 차단해 403 을 돌려주지만 사람은 정상적으로 볼 수 있는 링크.
linkcheck_ignore = [
    r'https://www\.netapp\.com/learn/.*',
]

# 링크 검사 시 동시 요청 수와 재시도 (CI 에서의 산발적 실패를 줄입니다).
linkcheck_workers = 5
linkcheck_timeout = 15
linkcheck_retries = 2

# 외부 공식 문서로의 교차 참조가 필요해지면 ``sphinx.ext.intersphinx`` 를
# extensions 에 추가하고 여기에 intersphinx_mapping 을 정의하세요.
