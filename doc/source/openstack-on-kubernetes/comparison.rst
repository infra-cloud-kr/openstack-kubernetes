================================
Kolla-Ansible vs openstack-helm
================================

두 배포 도구 모두 OpenStack 배포를 자동화하지만, 오케스트레이션 계층이
다릅니다(Kolla-Ansible = Ansible + Docker, openstack-helm = Kubernetes + Helm).
즉 Kolla-Ansible 은 Kubernetes 위가 아니라 Docker 컨테이너로 직접 배포하며,
이 문서는 그 대비로 openstack-helm 이 무엇을 바꾸는지 정리합니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


오케스트레이션 레이어 차이
==========================

* Kolla-Ansible — idempotent playbook 실행(push 기반), 지속 reconcile 없음
* openstack-helm — Kubernetes 컨트롤러의 reconciliation loop 상속

.. todo::

   두 모델의 desired-state 관리 방식 차이를 표로 정리.


가용성 / 운영
=============

* self-healing, 롤링 업데이트, 스케일 아웃의 선언성 비교
* 디버깅 경험(SSH 컨테이너 확인 vs kubectl/기존 K8s tooling)

.. todo::

   Prometheus/Grafana 등 기존 K8s 운영 tooling 통합 관점 보강.


stateful 워크로드 문제
======================

* nova-compute, cinder-volume 등 하이퍼바이저/스토리지 바인딩 서비스의 K8s화
* hostPath / DaemonSet 강제 등 Pod 추상화와의 충돌 지점

.. todo::

   openstack-helm 학습의 최대 난관인 stateful 서비스 처리 방식 보강.


언제 무엇을 고르나
==================

.. todo::

   조직 상황별(기존 K8s 운영 역량 유무 등) 선택 기준 정리.


더 읽을거리
===========

.. todo::

   Kolla-Ansible / openstack-helm 공식 문서 링크 보강.
