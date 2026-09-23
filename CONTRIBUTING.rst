==================
Contributing Guide
==================

Thank you for your interest in this project. Since one of its goals is to
learn the conventions of the OpenStack documentation ecosystem, the
contribution workflow also follows the approach of the `OpenStack
Documentation Contributor Guide
<https://docs.openstack.org/doc-contrib-guide/>`_. The one difference is that
code review and CI use **GitHub Pull Requests** and **GitHub Actions** instead
of Gerrit and Zuul.


Before you start
================

#. Fork this repository and clone it locally.
#. Install Python 3.10+ and `tox <https://tox.wiki/>`_.
#. Confirm that the documentation builds:

   .. code-block:: console

      $ tox -e docs


Workflow
========

#. **Find or open an issue**: Check whether an issue already exists for the
   work you want to do, and open one if needed to share your intent.
#. **Create a branch**: Branch from ``main``. Branch names in the form
   ``docs/<topic>`` or ``fix/<topic>`` are recommended.
#. **Write documentation**: Add or edit rST documents in the appropriate place
   under ``doc/source/``. When you add a new page, always register it in the
   parent ``index.rst`` ``toctree``.
#. **Build and lint locally**:

   .. code-block:: console

      $ tox -e docs
      $ tox -e pep8

#. **Commit**: A one-line summary (about 50 characters) followed by a body is
   recommended.
#. **Open a pull request**: Send a PR to ``main`` from your fork. GitHub
   Actions will automatically validate the documentation build.
#. **Address review feedback**: Update the PR to reflect reviewer feedback.


reStructuredText conventions
============================

* Keep one sentence per line where possible, and keep line length under 79
  characters (the ``doc8`` lint default).
* Section title underlines must be at least as long as the title text. Note
  that CJK (full-width) characters count as width 2, so make underlines
  generously long for titles that contain them.
* Use heading levels consistently within a document. The recommended order in
  this project is:

  .. code-block:: rst

     ======
     Title 1 (document title, overline and underline)
     ======

     Title 2
     =======

     Title 3
     -------

     Title 4
     ~~~~~~~

* Use admonition directives such as note and warning:

  .. code-block:: rst

     .. note::

        Something worth noting.

* Prefer explicit hyperlinks for external links, and connect terminology to
  the glossary in ``doc/source/glossary.rst``.


Documentation style guide
==========================

Korean prose conventions
------------------------

Korean is the source language of this repository, so these rules keep the
pages consistent and keep the gettext catalog stable.

* **Sentence endings**: use the polite ``합니다`` style
  ("Neutron 은 ... 서비스입니다"), not the plain ``한다`` style. The only
  exception is ``doc/source/glossary.rst``, where dictionary-style ``한다``
  definitions are used throughout.
* **Spacing around particles**: put a space between a Latin word and the
  Korean particle that follows it — ``Neutron 은``, ``Pod 가``, ``VM 의``,
  ``openstack-helm 으로``. Particles after a bare number stay attached
  (``폭이 2로``), and particles after a closing parenthesis stay attached
  (``제어 평면(control plane)이라고``).
* **First use of a term**: write it as ``한글(English, ABBR)`` — for example
  ``특별 관심 그룹(Special Interest Group, SIG)`` or
  ``역할 기반 접근 제어(role-based access control, RBAC)``. Use the
  abbreviation alone afterwards.
* **Proper nouns / project names**: keep the original spelling for names such
  as OpenStack, Kubernetes, Nova, and Neutron. Write the project name as
  ``openstack-helm`` in lower case, and spell ``Kubernetes`` out rather than
  abbreviating it to ``K8s``.
* **Preferred terms**: ``Pod`` (not 파드), ``VM`` (not 가상 머신 after the
  first use), ``Octavia`` (not 옥타비아). When in doubt, follow the headword
  used in ``doc/source/glossary.rst`` and link the first mention with
  ``:term:``.

Markup and links
----------------

* **Commands / code**: specify the appropriate language for ``code-block``
  directives (``console``, ``yaml``, ``bash``, etc.).
* Use inline literals (``` ``like this`` ```) only for code, paths, commands
  and identifiers. To emphasize a phrase, use ``**bold**`` instead.
* Prefer ``` ``literal`` ``` over the ``:code:`` role for inline code.
* Write ordered lists with ``#.`` so the numbering stays automatic.
* Point external links at their final URL, not at one that redirects
  (``https://docs.openstack.org/magnum/latest/``, not
  ``https://docs.openstack.org/magnum/``). ``tox -e linkcheck`` reports both
  broken links and redirects.

Translated documents
--------------------

Convey the meaning of the source text accurately while prioritizing natural
prose, and record the source document and its version.

For detailed rST/Sphinx conventions, see the ``doc/source/documentation/``
section.


Code of Conduct
===============

This project aims to be an open and respectful community. All participants are
encouraged to follow the spirit of the `OpenStack Community Code of Conduct
<https://www.openstack.org/legal/community-code-of-conduct/>`_.
