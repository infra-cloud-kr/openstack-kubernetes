=========================
Cinder (블록 스토리지)
=========================

Cinder 는 OpenStack 의 블록 스토리지 서비스입니다. Kubernetes 에서는 Cinder
CSI 드라이버를 통해 PersistentVolume 으로 활용됩니다.

.. note::

   기여자 작업용 골격입니다. Kubernetes 관점의 드라이버 사용법은
   :doc:`../kubernetes-on-openstack/cinder-csi` 에서 다루므로, 이 문서는
   스토리지 서비스 자체의 개념을 중심으로 보강해 주세요.


개념
====

* 볼륨, 스냅샷, 백업
* 볼륨 타입과 백엔드 드라이버
* 멀티 백엔드 구성


Kubernetes 연동
===============

* CSI 드라이버를 통한 PersistentVolume 제공
* 동적 프로비저닝과 ``StorageClass`` 매핑

자세한 내용: :doc:`../kubernetes-on-openstack/cinder-csi`
