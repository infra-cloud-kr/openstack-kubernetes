==========================================
OpenStack ↔ Kubernetes 연동 인터페이스
==========================================

가상화 기초·OpenStack·Kubernetes 세 레이어를 이해했다면, 다음은 두 기술을
실제로 잇는 표준 인터페이스입니다. 각 개념의 상세는 통합 패턴·네트워킹·
스토리지 섹션에서 다루며, 이 문서는 "무엇을 어디서 다루는지" 를 안내하는
지도(signpost) 역할을 합니다.

.. note::

   기여자 작업용 골격입니다. 이 문서는 지도 역할이므로 각 항목은 한 줄 정의와
   상세 문서 링크까지만 유지하고, 상세 설명은 링크된 문서에서 보강해 주세요
   (여기서 중복 서술하지 않기).


연동 표준 인터페이스
========================

Kubernetes 가 클라우드(OpenStack) 자원을 쓰기 위한 표준 확장점입니다. 각
인터페이스가 OpenStack 의 무엇과 이어지는지가 핵심입니다.

.. list-table::
   :header-rows: 1
   :widths: 16 54 30

   * - 인터페이스
     - 무엇을 잇나
     - 상세
   * - CNI
     - Pod 네트워킹 ↔ Neutron (두 스택 공존)
     - :doc:`../openstack-on-kubernetes/cni-and-neutron`
   * - CSI
     - 퍼시스턴트 스토리지 ↔ Cinder
     - :doc:`../kubernetes-on-openstack/cinder-csi`
   * - CCM
     - LoadBalancer·노드 수명주기 ↔ OpenStack
     - :doc:`../kubernetes-on-openstack/cloud-provider-openstack`


인터페이스는 아니지만 두 기술을 결합할 때 함께 등장하는 프로젝트·도구입니다.
성격에 따라 나누어 정리합니다(상세는 각 섹션에서 다룸).

.. note::

   전제 도구 — **Helm**: Kubernetes 패키지 매니저(Chart/Values/Release).
   openstack-helm 을 비롯한 아래 여러 방식의 기반입니다.


배포·프로비저닝
========================

두 기술을 결합하는 방법으로, 방향에 따라 나뉩니다.

.. list-table::
   :header-rows: 1
   :widths: 24 46 30

   * - 이름
     - 한 줄 정의
     - 상세
   * - openstack-helm
     - OpenStack 을 K8s 에 배포 (OpenStack → K8s)
     - :doc:`../openstack-on-kubernetes/openstack-helm`
   * - Magnum
     - OpenStack 이 K8s 클러스터를 생성 (K8s → OpenStack)
     - :doc:`../kubernetes-on-openstack/magnum`
   * - Cluster API (CAPO)
     - 선언적으로 K8s 클러스터 프로비저닝 (K8s → OpenStack)
     - :doc:`../kubernetes-on-openstack/cluster-api`


베어메탈 (물리 서버)
========================

멀티노드 운영은 결국 물리 서버로 내려갑니다. 여기서 K8s 의 Metal3 와
OpenStack 의 Ironic 이 만나는데, Metal3(CRD)가 내부적으로 Ironic 을 호출하는
구조라 두 스택의 베어메탈 관리가 한 지점으로 수렴합니다.

.. list-table::
   :header-rows: 1
   :widths: 24 46 30

   * - 이름
     - 한 줄 정의
     - 상세
   * - Ironic
     - OpenStack 의 베어메탈 프로비저닝 서비스
     - 전용 문서 예정
   * - Metal3
     - K8s(CRD)로 베어메탈 관리 — 내부적으로 Ironic 사용
     - 전용 문서 예정


공용 스토리지
========================

두 스택이 같은 스토리지 백엔드(Ceph)를 공유하는 수렴 지점입니다. K8s 측은
Rook 오퍼레이터로, OpenStack 측은 Cinder·Glance 등이 같은 Ceph 를 바라봅니다.

.. list-table::
   :header-rows: 1
   :widths: 24 46 30

   * - 이름
     - 한 줄 정의
     - 상세
   * - Ceph / Rook
     - OpenStack·K8s 공용 스토리지 백엔드 (Rook = K8s 오퍼레이터)
     - :doc:`../storage/ceph`

.. todo::

   * Metal3/Ironic 전용 심화 문서 신설 여부 검토
   * 통합 패턴 섹션이 바뀌면 이 지도의 링크·항목도 함께 갱신
