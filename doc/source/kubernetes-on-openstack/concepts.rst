==========
핵심 개념
==========

OpenStack 위에 Kubernetes 를 올릴 때 알아야 할 핵심 개념을 정리합니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


배포 경로
=========

* **Magnum** — OpenStack 이 제공하는 K8s-as-a-Service
  (:doc:`magnum`)
* **Kubespray** — Ansible 기반 범용 Kubernetes 배포 도구
* **kOps** — 클러스터 수명주기 관리 도구 (state store 로 Swift 활용 가능)
* **Cluster API (CAPI)** — 선언적 클러스터 수명주기 관리


OpenStack 과의 통합 지점
========================

Kubernetes 가 OpenStack 서비스를 활용하는 표준 인터페이스는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 인터페이스
     - 역할
   * - CCM (Cloud Controller Manager)
     - 노드 수명주기, 로드밸런서, 라우팅 통합
       (:doc:`cloud-provider-openstack`)
   * - CSI (Container Storage Interface)
     - Cinder 블록 스토리지를 PersistentVolume 으로 (:doc:`cinder-csi`)
   * - LoadBalancer Service
     - Octavia 를 통한 로드밸런서 프로비저닝
       (:doc:`octavia-load-balancer`)
