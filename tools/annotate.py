#!/usr/bin/env python3
"""Annotate preserved source paragraphs from attested readings and explicit decisions.

Run from any directory. No metrical template is used to choose a reading.
Coordinates are zero-based Unicode codepoint offsets in the ORIGINAL paragraph.
"""
import hashlib
import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
PHON = DATA / 'phonology'
ORDER = '平上去入'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def cjk(ch):
    return '\u3400' <= ch <= '\u9fff' or '\U00020000' <= ch <= '\U000323af' or '\uf900' <= ch <= '\ufaff'

def pz(tones):
    values = {'平' if t == '平' else '仄' for t in tones}
    return next(iter(values)) if len(values) == 1 else '□'

def spans(text):
    """Heading spans are retained and excluded; source lacunae remain lacunae."""
    labels = list(re.finditer(r'【[^】]*】|（[^）]*）|\([^)]*\)|\[[^]]*\]', text))
    excluded = {i for m in labels for i in range(m.start(), m.end())}
    units = []
    for m in re.finditer(r'[^，。！？、；：\n]+', text):
        inds = [i for i in range(m.start(),m.end()) if i not in excluded and (cjk(text[i]) or text[i] == '□')]
        if inds:
            units.append((inds, ''.join(text[i] for i in inds)))
    return excluded, units

def choose(char, context, pos, rules, readings):
    key = char + '|' + context
    if key in rules['exact']:
        rule = rules['exact'][key]
        return rule['tone'], 'context_exact', rule['reason']
    for rule in rules['phrases']:
        if char not in rule['chars']:
            continue
        for match in re.finditer(rule['pattern'], context):
            if match.start() <= pos < match.end():
                return rule['tone'], 'context_phrase', rule['reason']
    rule = rules['semantic'].get(char)
    if rule and not any(re.search(s,context) for s in rule.get('hold_patterns',[])):
        return rule['tone'], 'context_semantic', rule['reason']
    return '□', 'unresolved', '문맥만으로 해당 이독을 구별할 근거가 충분하지 않음'

def apply_rhyme(corpus, lex, pending, decisions, counts):
    """Only local even-line endings, with two different independently read anchors.

    No 平仄 template or 2/4-position preference is consulted. Rhyme assignments
    never serve as anchors for further assignments (avoid propagating guesses).
    Groups reset at headings, non-5/7 segments and changes of line length.
    """
    index = {(r['poem_id'],r['content_index'],r['offset']):r for r in pending}
    def keys(ch,tone=None):
        return {(e['tone'], re.sub(r'^.*聲\d*','',e['rime'])) for e in lex.get(ch,{}).get('entries',[]) if not tone or e['tone']==tone}
    accepted = set()
    for poem in corpus:
        blocks, block = [], []
        last_length = None
        for pi,text in enumerate(poem['content']):
            excluded,units=spans(text)
            # Any bracketed heading is a stanza boundary in this upstream corpus.
            if excluded and block:
                blocks.append(block);block=[];last_length=None
            for inds,context in units:
                n=len(inds)
                if n not in (5,7) or n!=last_length:
                    if block:blocks.append(block);block=[]
                last_length=n
                if n in (5,7):
                    a=poem['tone_annotations'][pi]
                    end=inds[-1];ch=text[end];tone=a['four_tones'][end]
                    block.append({'pi':pi,'offset':end,'char':ch,'tone':tone,'context':context})
        if block:blocks.append(block)
        for block in blocks:
            ends=[e for i,e in enumerate(block) if i%2==1]
            for j,end in enumerate(ends):
                loc=(poem['id'],end['pi'],end['offset'])
                if end['tone']!='□' or loc not in index:continue
                support={}
                for anchor in ends[max(0,j-3):j]+ends[j+1:j+4]:
                    if anchor['tone'] not in ORDER:continue
                    for k in keys(anchor['char'],anchor['tone']):
                        support.setdefault(k,[]).append(anchor)
                matches={k:aa for k,aa in support.items() if k in keys(end['char']) and len({a['char'] for a in aa})>=2}
                possible={k[0] for k in matches}
                if len(possible)!=1:continue
                tone=next(iter(possible));row=index[loc]
                row.update(tone=tone,pingze='平' if tone=='平' else '仄',method='rhyme_local',reason='동일 길이의 연속 시구에서 가까운 짝수구 말자 두 종류 이상이 같은 廣韻 성조·운목을 지지함',rhyme_support=[{'tone':k[0],'rime':k[1],'anchors':[{'char':a['char'],'context':a['context'],'content_index':a['pi'],'offset':a['offset']} for a in aa]} for k,aa in matches.items()])
                a=poem['tone_annotations'][end['pi']]
                for field,value in [('four_tones',tone),('pingze',row['pingze'])]:
                    arr=list(a[field]);arr[end['offset']]=value;a[field]=''.join(arr)
                accepted.add(loc);decisions.append(row)
                counts['four_tone_unresolved']-=1;counts['unresolved']-=1;counts['rhyme_local']+=1
                if pz(row['possible_tones'])=='□':counts['pingze_unresolved']-=1
    return [r for r in pending if (r['poem_id'],r['content_index'],r['offset']) not in accepted]

