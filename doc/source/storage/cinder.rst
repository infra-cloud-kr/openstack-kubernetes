=========================
Cinder (블록 스토리지)
=========================

Cinder 는 OpenStack 의 블록 스토리지 서비스입니다. 이 문서는 서비스 자체를
다루며, K8s 에서 CSI 로 소비하는 관점은
:doc:`../kubernetes-on-openstack/cinder-csi` 에서 다룹니다.

.. note::

   기여자 작업용 골격입니다. Kubernetes 관점의 드라이버 사용법은
   :doc:`../kubernetes-on-openstack/cinder-csi` 에서 다루므로, 이 문서는
   스토리지 서비스 자체의 개념을 중심으로 보강해 주세요.


개념
====

* 볼륨, 스냅샷, 백업
* 볼륨 타입과 백엔드 드라이버
* 멀티 백엔드 구성
