========================================================================
OpenStack & Kubernetes Operations Documentation and Internationalization
========================================================================

.. image:: https://github.com/infra-cloud-kr/openstack-kubernetes/actions/workflows/docs.yml/badge.svg
   :target: https://github.com/infra-cloud-kr/openstack-kubernetes/actions/workflows/docs.yml
   :alt: Documentation build status

This project documents how to install and operate the two leading global
open source infrastructure projects — **Kubernetes** and **OpenStack** — along
with their best practices, and contributes to the internationalization (i18n)
of the related upstream technical documentation, including its translation
into Korean.

Just as the two communities formally met through SIGs (Special Interest
Groups) to drive technical integration, their documentation localization
efforts run in parallel: the **OpenStack I18n SIG** and the **Kubernetes
SIG Docs localization subproject**. This project sits at the meeting point of
these two localization communities and aims to experience both of their
Korean localization workflows.

Following the conventions of the OpenStack documentation ecosystem, the
repository is built with `Sphinx <https://www.sphinx-doc.org/>`_ and
reStructuredText (rST), built via `tox <https://tox.wiki/>`_, and validated by
GitHub Actions. The goal goes beyond simply writing documents: contributors
also gain hands-on experience with the OpenStack-style documentation
contribution workflow (rST/Sphinx, reviewable PRs, CI-based quality checks).

.. note::

   The documentation is currently an initial skeleton. The body of each
   section is intended to be filled in incrementally (see the ``note`` / TODO
   markers in each document).


Goals
=====

The project centers on **"hands-on Korean localization"**:

* Document installation, operation, and best practices for the *OpenStack on
  Kubernetes* and *Kubernetes on OpenStack* environments, based on real
  experience building and operating them. Beyond understanding the two
  projects, contributors practice documenting in a way that follows global
  norms, building the fundamentals needed to contribute to upstream open
  source projects.
* Select the upstream documents referenced along the way and aim for 100%
  Korean localization. This includes setting up a translation platform such
  as Weblate and organizing know-how on AI-assisted translation, leaving a
  meaningful footprint in global open source documentation and i18n while
  translating with first-hand understanding of both technologies.


Documentation layout
=====================

The documentation source lives under ``doc/source/`` and is organized into the
following sections.

* **introduction** — why the two technologies are used together, the history
  and present of SIG activities, and a suggested learning path
* **OpenStack on Kubernetes** — running the OpenStack control plane on top of
  Kubernetes using openstack-helm, Kolla, and more
* **Kubernetes on OpenStack** — running Kubernetes on top of OpenStack using
  Magnum, cloud-provider-openstack, Cinder CSI, the Octavia load balancer,
  and more
* **storage** — integrating Cinder, Swift, and Ceph with Kubernetes
* **labs** — step-by-step hands-on guides
* **documentation** — rST/Sphinx basics, OpenStack/Kubernetes documentation
  conventions, and review guidelines
* **translation-i18n** — how the two Korean localization communities (the
  OpenStack I18n SIG and the Kubernetes SIG Docs localization subproject) are
  organized, plus OpenStack i18n, Kubernetes localization, Weblate, and
  AI-assisted translation workflows


Building locally
================

With `tox <https://tox.wiki/>`_ installed, build the HTML documentation with:

.. code-block:: console

   $ tox -e docs

The output is generated under ``doc/build/html/``. Open
``doc/build/html/index.html`` in a browser to review it.

To build directly without tox:

.. code-block:: console

   $ python -m venv .venv
   $ . .venv/bin/activate
   $ pip install -r doc/requirements.txt
   $ sphinx-build -W -b html doc/source doc/build/html

To lint the rST sources:

.. code-block:: console

   $ tox -e pep8


Translation (i18n)
==================

Korean is the source language; the docs are translated into English via
Weblate (https://translate.openinfra.kr, project ``openstack-kubernetes``).
Weblate reads and writes the gettext catalog at
``doc/source/locales/<lang>/LC_MESSAGES/docs.po``.

**Catalog sync is automated.** When ``doc/source/**.rst`` or ``conf.py``
changes land on ``main``, the ``i18n-sync`` workflow regenerates and
commits ``docs.po``; Weblate then picks up the changes via a GitHub
webhook. You do not need to run anything by hand. To preview/update the
catalog locally:

.. code-block:: console

   $ tox -e update-po        # regenerate docs.po (keeps existing msgstr)
   $ tox -e docs-en          # build the English site into doc/build/html/en

Translators translate in Weblate, and their work returns as pull
requests. See the *번역 · 국제화 → Weblate* and *Weblate 번역 가이드*
pages in the built documentation for the full pipeline and a
step-by-step guide.


Contributing
============

See `CONTRIBUTING.rst <CONTRIBUTING.rst>`_ for how to contribute.


License
=======

This project is licensed under the `Apache License 2.0 <LICENSE>`_.
