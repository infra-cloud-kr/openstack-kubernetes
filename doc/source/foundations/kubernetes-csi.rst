=============
CSI 기본 개념
=============

:term:`CSI` 는 컨테이너 오케스트레이터에 외부 스토리지를 연결하기 위한 표준
인터페이스입니다. 이 문서는 인터페이스 자체의 개념을 다루며, OpenStack 의
블록 스토리지를 실제로 연결하는 방법은
:doc:`../kubernetes-on-openstack/cinder-csi` 에서 다룹니다.

CSI 도입 배경
=============

Kubernetes 는 컨테이너화된 애플리케이션을 확장하고 관리할 수 있지만, 데이터를
영속적으로 관리하는 측면에서는 한계가 있습니다.

:term:`Pod` 를 재시작하면 Pod 내부에 쌓여 있던 데이터는 유실됩니다.
이를 피하려고 :term:`PV / PVC` 의 PV 를 HostPath 로 잡아 노드의 로컬 디스크에
저장할 수도 있지만, Pod 가 다른 노드로 재배포되면 그 데이터를 다시 사용할 수
없습니다.

Kubernetes 는 이 문제를 해결하기 위해 외부 스토리지를 연결하는 표준
인터페이스를 도입했습니다. 이 인터페이스를 사용하면 Pod 가 어느 노드에
재배포되더라도 같은 데이터를 계속 참조할 수 있습니다.

CSI 개념
========

`Kubernetes CSI 공식 개발 문서 <https://kubernetes-csi.github.io/docs/>`_ 에
따르면 CSI 는 컨테이너화된 워크로드에 임의의 블록 및 파일 스토리지 시스템을
노출하기 위한 표준입니다.

이름 그대로 인터페이스이므로, 클라이언트는 정해진 형식으로 요청을 보내고
구현체에 따라 서로 다른 동작이 실행됩니다. 즉 벤더는 이 표준을 구현한
드라이버(플러그인)를 만들어 배포하고, 관리자는 Kubernetes 릴리스와 무관하게
드라이버를 독립적으로 배포·업데이트하여 원하는 벤더의 스토리지를 사용할 수
있습니다.

Pod 가 어느 노드로 재배포되더라도 CSI 드라이버가 해당 노드에 외부 스토리지
볼륨을 다시 부착(attach)하므로, 같은 데이터를 계속 참조할 수 있습니다.

세부 구조
=========

CSI 드라이버는 역할이 다른 두 종류의 플러그인으로 배포되고, 노드 쪽에서는
kubelet 이 이 플러그인을 호출합니다.

* **컨트롤러 플러그인(controller plugin)** — kube-apiserver 를 통해 볼륨
  생성·삭제·부착 같은 제어를 담당합니다. 보통 :term:`Deployment` 나
  :term:`StatefulSet` 으로 운영됩니다.
* **노드 플러그인(node plugin)** — 실제 마운트(mount)와 마운트
  해제(unmount)를 수행합니다. 모든 노드에서 동작해야 하므로
  :term:`DaemonSet` 으로 배포됩니다.
* **kubelet** — CSI 컴포넌트는 아니지만, 각 노드에서 UNIX 도메인
  소켓(socket)을 통해 노드 플러그인을 호출하는 주체입니다.

.. code-block:: console

   $ kubectl get ds,deploy -n rook-ceph
   daemonset.apps/rook-ceph.rbd.csi.ceph.com-nodeplugin
   deployment.apps/rook-ceph.rbd.csi.ceph.com-ctrlplugin

작동 원리
=========

#. 사용자가 PVC 를 생성하면 Kubernetes 가 :term:`StorageClass` 를 보고 어떤
   CSI 드라이버를 쓸지 결정합니다.
#. 컨트롤러 플러그인이 스토리지 시스템에 볼륨 생성을 요청해 실제 볼륨을
   만듭니다.
#. Kubernetes 는 만들어진 결과를 PV 로 표현하고 PVC 와 바인딩합니다.
#. Pod 가 스케줄되면 필요한 경우 컨트롤러 플러그인이 노드에 볼륨을
   부착합니다.
#. 노드 플러그인이 파일시스템을 준비하고 Pod 경로에 마운트합니다.


더 읽을거리
===========

* Kubernetes CSI: https://kubernetes-csi.github.io/docs/
* CSI 동작 원리:
  https://www.netapp.com/learn/cvo-blg-kubernetes-csi-basics-of-csi-volumes-and-how-to-build-a-csi-driver/
* :doc:`../kubernetes-on-openstack/cinder-csi` — Cinder 볼륨을 CSI 로
  소비하는 관점
