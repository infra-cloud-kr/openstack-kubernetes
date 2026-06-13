=====================
Kolla / Kolla-Ansible
=====================

`Kolla <https://docs.openstack.org/kolla/>`_ 는 OpenStack 서비스의 프로덕션용
컨테이너 이미지를 제공하며,
`Kolla-Ansible <https://docs.openstack.org/kolla-ansible/>`_ 은 이를 Ansible
로 배포·운영하는 도구입니다.

.. note::

   기여자 작업용 골격입니다. 공식 문서와 실습 경험을 바탕으로 보강해 주세요.


개요
====

* Kolla: OpenStack 서비스 컨테이너 이미지 빌드/배포
* Kolla-Ansible: Ansible 기반 배포 자동화
* openstack-helm 과의 차이: 오케스트레이션 계층(Ansible vs Helm/Kubernetes)


언제 무엇을 선택하는가
======================

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 기준
     - 고려사항
   * - 운영 플랫폼
     - 이미 Kubernetes 중심이면 openstack-helm 이 자연스러움
   * - 학습 곡선
     - Ansible 친숙도 vs Helm/Kubernetes 친숙도
   * - 업그레이드 전략
     - 두 방식의 롤링 업그레이드/롤백 모델 차이


참고
====

* Kolla — https://docs.openstack.org/kolla/
* Kolla-Ansible — https://docs.openstack.org/kolla-ansible/
