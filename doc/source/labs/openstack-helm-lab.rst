=================================
실습: openstack-helm
=================================

openstack-helm 으로 Kubernetes 위에 OpenStack 을 배포하는 실습입니다.

.. note::

   기여자 작업용 골격입니다. 검증된 버전·전제 조건·트러블슈팅을 추가해
   주세요. 개념 설명은 :doc:`../openstack-on-kubernetes/openstack-helm`
   을 참고하고, 이 문서는 실행 가능한 단계에 집중합니다.


전제 조건
=========

* 동작 중인 Kubernetes 클러스터 (버전 명시)
* Helm (버전 명시)
* 충분한 CPU/메모리/스토리지


단계
====

#. 클러스터/네임스페이스 준비
#. 인프라 의존 컴포넌트 배포 (MariaDB, RabbitMQ, Memcached 등)
#. Keystone 배포 및 검증
#. 추가 서비스(Glance, Nova, Neutron 등) 순차 배포
#. 엔드포인트 및 인증 검증


검증
====

.. code-block:: console

   $ openstack endpoint list
   $ openstack service list


정리(cleanup)
=============

실습 후 리소스를 정리하는 방법을 명시하세요.
