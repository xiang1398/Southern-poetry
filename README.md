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

시구 본문 39,736자 중 근거 기반 판독은 37,675자이다. 사용자 요청에 따라 미확정 이독 2,061곳에 일반 독음의 **잠정값**을 적용하여 사성·평측 39,736자를 모두 채웠다. 嗳·垌은 집운·강희의 사전 독음을 잠정 적용했으며 자형 교감 문제는 남아 있다. 熳은 爛漫 대응을 거쳐 집운 漫의 去聲을 적용했다. 잠정값은 `decisions.json`의 `general_default` 및 문단 주석의 `general_reading_offsets`로 구분한다. 본문 결자 12자와 소제목·설명 625자는 이 수량에서 제외한다. 412는 원본 레코드 수이며 묶음시 레코드도 포함한다.

[일반 독음 정책](data/phonology/general_readings.json)은 통행 용법을 기준으로 선택한 대표 독음이며 최빈 독음을 통계적으로 증명한 자료가 아니다. `python tools/annotate.py --strict`는 잠정값을 제외한 결과(사성 미확정 2,061곳)를 생성하고, `python tools/annotate.py`는 일반 독음을 적용한다. 疋 1곳은 廣韻의 匹 속자 주기에 따라 수량사로 추가 판독했다.

기존 `analysis/`, `annotated/`, `reviewed/`의 성조 분석·중간본·통계는 최신 브랜치에서 삭제했다. 원본 시가 스냅샷과 선정 자료는 유지한다. 문맥 판독은 복원이며, □를 평측 배열에 맞춰 채우는 규칙은 없다.

후속 검증으로 직전 커밋의 미확정 3,743곳 중 1,252곳을 추가 판독했다. 이전 미커밋 결과 995곳을 재현하고 이번에 257곳을 더 판독했다. [3,743곳의 판독 전후 좌표](data/phonology/remaining_review.json)와 [후속 시구 판독·보류 근거](data/phonology/followup_review.json)를 보존했다.

추가 문맥 검증에서 陳·勝·遺·養·彈·障의 53곳을 더 판독했다. 전체 추가 판독은 최초 미확정 3,743곳 중 1,305곳이다. [추가 53곳의 좌표·근거 및 보류 사항](data/phonology/batch04_review.json)을 보존했다.

다음 검증에서 141곳을 추가 판독하여 최초 3,743곳 대비 누적 1,446곳을 판독했다. [시구별 판독·보류 및 泥泥의 상성 후보 보충](data/phonology/batch05_review.json)을 기록했다.

추가 검증에서 146곳을 판독하여 최초 3,743곳 대비 누적 1,592곳을 판독했다. [363곳의 시구별 판독·보류 및 臉의 뺨 의미 후보 보충](data/phonology/batch06_review.json)을 기록했다. 出의 문맥 독법에는 역사적 입·거성 통용 가능성도 명시했다.

추가 어휘·품사 검증에서 89곳을 판독하여 최초 3,743곳 대비 누적 1,681곳을 판독했다. [시구별 판독·보류 근거](data/phonology/batch07_review.json)를 기록했다.
