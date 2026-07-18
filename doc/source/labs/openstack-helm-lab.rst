=================================
실습: openstack-helm
=================================

openstack-helm 으로 Kubernetes 위에 OpenStack 을 배포하는 실습입니다. 순서는
OpenStack-Helm 공식 설치 흐름(Before starting → Kubernetes → Kubernetes
전제조건 → Deploy OpenStack)을 따릅니다.

.. note::

   기여자 작업용 골격입니다. 검증된 버전·전제 조건·트러블슈팅을 추가해
   주세요. 개념 설명은 :doc:`../openstack-on-kubernetes/openstack-helm`
   을 참고하고, 이 문서는 실행 가능한 단계에 집중합니다.


시작 전에 (Before starting)
===========================

* 노드 구성 및 최소 사양 — :doc:`../openstack-on-kubernetes/reference-architecture`
* 필요한 도구(kubectl, helm, git 등) 버전 명시

.. todo::

   실습에 사용할 OS·커널·컨테이너 런타임 등 기준 환경 확정.


1. Kubernetes 배포
==================

동작 중인 Kubernetes 클러스터를 준비합니다. OSH 는 Ansible 롤 기반 부트스트랩을
권장합니다.

* roles 저장소 clone
* Ansible 설치 및 roles lookup 경로 설정
* 인벤토리(inventory) 작성 — 멀티노드 구성 반영
* 플레이북(playbook) 작성 및 실행

.. todo::

   최소 3노드 인벤토리 예시와 실행 명령 보강. 로컬 대체 경로(kubeadm/멀티노드
   Kind)도 함께 안내. 토폴로지는
   :doc:`../openstack-on-kubernetes/reference-architecture` 참고.


2. Kubernetes 전제조건
======================

OpenStack 배포 전에 클러스터에 준비해야 하는 구성요소입니다.

* Gateway API — 게이트웨이/라우팅 진입점
  (:doc:`../openstack-on-kubernetes/gateway-api`)
* MetalLB — 베어메탈 ``LoadBalancer`` Service 구현
  (:doc:`../openstack-on-kubernetes/metallb`)
* Ceph — 퍼시스턴트 스토리지 백엔드 (:doc:`../storage/ceph`)
* Node labels — 서비스 배치를 위한 노드 라벨링

.. todo::

   각 전제 구성요소의 설치·검증 명령과 최소 설정값 보강.


3. OpenStack 배포
=================

* 배포 전 체크리스트 확인
* 환경 변수 설정
* values 오버라이드 획득/구성 (``get values overrides``)
* OpenStack backend 구성
* 핵심 서비스 순차 배포 (Keystone → Glance → Nova → Neutron …)
* OpenStack client 설정
* 기타 컴포넌트(optional) 배포

.. todo::

   values 오버라이드 파일 구조와 backend 선택 기준(스토리지·네트워크) 보강.


검증
====

.. code-block:: console

   $ openstack endpoint list
   $ openstack service list


정리(cleanup)
=============

실습 후 리소스를 정리하는 방법을 명시하세요.
