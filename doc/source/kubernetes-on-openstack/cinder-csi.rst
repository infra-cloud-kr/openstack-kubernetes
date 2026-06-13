==========
Cinder CSI
==========

Cinder CSI 드라이버는 OpenStack 의 블록 스토리지(Cinder)를 Kubernetes 의
PersistentVolume 으로 제공합니다.

.. note::

   기여자 작업용 골격입니다. :doc:`../storage/cinder` 와 내용이 연결되므로
   중복을 피하며 보강해 주세요.


개요
====

* ``StorageClass`` 를 통한 동적 프로비저닝
* 볼륨 확장, 스냅샷, 토폴로지 인식
* CSI 표준 인터페이스 준수


기본 사용 흐름
==============

#. CSI 드라이버 배포
#. ``StorageClass`` 정의 (Cinder 백엔드 지정)
#. ``PersistentVolumeClaim`` 생성
#. 파드에서 볼륨 마운트


관련 문서
=========

* 스토리지 관점의 설명: :doc:`../storage/cinder`
* CCM 과의 관계: :doc:`cloud-provider-openstack`
