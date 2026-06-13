====
Ceph
====

Ceph 는 블록·오브젝트·파일 스토리지를 모두 제공하는 분산 스토리지
플랫폼으로, OpenStack 과 Kubernetes 양쪽에서 널리 쓰이는 통합 백엔드입니다.

.. note::

   기여자 작업용 골격입니다. OpenStack(Cinder/Glance/Swift 백엔드)과
   Kubernetes(Rook 등) 양쪽 관점에서 보강해 주세요.


개요
====

* RADOS 기반 분산 스토리지
* RBD(블록), RGW(오브젝트), CephFS(파일)
* OpenStack 통합 백엔드로서의 역할


OpenStack 과 Kubernetes 에서의 활용
===================================

* OpenStack: Cinder/Glance/Nova 의 공통 백엔드
* Kubernetes: Rook 를 통한 운영, CephFS/RBD CSI 드라이버
* 두 플랫폼이 동일한 Ceph 클러스터를 공유하는 구성
