# Southern Poetry — 南朝詩歌語料庫

A preliminary, provenance-preserving subset of [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), from `source/诗/南北朝/poetry.南北朝.0000.base.json`.

**Status: preliminary author-based selection, NOT a critically established edition or final attribution.** The source groups Northern, Southern and Sui poets under 南北朝; its dynasty field alone is not usable for Southern attribution.

- `data/southern_candidates.json`: 412 included works, 52 authors; require poem-level verification.
- `data/review_required.json`: 31 works: 蘇小小, 陸凱, anonymous.
- `data/excluded.json`: 38 works, provisionally excluded by author attribution (Northern or Sui); retain for audit.
- `source/original_northern_southern.json`: unmodified upstream snapshot (481 works).

Original fields and IDs are retained. Extra `source_repository`, `source_path`, `selection_status` fields document provenance and selection.

## Scope and limitations

The candidates are **not yet independently checked** against chronological sources, variant readings, poem-level dating, duplicate records, or completeness. In particular, do not treat this as all Southern Dynasties poetry. A second phase will add author/poem metadata (Liu Song, Southern Qi, Liang, Chen), composition location/date confidence, five/seven-character verse segmentation, and historically appropriate four-tone assignments with polyphonic-character uncertainty.

## Source attribution

Source: [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), path `source/诗/南北朝/poetry.南北朝.0000.base.json`, fetched 2026-10-08. Check the upstream repository license and original underlying textual sources before redistribution beyond this research copy.

## Research aim

Test whether 上、去、入 behave as a common non-平 metrical class in Southern Dynasties verse, distinguishing four-tone dissimilation from 平/非平 opposition and controlling for token-level tone frequencies.

## Updated cross-regional inclusion policy (2026-10-08)

Include poets who began composing in Southern Dynasties literary circles even when later active in Northern courts. 庾信, 蕭詧, 王褒 are now included. Southern training does NOT imply that every poem was composed in the South. Cross-regional records have `southern_training: true`, `cross_regional_author: true`, and `composition_period: undetermined`. Date individual poems before comparing Southern-period vs Northern-period tonal patterns.

Current counts: 412 included, 31 review, 38 excluded; 52 included authors.

## Exploratory tonal analysis (2026-10-08)

**[한국어 분석 보고서](analysis/RESULTS_KO.md)** · [원자료를 재현한 시구별 표](analysis/verse_lines.tsv) · [집계 JSON](analysis/results.json) · [평측/사성 모형 비교](analysis/model_comparison.json) · [민감도 분석](analysis/robustness.json) · [모형 선택 bootstrap](analysis/model_bootstrap.json) · [재현용 Python](analysis/reproduce.py).

The data support a marked rise in second-vs-fourth-position P/Z opposition from Song-author cohorts to Qi, Liang, and Chen author cohorts. Four-tone dissimilation fits the strict Song subset modestly better; P/Z binary fits Qi and later subsets more convincingly. **This is provisional evidence, not a directly dated history of poem composition or evidence of conscious metrical doctrine.**

## Activity-period regrouping (2026-10-08)

For an alternative **principal literary activity period** grouping (not poem-level composition dating), see [Korean results](analysis/ACTIVITY_RESULTS_KO.md), [updated statistics](analysis/activity_results.json), [author attribution with confidence notes](analysis/activity_author_cohorts.json), and [line-level reclassified data](analysis/activity_verse_lines.tsv). The previous grouping remains available for comparison. 江淹 is a particularly influential borderline Song/Qi reassignment and must be treated as tentative.
