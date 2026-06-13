====================
로컬 개발 환경 준비
====================

본격적인 실습에 앞서 로컬 개발 환경을 준비합니다. 문서 작업과 가벼운
Kubernetes 실습을 위한 최소 구성을 안내합니다.

.. note::

   기여자 작업용 골격입니다. 권장 버전과 설치 명령을 검증하여 보강해
   주세요.


문서 작업 환경
==============

문서 빌드를 위해 다음을 준비합니다.

.. code-block:: console

   $ python -m venv .venv
   $ . .venv/bin/activate
   $ pip install -r doc/requirements.txt
   $ sphinx-build -W -b html doc/source doc/build/html

또는 ``tox`` 를 사용합니다.

.. code-block:: console

   $ tox -e docs


로컬 Kubernetes
===============

가벼운 실습을 위한 로컬 Kubernetes 선택지:

* kind (Kubernetes in Docker)
* minikube
* k3s


다음 단계
=========

* OpenStack on Kubernetes 실습: :doc:`openstack-helm-lab`
* Kubernetes on OpenStack 실습: :doc:`kubernetes-on-openstack-lab`
