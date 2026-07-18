========
스토리지
========

OpenStack 의 스토리지 서비스를 다룹니다. 블록 스토리지(Cinder)와 오브젝트
스토리지(Swift), 그리고 두 스택이 공유하는 통합 백엔드 Ceph 를 포함합니다.
K8s 와의 연동(Cinder CSI 등)은 통합 패턴 섹션에서 다룹니다.

.. toctree::
   :maxdepth: 1

   cinder
   swift
   ceph
