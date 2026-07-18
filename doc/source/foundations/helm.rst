===============
Helm 핵심 개념
===============

OpenStack 을 Kubernetes 위에 올릴 때 반복해서 등장하는 전제 도구입니다. Helm
은 K8s 애플리케이션의 패키징·배포를 선언적으로 다룹니다. 도구 자체의 상세는
공식 문서로 링크하고, 여기서는 "이 개념이 OpenStack·K8s 결합에서 무엇에
쓰이는가"에 초점을 둡니다.

.. note::

   기여자 작업용 골격입니다. 도구 사용법을 재설명하지 말고, 각 개념이
   OpenStack·K8s 결합의 어디에 쓰이는지(왜 알아야 하는지)를 한 줄로 유지하세요.
   상세는 공식 문서와 해당 섹션으로.


핵심 구성요소
=============

.. todo::

   * Chart / Values / Release → K8s 애플리케이션을 패키징·배포하는 단위
   * Values 오버라이드 → 환경별 설정 주입 (openstack-helm 배포의 핵심 조작점)


결합에서의 역할
===============

.. todo::

   * openstack-helm 의 기반 → OpenStack 을 K8s 에 올리는 여러 방식의 전제 도구
     (:doc:`../openstack-on-kubernetes/openstack-helm`)
   * Rook 등 오퍼레이터 설치에도 Helm Chart 사용 (:doc:`../storage/ceph`)


더 읽을거리
===========

.. todo::

   Helm 공식 문서(helm.sh/docs) 링크.
