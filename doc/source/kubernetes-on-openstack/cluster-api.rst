============================
Cluster API (CAPO)
============================

Cluster API(CAPI)는 Kubernetes 클러스터 자체를 K8s 스타일 API(CRD)로 선언적으로
프로비저닝·관리하는 프로젝트입니다. CAPO(Cluster API Provider OpenStack)는 그
OpenStack 프로바이더로, OpenStack(Nova/Neutron 등) 위에 K8s 클러스터를 만듭니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.

   Magnum 과 함께 "K8s on OpenStack" 클러스터 프로비저닝의 대표 방식입니다.


개요
====

* CAPI 리소스 모델 — Cluster / MachineDeployment / Machine 등
* CAPO 가 사용하는 OpenStack 자원 — Nova(VM), Neutron, (선택) Octavia LB
* 선언적 클러스터 수명주기(생성·확장·업그레이드·삭제)

.. todo::

   부트스트랩(관리 클러스터) 구성과 최소 CAPO 매니페스트 예시 보강.


Magnum 과의 비교
================

* Magnum — OpenStack API/서비스로 K8s 클러스터 제공 (:doc:`magnum`)
* CAPO — Kubernetes 네이티브 API(CRD)로 선언적 프로비저닝

.. todo::

   선택 기준(기존 운영 방식, 멀티클라우드 일관성 등) 정리.


더 읽을거리
===========

.. todo::

   Cluster API / CAPO 공식 문서 링크 보강.
