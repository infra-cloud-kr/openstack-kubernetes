============================
CNI 와 Neutron 의 공존
============================

OpenStack on Kubernetes 구성에서 가장 헷갈리는 지점입니다. Kubernetes Pod
네트워킹(CNI)과 OpenStack 가상 네트워킹(Neutron), 성격이 다른 두 스택이 한
클러스터에 겹쳐 돌기 때문입니다.

.. note::

   기여자 작업용 골격입니다. 실습 경험과 공식 문서를 바탕으로 보강해 주세요.


두 스택이 공존하는 이유
=======================

* K8s 계층 — Pod 간 통신을 위한 CNI(Calico, Flannel 등)
* OpenStack 계층 — VM/테넌트 네트워크를 위한 Neutron
* 두 계층이 서로 다른 네트워크 네임스페이스를 다룸

.. todo::

   "무엇이 어느 계층에서 처리되는가" 를 다이어그램으로 정리(초심자 혼란 지점).


통합 접근
=========

* 두 스택을 각각 운영하는 구성
* OVN 으로 CNI 와 Neutron 을 하나로 수렴시키는 구성(ovn-kubernetes)
  — :doc:`../networking/ovn-ovs` 참고

.. todo::

   각 접근의 트레이드오프(운영 복잡도 vs 통합 이점) 정리.


더 읽을거리
===========

.. todo::

   CNI / ovn-kubernetes 참고 링크 보강.
