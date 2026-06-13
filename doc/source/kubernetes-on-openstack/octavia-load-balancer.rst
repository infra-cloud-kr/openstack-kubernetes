==========================
Octavia 로드밸런서
==========================

OpenStack 의 로드밸런싱 서비스인 Octavia 는 Kubernetes 의
``Service type=LoadBalancer`` 요청을 처리하여 외부 트래픽을 분산합니다.

.. note::

   기여자 작업용 골격입니다. cloud-provider-openstack 의 로드밸런서
   컨트롤러 동작과 함께 보강해 주세요.


동작 개요
=========

#. 사용자가 ``Service type=LoadBalancer`` 를 생성
#. cloud-provider-openstack 의 로드밸런서 컨트롤러가 감지
#. Octavia 에 로드밸런서/리스너/풀 프로비저닝
#. 외부 IP(VIP)가 Service 에 할당


주요 고려사항
=============

* Octavia 와 (구) Neutron-LBaaS 의 차이
* 어노테이션을 통한 세부 설정 (헬스 모니터, 프로토콜 등)
* 옥타비아 amphora 와 OVN 프로바이더 차이


관련 문서
=========

* CCM 통합: :doc:`cloud-provider-openstack`
