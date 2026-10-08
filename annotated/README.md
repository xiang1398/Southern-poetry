# 南朝詩歌逐行四聲標注

- `southern_poetry_tone_annotated.txt`: 412수 원문 각 행 바로 아래에 平上去入 또는 □를 한 글자씩 표기.
- `southern_poetry_tone_annotated.json`: 작품 ID·작가·대표 활동 조대·원본 출처를 유지한 구조화 판본.

## 표기 원칙

각 漢字에 대해 《廣韻》 계열 QYS4MCPDict 자료에서 유일한 성조만 확인되면 **平·上·去·入**으로 표기합니다. 두 성조 이상이 가능하거나 해당 글자가 자료에 없으면 **□**로 표기합니다. □는 平仄의 확정 여부와 무관하게 **四聲이 단일하게 확정되지 않았다는 뜻**입니다. 문맥에 따른 異讀 판정은 아직 하지 않았습니다. 구두점은 원문과 동일한 위치에 유지합니다. 간체자는 OpenCC의 STCharacters 정체 후보를 통해 대조했으며, 이 과정에서 정체 후보가 여럿이면 그 성조도 모두 고려하므로 □가 늘 수 있습니다.

## 출처 및 보존

- 원본 481수: [snowtraces/poetry-source](https://github.com/snowtraces/poetry-source), `source/诗/南北朝/poetry.南北朝.0000.base.json`.
- 포함 412수: 본 저장소 `data/southern_candidates.json`; 보류 31수·제외 38수는 기존 파일에 보존.
- 聲調: [untunt/QYS4MCPDict](https://github.com/untunt/QYS4MCPDict), `all_chars.tsv`, `all_rimes.tsv`.
- 簡繁字形: [BYVoid/OpenCC](https://github.com/BYVoid/OpenCC), `data/dictionary/STCharacters.txt`.
- 성조 집합 및 자형 후보: 본 저장소 `analysis/tone_inventory.json`.

## 주의

이 파일은 《廣韻》 기준의 기계적 四聲 표기이며, 六朝 당대의 음운체계를 직접 복원한 것이 아닙니다. 특히 多音字의 文讀·白讀, 詩句 문맥, 詞性, 押韻을 고려한 판정은 후속 교감이 필요합니다. 작품별 시대 분류도 확정된 편년이 아닌 시인별 주요 창작 활동 조대입니다.

## 통계

총 漢字 40365자 중 단일 四聲 확정 30090자 (74.5%), □ 10275자 (25.5%); □ 가운데 多音 9726, 사전 미수록 549.
