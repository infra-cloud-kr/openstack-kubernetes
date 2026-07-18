============================
Kolla (컨테이너 이미지)
============================

`Kolla <https://docs.openstack.org/kolla/>`_ 는 OpenStack 서비스의 프로덕션용
컨테이너 이미지를 빌드하는 프로젝트입니다. openstack-helm 과 Kolla-Ansible 이
모두 이 이미지를 사용합니다 — 즉 Kolla 는 "배포 도구" 가 아니라 그 아래의
"이미지 레이어" 입니다.

.. note::

   기여자 작업용 골격입니다. 공식 문서와 실습 경험을 바탕으로 보강해 주세요.

   Kolla-Ansible(Ansible + Docker 로 배포하는 도구, Kubernetes 위가 아님)과
   openstack-helm 의 비교는 :doc:`comparison` 에서 다룹니다.


개요
====

* OpenStack 서비스별 컨테이너 이미지 빌드(source / binary 타입)
* 배포판·버전 조합에 맞춘 이미지 태깅
* openstack-helm 이 배포하는 Pod 가 실제로 사용하는 이미지 출처

.. todo::

   이미지 빌드 옵션과 커스터마이징(로컬 레지스트리 등) 보강.


openstack-helm 과의 관계
========================

* openstack-helm 의 chart 는 Kolla 이미지를 참조해 Pod 로 실행
* 이미지 레지스트리·태그를 values 로 지정 — :doc:`openstack-helm`

.. todo::

   Kolla 이미지 ↔ openstack-helm values(이미지 지정) 연결 예시 보강.


참고
====

* Kolla — https://docs.openstack.org/kolla/
* Kolla-Ansible(배포 도구, 비교용) — https://docs.openstack.org/kolla-ansible/
