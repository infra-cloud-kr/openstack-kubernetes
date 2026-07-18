================================================
OpenStack & Kubernetes 운영 문서화 및 국제화
================================================

본 프로젝트는 인프라를 위한 두 대표 글로벌 오픈소스 프로젝트인
**Kubernetes(쿠버네티스)** 와 **OpenStack(오픈스택)** 을 설치·운영하는 방법 및
모범 사례를 문서화하고, 이와 관련한 글로벌 공식 기술 문서의 한글 번역 및
국제화를 위한 인프라 개선에 기여하는 것을 목표로 합니다.

이 문서는 "직접 써본 사람이 쓴 한국어 가이드" 를 지향합니다. 두 기술을 직접
구축·운영해 본 경험을 바탕으로 설치·운영·모범 사례를 문서화하고, 관련 공식
문서를 한글화하는 것을 목표로 합니다.

.. note::

   이 저장소는 OpenStack 문서 생태계의 관례를 따라 Sphinx 와
   reStructuredText(rST) 로 작성되며, ``tox`` 로 빌드하고 GitHub Actions 로
   렌더링을 검증합니다.

.. note::

   현재 문서는 초기 골격 단계입니다. 각 섹션의 본문은 추후 단계적으로
   보완할 예정입니다 (각 문서의 ``note``/TODO 참고).


목차
====

.. toctree::
   :maxdepth: 2
   :caption: 소개

   introduction/index

.. toctree::
   :maxdepth: 2
   :caption: 기초 개념

   foundations/index

.. toctree::
   :maxdepth: 2
   :caption: 통합 패턴

   integration-patterns

.. toctree::
   :maxdepth: 2
   :caption: 실습

   labs/index

.. toctree::
   :maxdepth: 2
   :caption: 기여

   contributing

.. toctree::
   :maxdepth: 1
   :caption: 참고

   glossary


색인
====

* :ref:`genindex`
* :ref:`search`
