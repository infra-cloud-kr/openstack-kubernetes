====================
OpenStack 주요 특징
====================

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


핵심 컴포넌트
=============

.. todo::

   핵심 서비스(Keystone, Nova, Neutron, Cinder, Glance 등)와 각 역할을
   표로 정리.


왜 컨테이너화가 자연스러운가
============================

.. todo::

   * "각 서비스가 독립된 REST API 서버" 라는 특성과, 이것이
     :doc:`../openstack-on-kubernetes/index` (openstack-helm, Kolla)의
     전제가 되는 이유 설명 보강
   * 서비스 간 의존 관계(예: 대부분의 서비스가 Keystone 인증에 의존) 정리
   * 데이터베이스(MariaDB)·메시지 큐(RabbitMQ) 등 공용 인프라 컴포넌트 보강


OpenStack 배포 방식 (배경)
==========================

OpenStack 은 여러 서비스의 집합이라 배포 방식이 곧 운영 경험을 좌우합니다.
대표적인 배포 방식부터 이 프로젝트가 다루는 방식까지 짚어 둡니다.

* DevStack — 개발·학습용 올인원(단일 노드) 배포
* Kolla-Ansible — OpenStack 을 컨테이너(Docker)로 묶어 Ansible 로 배포하는
  전통적 프로덕션 방식. Kubernetes 위가 아님
* openstack-helm — 같은 컨테이너화를 Kubernetes 네이티브(Helm)로 올린 방식.
  이 프로젝트 :doc:`../openstack-on-kubernetes/index` 의 주제

Kolla-Ansible 과 openstack-helm 의 상세 비교는
:doc:`../openstack-on-kubernetes/comparison` 에서 다룹니다.

.. todo::

   Kolla-Ansible/DevStack 을 기준점으로, openstack-helm 이 무엇을 바꾸는지
   한 문단으로 연결.


실습 전 기본 명령
=================

.. todo::

   VM/이미지/네트워크 조회 등 기본 ``openstack`` CLI 예시 보강.


더 읽을거리
===========

.. todo::

   참고 링크 보강.
