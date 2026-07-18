==============================
핵심 개념 (OpenStack on K8s)
==============================

OpenStack 을 Kubernetes 위에서 운영하기 전에 잡아 두면 좋은 핵심 개념을
모았습니다.

.. note::

   기여자 작업용 골격입니다. 각 절을 실습 경험과 공식 문서를 바탕으로
   보강해 주세요.


왜 OpenStack 을 컨테이너로 운영하는가
=====================================

* 선언적 배포와 반복 가능한 업그레이드
* 컨트롤 플레인 구성요소의 격리와 스케일링
* Kubernetes 의 자가 치유(self-healing) 및 롤아웃/롤백 활용
* GitOps 와 결합한 Day-2 운영 자동화


구성요소 매핑
=============

OpenStack 의 주요 서비스가 Kubernetes 리소스로 어떻게 매핑되는지 정리합니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - OpenStack 서비스
     - Kubernetes 상의 형태 (예)
   * - Keystone (인증)
     - Deployment + Service, 외부 노출용 Ingress
   * - Nova (compute)
     - 컨트롤 컴포넌트는 Pod, 하이퍼바이저 노드는 별도 관리
   * - Neutron (network)
     - Deployment/DaemonSet 조합
   * - Glance (image)
     - Deployment + 오브젝트 스토리지 백엔드
   * - 데이터베이스 / 메시지 큐
     - Operator 또는 StatefulSet (MariaDB, RabbitMQ 등)


배포 방식 비교
==============

컨테이너화된 OpenStack 을 올리는 배포 방식은 크게 둘입니다.

* :doc:`openstack-helm` — Helm chart 기반, Kubernetes 위 배포
* Kolla-Ansible — Ansible + Docker 기반(Kubernetes 아님)

두 방식의 상세 비교와 선택 기준은 :doc:`comparison` 에서 다룹니다. 두 방식이
공통으로 사용하는 컨테이너 이미지 레이어는 :doc:`kolla` 를 참고하세요.
