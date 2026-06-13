===================================
실습: Kubernetes on OpenStack
===================================

OpenStack 위에 Kubernetes 클러스터를 프로비저닝하는 실습입니다.

.. note::

   기여자 작업용 골격입니다. 검증된 버전·전제 조건·트러블슈팅을 추가해
   주세요. 개념 설명은 :doc:`../kubernetes-on-openstack/index` 를 참고하고,
   이 문서는 실행 가능한 단계에 집중합니다.


전제 조건
=========

* 접근 가능한 OpenStack 클라우드 (프로젝트/쿼터 확인)
* ``openstack`` CLI 및 인증 정보(clouds.yaml 또는 RC 파일)
* 적절한 이미지/플레이버/네트워크


배포 경로 선택
==============

* **Magnum** — OpenStack 이 제공하는 관리형 클러스터
  (:doc:`../kubernetes-on-openstack/magnum`)
* **Kubespray** — Ansible 기반 직접 배포
* **Cluster API (CAPI)** — 선언적 클러스터 수명주기 관리


배포 후 통합 검증
=================

#. CCM 동작 확인 (노드/로드밸런서)
   (:doc:`../kubernetes-on-openstack/cloud-provider-openstack`)
#. Cinder CSI 로 PVC 프로비저닝 확인
   (:doc:`../kubernetes-on-openstack/cinder-csi`)
#. ``Service type=LoadBalancer`` 로 Octavia 연동 확인
   (:doc:`../kubernetes-on-openstack/octavia-load-balancer`)


정리(cleanup)
=============

실습 후 리소스를 정리하는 방법을 명시하세요.
