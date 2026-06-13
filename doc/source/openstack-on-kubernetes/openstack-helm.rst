==============
openstack-helm
==============

`openstack-helm <https://docs.openstack.org/openstack-helm/>`_ 은 OpenStack
서비스를 Helm chart 로 패키징하여 Kubernetes 위에 배포하는 프로젝트입니다.

.. note::

   기여자 작업용 골격입니다. 실습(:doc:`../labs/openstack-helm-lab`) 경험과
   공식 문서를 바탕으로 각 절을 보강해 주세요.


개요
====

* Helm chart 단위의 OpenStack 서비스 배포
* values 를 통한 설정 오버라이드
* 의존 컴포넌트(MariaDB, RabbitMQ, Memcached 등) 관리


사전 요구사항
=============

* 동작 중인 Kubernetes 클러스터
* Helm
* 스토리지(PV/PVC) 및 네트워킹 준비


배포 흐름 (개략)
================

#. 클러스터 준비 및 네임스페이스 구성
#. 인프라 의존 컴포넌트 배포
#. Keystone 등 핵심 서비스 순차 배포
#. 검증 및 엔드포인트 확인

자세한 단계별 실습은 :doc:`../labs/openstack-helm-lab` 를 참고하세요.


GitOps 연계
===========

FluxCD/ArgoCD 와 결합하여 선언적 배포와 Day-2 운영을 자동화하는 방법은
:doc:`operations` 에서 다룹니다.
