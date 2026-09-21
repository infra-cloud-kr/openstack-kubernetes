=============
CSI 기본 개념
=============

CSI 도입 배경
=============

쿠버네티스는 컨테이너화된 애플리케이션을 확장, 관리할 수 있지만 데이터를
영속적으로 관리하는 측면에서 한계가 존재한다.

Kubernetes의 Pod를 재시작할 때 파드 내부에 축적되어 있는 데이터 정보는
유실된다.
이러한 문제를 해결하기 위해 PV를 HostPath로 사용하여 노드의 로컬
디스크로 저장할 수 있으나, 파드가 다른 노드로 재배포될 경우 데이터를 공유하여
활용할 수 없다.

쿠버네티스는 이러한 문제를 해결하기 위해 컨테이너 간 스토리지를 이용할 수
있는 인터페이스를 구현했다.
즉, 파드가 어느 노드에 재배포가 되더라도 동일한
데이터를 참조하여 활용할 수 있게 된다.

CSI 개념
========

`Kubernetes CSI 공식 개발 문서 <https://kubernetes-csi.github.io/docs/>`_ 에
의하면 CSI는 컨테이너화된 워크로드에 임의의 블록 및 파일 스토리지 시스템을
노출하기 위한 표준을 의미한다.

이름에서부터 인터페이스가 나와 있으므로, 클라이언트는 형식화된 포맷으로
요청을 수행하게 되며, 구현부에 따라 서로 다른 기능을 실행시킬 수 있다.
즉,벤더는 이 표준을 구현한 드라이버(플러그인)를 제작하여 배포하면 되고,
관리자는 Kubernetes 릴리스와 무관하게 독립적으로 배포, 업데이트하여
원하는 벤더의 스토리지를 활용할 수 있게 된다.

파드가 어느 노드로 재배포되더라도 CSI 드라이버가 해당 노드에 외부 스토리지
볼륨을 다시 부착(attach)해주므로, 동일한 데이터를 계속 참조할 수 있다.

세부 구조
=========

CSI는 3개의 컴포넌트가 필요하다.

* Controller side: kube-apiserver를 통해 볼륨 생성, 삭제, 부착과
  같은 제어를 담당한다.
  보통 Deployment 나 StatefulSet으로 운영된다.
* Node side: 실제 마운트(mount)와 마운트 해제(unmount) 혹은 kubelet 연동을
  수행한다.
  DaemonSet으로 노드별로 배포된다.
* Kubelet: kubelet을 통해 UNIX 도메인 소켓(socket)을 통해 CSI 노드의 서비스를
  수행한다.

.. code-block:: console

   $ kubectl get ds,deploy -n rook-ceph
   daemonset.apps/rook-ceph.rbd.csi.ceph.com-nodeplugin
   deployment.apps/rook-ceph.rbd.csi.ceph.com-ctrlplugin

작동 원리
=========

1. 사용자가 PVC를 생성하면 Kubernetes가 StorageClass를 보고 어떤 CSI
   드라이버를 쓸지 결정한다.
2. Controller 쪽 CSI가 스토리지 시스템에 볼륨 생성을 요청해 실제 볼륨을 만든다.
3. Kubernetes는 만들어진 결과를 PV로 표현하고, PVC와 바인딩한다.
4. Pod가 스케줄되면 필요한 경우 controller가 노드에 attach를 수행한다.
5. 노드에서는 CSI node plugin이 파일시스템을 준비하고 Pod 경로에 마운트한다.


더 읽을거리
===========

* CSI 동작 원리:
  https://www.netapp.com/learn/cvo-blg-kubernetes-csi-basics-of-csi-volumes-and-how-to-build-a-csi-driver/
* Kubernetes CSI: https://kubernetes-csi.github.io/docs/
