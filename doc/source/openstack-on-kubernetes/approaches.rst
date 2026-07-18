======================
배포 방식과 프로젝트
======================

OpenStack 을 Kubernetes 위에 올리는 방법은 하나가 아닙니다. 여기서는 대표적인
프로젝트·접근을 훑고, 그중 이 섹션이 중심으로 삼는 openstack-helm 이 어디에
서 있는지 짚습니다.

.. note::

   기여자 작업용 골격입니다. 이 문서는 지형(landscape) 안내용이므로 각
   프로젝트는 한 줄 소개와 링크까지만 유지하고, 최신 생태계에 맞추어 목록을
   보강해 주세요.


프로젝트·접근 한눈에 보기
=========================

.. list-table::
   :header-rows: 1
   :widths: 26 44 30

   * - 프로젝트·접근
     - 성격
     - 비고
   * - openstack-helm
     - Helm 차트 기반(OpenStack 공식). 이 섹션의 중심
     - :doc:`openstack-helm`
   * - openstack-k8s-operators
     - 오퍼레이터(CRD) 기반 (Red Hat RHOSO/"podified")
     - Helm 이 아닌 접근
   * - Kolla-Ansible
     - 컨테이너(Docker)+Ansible, Kubernetes 아님
     - 비교: :doc:`comparison`

.. todo::

   * 각 프로젝트의 위치(기반/배포판/대안)와 openstack-helm 과의 관계 보강
   * 최신 생태계 반영(신규 프로젝트 추가·정리)