def apply_general_defaults(corpus, lex, supplements, pending, decisions, counts):
    """User-authorized provisional readings; never used as rhyme anchors."""
    policy = load(PHON/'general_readings.json')
    poems = {p['id']:p for p in corpus}
    remaining = []
    for initial in pending:
        profile = policy['profiles'].get(initial['char'])
        if not profile:
            remaining.append(initial)
            continue
        override = next((r for r in policy['overrides'] if r['char']==initial['char'] and r['context']==initial['context']), None)
        selected = {**profile, **(override or {})}
        entries = lex.get(initial['char'],{}).get('entries',[]) + supplements.get(initial['char'],{}).get('entries',[]) + policy.get('default_supplements',{}).get(initial['char'],[])
        support = [e for e in entries if e['tone']==selected['tone'] and e['fanqie']==selected['fanqie']]
        assert support, (initial,selected)
        row = {**initial, 'tone':selected['tone'], 'pingze':'平' if selected['tone']=='平' else '仄',
               'method':'general_default', 'status':'provisional_general', 'reason':selected['reason'],
               'previous_tone':initial['tone'], 'previous_pingze':initial['pingze'],
               'collation_required':selected.get('collation_required',False),
               'possible_tones':[t for t in ORDER if t in set(initial['possible_tones']) | {e['tone'] for e in entries}],
               'supporting_entries':[{'head':e.get('head',initial['char']),'tone':e['tone'],'fanqie':e['fanqie'],'source':e['source'],'id':e.get('id')} for e in support]}
        annotation = poems[row['poem_id']]['tone_annotations'][row['content_index']]
        for field,value in [('four_tones',row['tone']),('pingze',row['pingze'])]:
            values=list(annotation[field]);values[row['offset']]=value;annotation[field]=''.join(values)
        annotation.setdefault('general_reading_offsets',[]).append(row['offset'])
        decisions.append(row)
        counts['general_default']+=1
        counts['unresolved']-=1
        counts['four_tone_unresolved']-=1
        counts['pingze_unresolved']-=initial['pingze']=='□'
    return remaining

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict',action='store_true',help='Skip provisional general-reading defaults')
    args=parser.parse_args()
    corpus = load(DATA/'southern_candidates.json')
    lex = load(PHON/'guangyun_lexicon.json')
    rules = load(PHON/'reading_rules.json')
    supplements = load(PHON/'supplements.json')
    decisions, pending, counts = [], [], Counter()
    original = [{k:v for k,v in poem.items() if k not in ('tone_annotations','tone_annotation_version')} for poem in corpus]
    source_hash = hashlib.sha256(json.dumps(original,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    for poem in corpus:
        poem['tone_annotation_version'] = '2026-10-08-reviewed-v4-strict' if args.strict else '2026-10-08-reviewed-v4-general'
        annotations = []
        for paragraph_index, text in enumerate(poem['content']):
            excluded, units = spans(text)
            tones, binary = list(text), list(text)
            counts['excluded_heading_characters'] += sum(cjk(text[i]) for i in excluded)
            counts['source_lacunae'] += sum(text[i] in ('□','囗') for i in range(len(text)) if i not in excluded)
            for inds, context in units:
                for pos,offset in enumerate(inds):
                    char = text[offset]
                    if char in ('□','囗'):
                        tones[offset]=binary[offset]='□'
                        continue
                    readings = lex.get(char,{}).get('entries',[])
                    extra = supplements.get(char,{}).get('entries',[])
                    options = set(r['tone'] for r in readings + extra)
                    counts['verse_characters'] += 1
                    selected,method,reason = '□','unresolved','사전 수록 또는 자형 대응을 추가 확인해야 함'
                    if len(options)==1:
                        selected = next(iter(options))
                        method = 'single_reading' if len({(r.get('position'),r.get('fanqie')) for r in readings+extra})==1 else 'single_tone'
                        reason = '확보한 사전 항목의 성조가 단일함'
                    elif options:
                        selected,method,reason = choose(char,context,pos,rules,readings+extra)
                        if selected != '□':
                            assert selected in options, (char,context,selected,options)
                    if selected=='□':
                        method='unresolved'
                        reason=rules.get('holds',{}).get(char,{}).get('reason',reason)
                    tones[offset] = selected
                    binary[offset] = ('平' if selected=='平' else '仄') if selected!='□' else pz(options)
                    counts[method] += 1
                    counts['four_tone_unresolved'] += selected=='□'
                    counts['pingze_unresolved'] += binary[offset]=='□'
                    if len(options)!=1 or extra:
                        row = {'poem_id':poem['id'],'content_index':paragraph_index,'offset':offset,'char':char,'context':context,'tone':selected,'pingze':binary[offset],'possible_tones':[t for t in ORDER if t in options],'method':method,'reason':reason}
                        if selected!='□':
                            row['supporting_entries']=[{'head':r.get('head',char),'tone':r['tone'],'fanqie':r.get('fanqie'),'source':r['source'],'id':r.get('id')} for r in readings+extra if r['tone']==selected]
                            decisions.append(row)
                        else:
                            pending.append(row)
            annotations.append({'content_index':paragraph_index,'four_tones':''.join(tones),'pingze':''.join(binary),'excluded_spans':[{'start':m.start(),'end':m.end(),'text':m.group()} for m in re.finditer(r'【[^】]*】|（[^）]*）|\([^)]*\)|\[[^]]*\]',text)]})
            assert len(tones)==len(text)==len(binary)
        poem['tone_annotations'] = annotations
    pending=apply_rhyme(corpus,lex,pending,decisions,counts)
    review_path=PHON/'remaining_review.json'
    if review_path.exists():
        review=load(review_path)
        poems={p['id']:p for p in corpus}
        ledger={(r['poem_id'],r['content_index'],r['offset']):r for r in decisions+pending}
        outcomes=Counter()
        for row in review['token_reviews']:
            poem=poems[row['poem_id']]
            pi,offset=row['content_index'],row['offset']
            assert poem['content'][pi][offset]==row['char'],row
            annotation=poem['tone_annotations'][pi]
            row.setdefault('initial_pingze',row.pop('pingze',None))
            row['four_tones']=annotation['four_tones'][offset]
            row['final_pingze']=annotation['pingze'][offset]
            row['status']='resolved' if row['four_tones']!='□' else 'held'
            detail=ledger.get((row['poem_id'],pi,offset))
            row['method']=detail['method'] if detail else 'single_reading_or_tone'
            row['reason']=(detail['reason'] if row['status']=='resolved' else 'character_reviews의 해당 글자 hold_reason 참조') if detail else '재검증한 자형 대응의 사전 성조가 단일함'
            outcomes[row['status']]+=1
        assert len(review['token_reviews'])==3743
        review['outcomes']=dict(outcomes)
        save(review_path,review)
    for followup_path in [PHON/'followup_review.json', *sorted(PHON.glob('batch*_review.json'))]:
        if not followup_path.exists():continue
        review=load(followup_path)
        ledger={(r['poem_id'],r['content_index'],r['offset']):r for r in decisions+pending}
        outcomes=Counter()
        token_reviews=[]
        for initial in review['before_tokens']:
            loc=(initial['poem_id'],initial['content_index'],initial['offset'])
            final=ledger[loc]
            row={**initial,'initial_tone':initial['tone'],'initial_pingze':initial['pingze'],
                 'tone':final['tone'],'pingze':final['pingze'],'method':final['method'],
                 'reason':final['reason'],'status':'held' if final['tone']=='□' else 'resolved'}
            if final.get('rhyme_support'):row['rhyme_support']=final['rhyme_support']
            token_reviews.append(row)
            outcomes[row['status']]+=1
        review['token_reviews']=token_reviews
        review['outcomes']=dict(outcomes)
        assert len(token_reviews)==review['initial_pending_tokens']
        save(followup_path,review)
    counts['evidence_based_read']=counts['verse_characters']-counts['four_tone_unresolved']
    counts['before_general_unresolved']=counts['four_tone_unresolved']
    if not args.strict:
        pending=apply_general_defaults(corpus,lex,supplements,pending,decisions,counts)
    counts['filled_four_tones']=counts['verse_characters']-counts['four_tone_unresolved']
    output_text=[]
    for poem in corpus:
        output_text.append(f"# {poem['authorName']} · {poem['title']} [{poem['id']}]\n")
        for pi,text in enumerate(poem['content']):
            a=poem['tone_annotations'][pi]
            _,units=spans(text)
            previous_end=0
            for inds,context in units:
                for label in a['excluded_spans']:
                    if previous_end <= label['start'] < inds[0]:
                        output_text += [label['text'],'']
                output_text += [context,''.join(a['four_tones'][i] for i in inds),''.join(a['pingze'][i] for i in inds),'']
                previous_end=inds[-1]+1
            for label in a['excluded_spans']:
                if label['start'] >= previous_end:
                    output_text += [label['text'],'']
    counts['records'] = len(corpus)
    summary = {'original_fields_sha256':source_hash,'reading_policy':'strict' if args.strict else 'general_default','counts':dict(counts),'unresolved_by_character':dict(Counter(r['char'] for r in pending).most_common()),'note':'廣韻系 분류를 기준으로 한 성조 복원. general_default는 사용자 요청에 따른 일반 독음 잠정값이며 문맥 확정과 구분한다. 평측 틀로 독음을 고르지 않으며 잠정값은 운각 판독의 근거로 쓰지 않는다. 남조 당시 개별 실현음 자체를 확정하는 자료가 아니다. 역사적 검토 JSON의 결과는 일반 독음 적용 전 단계이다.'}
    save(DATA/'southern_candidates.json',corpus)
    (DATA/'southern_candidates_tones.txt').write_text('\n'.join(output_text)+'\n',encoding='utf-8')
    save(PHON/'decisions.json',decisions)
    save(PHON/'unresolved.json',pending)
    save(PHON/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
