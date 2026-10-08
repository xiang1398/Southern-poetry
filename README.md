# Southern Poetry — 南朝詩歌語料庫

A preliminary, provenance-preserving subset of [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), from `source/诗/南北朝/poetry.南北朝.0000.base.json`.

**Status: preliminary author-based selection, NOT a critically established edition or final attribution.** The source groups Northern, Southern and Sui poets under 南北朝; its dynasty field alone is not usable for Southern attribution.

- `data/southern_candidates.json`: 412 included works, 52 authors; require poem-level verification.
- `data/review_required.json`: 31 works: 蘇小小, 陸凱, anonymous.
- `data/excluded.json`: 38 works, provisionally excluded by author attribution (Northern or Sui); retain for audit.
- `source/original_northern_southern.json`: unmodified upstream snapshot (481 works).

Original fields and IDs are retained. Extra `source_repository`, `source_path`, `selection_status` fields document provenance and selection.

## Scope and limitations

The candidates are **not yet independently checked** against chronological sources, variant readings, poem-level dating, duplicate records, or completeness. In particular, do not treat this as all Southern Dynasties poetry. The corpus now includes four-tone and 平仄 annotations. Author/poem dating, duplicates and textual variants still require independent checking.

## Source attribution

Source: [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), path `source/诗/南北朝/poetry.南北朝.0000.base.json`, fetched 2026-10-08. Check the upstream repository license and original underlying textual sources before redistribution beyond this research copy.

## Research aim

Test whether 上、去、入 behave as a common non-平 metrical class in Southern Dynasties verse, distinguishing four-tone dissimilation from 平/非平 opposition and controlling for token-level tone frequencies.

## Updated cross-regional inclusion policy (2026-10-08)

Include poets who began composing in Southern Dynasties literary circles even when later active in Northern courts. 庾信, 蕭詧, 王褒 are now included. Southern training does NOT imply that every poem was composed in the South. Cross-regional records have `southern_training: true`, `cross_regional_author: true`, and `composition_period: undetermined`. Date individual poems before comparing Southern-period vs Northern-period tonal patterns.

Current counts: 412 included, 31 review, 38 excluded; 52 included authors.

## 성조·평측 주석 (2026-10-08)

- [원문 필드에 주석을 추가한 412개 레코드](data/southern_candidates.json)
- [시구 아래 사성·평측을 표시한 TXT](data/southern_candidates_tones.txt)
- [판독 기준과 재현 방법](docs/tone_annotation.md)
- [사전 출처](data/phonology/sources.json) · [사전 항목 스냅샷](data/phonology/guangyun_lexicon.json)
- [문맥 판독 규칙](data/phonology/reading_rules.json) · [개별 판독 기록](data/phonology/decisions.json)
- [미확정 목록](data/phonology/unresolved.json) · [현재 집계](data/phonology/summary.json)

원문과 원본 ID를 유지하고 `tone_annotations`를 직접 추가했다. 이독이 하나인 글자부터 처리하고, 같은 성조의 다독자, 문맥에 따른 판독, 제한적인 국소 압운 판독을 구별했다. 《廣韻》 반절·석의와 고자·이체자를 대조하고, 《集韻》 전자 원문 및 외부 사전으로 보충했다.

시구 본문 39,736자 중 사성 37,439자(94.22%), 평측 38,372자(96.57%)를 채웠다. 사성 미확정 2,297자, 평측 미확정 1,364자는 □로 남겼다. 본문 결자 12자와 소제목·설명 625자는 이 수량에서 제외한다. 412는 원본 레코드 수이며 묶음시 레코드도 포함한다.

기존 `analysis/`, `annotated/`, `reviewed/`의 성조 분석·중간본·통계는 최신 브랜치에서 삭제했다. 원본 시가 스냅샷과 선정 자료는 유지한다. 문맥 판독은 복원이며, □를 평측 배열에 맞춰 채우는 규칙은 없다.

후속 검증으로 직전 커밋의 미확정 3,743곳 중 1,252곳을 추가 판독했다. 이전 미커밋 결과 995곳을 재현하고 이번에 257곳을 더 판독했다. [3,743곳의 판독 전후 좌표](data/phonology/remaining_review.json)와 [후속 시구 판독·보류 근거](data/phonology/followup_review.json)를 보존했다.

추가 문맥 검증에서 陳·勝·遺·養·彈·障의 53곳을 더 판독했다. 전체 추가 판독은 최초 미확정 3,743곳 중 1,305곳이다. [추가 53곳의 좌표·근거 및 보류 사항](data/phonology/batch04_review.json)을 보존했다.

다음 검증에서 141곳을 추가 판독하여 최초 3,743곳 대비 누적 1,446곳을 판독했다. [시구별 판독·보류 및 泥泥의 상성 후보 보충](data/phonology/batch05_review.json)을 기록했다.
