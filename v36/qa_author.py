#!/usr/bin/env python3
"""v36 1차(작성자) 점검: 지문 단서 존재, 모범답안 자동 감지, 실제 답안 재채점, 누설·말줄임·연결 id·GEO."""
import json,re,subprocess,sys
d=json.load(open('/workspace/edu/src/items.json'));I={x['id']:x for x in d['items']}
B={x['id']:x for x in json.load(open('/workspace/edu/v36/items_before.json'))['items']}
LOG=json.load(open('/workspace/edu/v36/log.json'));st=json.load(open('/workspace/edu/v36/st.json'))
norm=lambda s:re.sub(r"[\s\(\)\[\]·,./→\-~'\"“”‘’:;!?㉠㉡㉢]","",str(s).lower())
hits=lambda t,kw:[any(norm(a) in norm(t) for a in g) for g in kw]
bad=[]
ids=[x['id'] for x in d['items']];assert len(ids)==len(set(ids));print('ids unique',len(ids))
# 바뀌지 않은 문항은 그대로
changed={e['id'] for e in LOG['edit']}|set(LOG['new'])
for i,x in B.items():
    if i not in changed and I[i]!=x: bad.append(('unexpected change',i))
for i in changed:
    x=I[i]
    for l in x.get('link',[]) or []:
        if l not in I: bad.append(('link missing',i,l))
    if x['k']=='ret':
        for e in x['el']:
            if e.get('cu') and e['cu'] not in x['ctx']: bad.append(('cu not in ctx',i,e['n']))
            if not all(hits(e['a'],e['kw'])) : bad.append(('model answer not detected',i,e['n'],e['a']))
            for w in e.get('ban',[]):
                if all(hits(w,e['kw'])): bad.append(('ban word passes kw',i,e['n'],w))
        # 실제 답안 재채점
        A=[a for a in st['ans'].get(i,[]) if a['t']>1794711600000]
        for a in A[:1]:
            bh=[all(hits(a['a'],e['kw'])) for e in B[i]['el']];ah=[all(hits(a['a'],e['kw'])) for e in x['el']]
            ch=[(e['n'],p,q) for e,p,q in zip(x['el'],bh,ah) if p!=q]
            print('RE-GRADE',i,'changed:',ch if ch else '없음')
    if x['k']=='kq':
        if not all(hits(x['a'],x['kw'])): bad.append(('kq answer kw',i))
for i in LOG['new']:
    x=I[i]
    if re.search(r'…|\.\.\.',x['a']): bad.append(('ellipsis',i))
    for k in x['ckw']:
        if k not in x['a']: bad.append(('ckw not in back',i,k))
    leak=[k for k in x['ckw'] if k in x['q'] and k not in ('관련성','변혁적')]
    print('NEW',i,'front leak check:',leak or '없음','| 학자명 질문:', bool(re.search(r'누구|학자(의|를)? ?(이름|명)',x['q'])))
for i in changed:
    if re.search(r'누구인가|학자(의 )?이름',I[i].get('q','')): bad.append(('asks scholar',i))
g=subprocess.run([sys.executable,'/workspace/edu/src/geo_guard.py'],capture_output=True,text=True);print(g.stdout.strip().splitlines()[-1])
print('PROBLEMS',len(bad));[print(' ',b) for b in bad]
