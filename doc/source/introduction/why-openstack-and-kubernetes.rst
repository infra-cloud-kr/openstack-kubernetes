=====================================
왜 OpenStack 과 Kubernetes 인가
=====================================

클라우드 인프라의 두 축
=======================

**OpenStack** 은 풀링된 가상 리소스를 사용하여 프라이빗 및 퍼블릭 클라우드를
구축·관리하는 오픈소스 프로젝트로, Open Infrastructure Foundation(구
OpenStack Foundation)의 핵심 프로젝트입니다.

**Kubernetes** 는 컨테이너화된 애플리케이션을 자동으로 배포·스케일링·관리하는
오픈소스 프로젝트로, CNCF(클라우드 네이티브 컴퓨팅 재단, Cloud Native
Computing Foundation)의 핵심 프로젝트입니다.

두 프로젝트를 지원하는 재단 모두 Linux Foundation 과 협력하여 클라우드
인프라 및 클라우드 네이티브 기술을 발전시키고 있으며, 전 세계 수많은 기업이
두 기술을 동시에 활용하고 있습니다.


경쟁이 아니라 결합
==================

OpenStack 과 Kubernetes 는 서로 경쟁하는 기술이 아닙니다. 실무에서는 오히려
두 기술이 긴밀하게 결합되어 운영됩니다. 그 방향은 크게 두 가지입니다.

OpenStack on Kubernetes
-----------------------

OpenStack 의 각 서비스(Nova, Neutron, Keystone, Glance, Swift 등)를
컨테이너로 패키징하여 Kubernetes 위에서 운영하는 방식입니다.

* `openstack-helm <https://docs.openstack.org/openstack-helm/>`_ 을 이용한
  Helm 기반 배포
* `Kolla / Kolla-Ansible <https://docs.openstack.org/kolla-ansible/>`_ 을
  이용한 컨테이너 기반 배포

국내외 클라우드 사업자들이 OpenStack 컨트롤 플레인 현대화를 위해 이 구조를
적극 채택하고 있습니다. GitOps(FluxCD, ArgoCD)와 결합하면 Day-2 운영
자동화까지 가능해져, 대규모 프라이빗 클라우드 운영의 효율성을 크게 높일 수
있습니다.

자세한 내용은 :doc:`../openstack-on-kubernetes/index` 를 참고하세요.

Kubernetes on OpenStack
-----------------------

OpenStack 의 VM 인프라 위에 Kubernetes 클러스터를 프로비저닝·운영하는
방식입니다.

* `Magnum <https://docs.openstack.org/magnum/>`_ 을 통한 K8s-as-a-Service 제공
* `cloud-provider-openstack
  <https://github.com/kubernetes/cloud-provider-openstack>`_ 을 통한 Cinder
  볼륨·Octavia 로드밸런서·Neutron 네트워크의 Kubernetes 통합
* `Kubespray <https://github.com/kubernetes-sigs/kubespray>`_ 또는 kOps 를
  이용한 자동화 배포

OpenStack 기반 프라이빗 클라우드를 운영하는 기업이 그 위에 컨테이너
워크로드를 얹는 가장 자연스러운 경로입니다.

자세한 내용은 :doc:`../kubernetes-on-openstack/index` 를 참고하세요.


스토리지 통합
=============

스토리지 파트에서는 블록 스토리지(Cinder)와 오브젝트 스토리지(Swift)가 모두
Kubernetes 와 연동됩니다.

* **Cinder** 는 CSI 드라이버를 통해 PersistentVolume 으로 활용됩니다.
* **Swift** 는 kOps 클러스터 state store, Glance 이미지 백엔드, 애플리케이션
  오브젝트 스토리지 등 다양한 역할을 맡습니다.

자세한 내용은 :doc:`../storage/index` 를 참고하세요.


국내 현황 — 실무 장벽과 문서·노하우 공유의 부재
===============================================

OpenStack 과 Kubernetes 의 통합은 글로벌 클라우드 인프라 실무의 중요한
흐름임에도 불구하고, 관련 경험과 노하우가 충분히 공유되지 않고 있습니다.

한국에서도 이 두 기술의 통합을 추진하는 시도가 있었습니다. 대표적으로
**Hanu(하누) 이니셔티브** 는 OpenStack 기반 프라이빗 클라우드와 Kubernetes 를
통합하는 오픈소스 프로젝트로 적극적인 기여가 있었습니다. 그러나 이러한
시도들은 실무에서 어느 정도 인프라 운영 경험을 갖춘 엔지니어가 아니면 필요성
자체를 체감하기 어렵다는 높은 진입 장벽에 부딪혀 왔습니다.

openstack-helm 을 처음 접하는 개발자라면 Kubernetes, Helm, OpenStack 컴포넌트
구조를 동시에 이해해야 하며, Magnum + CAPI 드라이버 구조는 기존 Heat 기반
문서가 outdated 상태임에도 이를 안내하는 자료가 사실상 전무합니다.

결과적으로 두 가지 문제가 중첩되어 있습니다.

#. 이 기술 조합의 실무적 필요성을 입문자가 이해할 수 있는 가이드가
   없습니다.
#. 설령 필요성을 인지하더라도, 실제로 환경을 구성하고 운영해보는 과정을
   단계적으로 안내하는 문서가 부족합니다.

글로벌 커뮤니티의 공식 문서들이 존재하나, 최신 아키텍처(CAPI, CCM, Weblate 등)를
반영하지 못한 경우가 많습니다.


본 프로젝트의 접근 방식
=======================

본 프로젝트는 이 간극을 메우고자 OpenStack과 Kubernetes 운영 환경에 대해
이해 및 실습, 문서화를 진행합니다. 또한, 관련 OpenStack/Kubernetes 문서를
한글화하는 방법에 대해 설명합니다.

이는 단순한 번역을 넘어, 개발자와 인프라 엔지니어가 글로벌 오픈소스
생태계의 최신 흐름을 국제화 환경에서 접할 수 있는 기반을 마련하는 작업입니다. 나아가
기여 과정에서 OpenStack Weblate 마이그레이션 파이프라인을 직접 경험함으로써,
오픈소스 기여의 기술적 깊이와 글로벌 커뮤니티 참여 방식을 동시에 체득하는 것을 지향합니다.

다음 절(:doc:`history-and-sigs`)에서는 이러한 통합이 어떤 역사적 맥락에서
형성되어 왔는지, 두 커뮤니티의 SIG 활동을 통해 살펴봅니다.
