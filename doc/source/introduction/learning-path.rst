==========
학습 경로
==========

아래 학습 경로는 두 오픈소스 기술을 직접 경험한 뒤 문서화·번역에 기여하기
위한 권장 순서입니다. 사전 지식 수준에 따라 조정할 수 있습니다.


1단계: 실습 기반 이해와 문서화
==============================

#. **개념 이해** — :doc:`why-openstack-and-kubernetes` 와
   :doc:`history-and-sigs` 를 읽고 두 기술이 함께 쓰이는 맥락을 파악합니다.
#. **문서화 도구 준비** — :doc:`../documentation/rst-sphinx-basics` 를 따라
   rST/Sphinx 와 ``tox`` 빌드 환경을 익힙니다.
#. **실습 환경 구성** — :doc:`../labs/index` 의 가이드를 따라 로컬 또는
   클라우드에서 실습 환경을 구성합니다.

   * OpenStack on Kubernetes 경로: :doc:`../labs/openstack-helm-lab`
   * Kubernetes on OpenStack 경로: :doc:`../labs/kubernetes-on-openstack-lab`

#. **문서화 기여** — 실습 중 얻은 이해를 바탕으로 설치·운영·모범 사례를
   문서화하고, 리뷰 가능한 PR 로 제출합니다
   (:doc:`../documentation/review-guidelines`).


2단계: 공식 문서 한글화와 국제화
================================

#. **대상 문서 선정** — 앞 단계에서 참조한 공식 문서 중 한글화 가치가 높은
   문서를 선정합니다.
#. **번역 워크플로우 학습** — :doc:`../translation-i18n/index` 를 따라
   OpenStack i18n / Kubernetes 현지화 / Weblate / AI 보조 번역 흐름을
   익힙니다.
#. **100% 한글화** — 선정한 문서를 번역하고, 번역 플랫폼을 통해 리뷰·반영
   과정을 경험합니다.
#. **노하우 정리** — 번역 과정에서 얻은 AI 보조 번역 노하우와 파이프라인을
   정리하여 커뮤니티에 환원합니다.


사전 지식 점검
==============

다음 항목에 익숙하지 않다면 해당 공식 문서를 먼저 둘러보길 권장합니다.

* 리눅스 기본 명령어, SSH, ``git`` 기본 사용법
* 컨테이너 기본 개념 (이미지, 컨테이너, 레지스트리)
* Kubernetes 기본 오브젝트 (Pod, Deployment, Service, PVC)
* OpenStack 핵심 서비스 (Keystone, Nova, Neutron, Cinder, Glance)
