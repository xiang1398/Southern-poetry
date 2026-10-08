# Southern Poetry — 南朝詩歌語料庫

A preliminary, provenance-preserving subset of [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), from `source/诗/南北朝/poetry.南北朝.0000.base.json`.

**Status: preliminary author-based selection, NOT a critically established edition or final attribution.** The source groups Northern, Southern and Sui poets under 南北朝; its dynasty field alone is not usable for Southern attribution.

- `data/southern_candidates.json`: 381 candidate works, 49 authors; require poem-level verification.
- `data/review_required.json`: 59 works: 庾信, 蕭詧, 蘇小小, 陸凱, anonymous. For transregional poets, author origin is not equivalent to place/date of composition.
- `data/excluded.json`: 41 works, provisionally excluded by author attribution (Northern or Sui); retain for audit.
- `source/original_northern_southern.json`: unmodified upstream snapshot (481 works).

Original fields and IDs are retained. Extra `source_repository`, `source_path`, `selection_status` fields document provenance and selection.

## Scope and limitations

The candidates are **not yet independently checked** against chronological sources, variant readings, poem-level dating, duplicate records, or completeness. In particular, do not treat this as all Southern Dynasties poetry. A second phase will add author/poem metadata (Liu Song, Southern Qi, Liang, Chen), composition location/date confidence, five/seven-character verse segmentation, and historically appropriate four-tone assignments with polyphonic-character uncertainty.

## Source attribution

Source: [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), path `source/诗/南北朝/poetry.南北朝.0000.base.json`, fetched 2026-10-08. Check the upstream repository license and original underlying textual sources before redistribution beyond this research copy.

## Research aim

Test whether 上、去、入 behave as a common non-平 metrical class in Southern Dynasties verse, distinguishing four-tone dissimilation from 平/非平 opposition and controlling for token-level tone frequencies.
