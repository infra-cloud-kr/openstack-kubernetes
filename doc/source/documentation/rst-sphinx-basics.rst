====================
rST / Sphinx 기초
====================

본 프로젝트는 reStructuredText(rST)와 `Sphinx <https://www.sphinx-doc.org/>`_
로 문서를 작성합니다. 이 문서는 처음 기여하는 분을 위한 최소한의 기초를
정리합니다.


왜 rST/Sphinx 인가
==================

* OpenStack 문서 생태계의 표준 (:doc:`openstack-doc-conventions`)
* ``toctree`` 기반의 다중 페이지 구조화에 강함
* 교차 참조(cross-reference), 용어집(glossary), admonition 등 학습 경로형
  문서에 적합한 기능 제공

.. note::

   Kubernetes 공식 문서는 Hugo/Markdown 기반입니다. 두 생태계의 차이는
   :doc:`kubernetes-doc-conventions` 에서 다룹니다.


제목과 섹션
===========

제목은 밑줄(또는 위아래 줄)로 표현하며, 본 프로젝트 권장 순서는 다음과
같습니다.

.. code-block:: rst

   ======
   제목 1 (문서 제목)
   ======

   제목 2
   ======

   제목 3
   ------

   제목 4
   ~~~~~~

.. warning::

   한글(전각 문자)은 폭이 2로 계산되므로, 밑줄 길이를 제목보다 충분히 길게
   하세요. 밑줄이 짧으면 ``sphinx-build -W`` 에서 빌드가 실패합니다.


목록
====

.. code-block:: rst

   * 순서 없는 항목
   * 또 다른 항목

   #. 번호 매김 항목
   #. 자동으로 번호가 매겨짐


코드 블록
=========

.. code-block:: rst

   .. code-block:: console

      $ tox -e docs


교차 참조와 toctree
===================

다른 문서를 가리킬 때 ``:doc:`` 를 사용합니다.

.. code-block:: rst

   자세한 내용은 :doc:`../introduction/index` 를 참고하세요.

새 문서를 추가하면 상위 ``index.rst`` 의 ``toctree`` 에 반드시 등록합니다.

.. code-block:: rst

   .. toctree::
      :maxdepth: 1

      new-page


admonition (참고/경고)
======================

.. code-block:: rst

   .. note::

      참고할 내용입니다.

   .. warning::

      주의할 내용입니다.


빌드와 린트
===========

.. code-block:: console

   $ tox -e docs    # HTML 빌드 (경고를 오류로 처리)
   $ tox -e pep8    # doc8 로 rST 스타일 검사
