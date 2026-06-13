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

* **Translated documents**: Convey the meaning of the source (English) text
  accurately while prioritizing natural Korean prose. When a technical term
  first appears, write it as ``한글(English)``.
* **Proper nouns / project names**: Keep the original spelling for names such
  as OpenStack, Kubernetes, Nova, and Neutron.
* **Commands / code**: Specify the appropriate language for ``code-block``
  directives (``console``, ``yaml``, ``bash``, etc.).

For detailed rST/Sphinx conventions, see the ``doc/source/documentation/``
section.


Code of Conduct
===============

This project aims to be an open and respectful community. All participants are
encouraged to follow the spirit of the `OpenStack Community Code of Conduct
<https://www.openstack.org/legal/community-code-of-conduct/>`_.
