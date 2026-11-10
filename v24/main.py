import json,re,sys,difflib,copy
sys.path.insert(0,'/workspace/edu/v24')
from dups import MANUAL
from overrides import Q as QO,A as AO,UNSURE,HM
from fronts_struct import SQ
SRC='/workspace/edu/src/items.json'
d=json.load(open(SRC));IT=d['items'];I={x['id']:x for x in IT};CON={c['id']:c for c in d['con']};CONF=d['conf']
orig=copy.deepcopy(I)
LOG={'dup':[],'merge':[],'front':[],'hint':0,'hint_items':[]}

def strip_b(s):return re.sub(r'\*\*','',s or '')
def ans_text(x):
  if x['k']=='struct':return ' / '.join(p['k']+': '+p['s'] for p in x['p'])
  return x.get('a') or x.get('model') or ''
STOPT=set('있다 한다 하는 것이다 것을 것은 위해 통해 이다 에서 으로 하고 하며 등의 수업 학생 교사 학교 교육 학습 평가 개념 특징 기능 원리 방법 단계 관점 내용 목표 그리고 있는 없는 대한 따라 함께 각각 가지 홍지완 강의 필기 사용자 노트 출처 기출 논술 교재 표준'.split())
def toks(s):return set(w for w in re.findall(r'[가-힣A-Za-z0-9]{2,}',strip_b(s)) if w not in STOPT)

# ---------- 1. 중복 처리 ----------
# 자동: 같은 개념에서 앞면이 같은 essay ↔ card 쌍 → card를 essay로 합침
by=[x for x in IT if x['k']=='essay']
for e in by:
  for x in IT:
    if x['k']=='card' and x['c']==e['c'] or (x['k']=='card' and x['q']==e['q']):
      if x['k']=='card' and x['q'].strip()==e['q'].strip() and x['id'] not in MANUAL:
        MANUAL[x['id']]=e['id']
# 모든 essay와 앞면이 같은 card (개념 id가 달라도)
for x in IT:
  if x['k']=='card' and x['id'] not in MANUAL:
    for e in by:
      if x['q'].strip()==e['q'].strip():MANUAL[x['id']]=e['id']
for dup,can in MANUAL.items():
  assert dup in I and can in I,(dup,can)
  assert can not in MANUAL,(can,'canon is dup')
  D,C=I[dup],I[can]
  D['dup']=can;C.setdefault('merged',[]).append(dup)
  LOG['dup'].append((dup,can))
  if can in AO:continue
  if C['k']=='struct' and D['k']=='struct':
    have={re.sub(r'\W','',p['k']) for p in C['p']}
    for p in D['p']:
      kn=re.sub(r'\W','',p['k'])
      if not any(kn in h or h in kn for h in have):
        C['p'].append(p);LOG['merge'].append((dup,can,'p+ '+p['k']))
    continue
  new=toks(ans_text(D))-toks(ans_text(C))-toks(C.get('q',''))-toks(C.get('e',''))
  if len(new)>=2:
    add=strip_b(ans_text(D)).replace('\n',' / ').strip()
    if C['k'] in('card','short'):
      C['a']=C['a'].rstrip()+('\n' if C['k']=='card' else ' / ')+('**함께 정리** — ' if C['k']=='card' else '함께 정리: ')+add
    elif C['k']=='essay':
      C['model']=C['model'].rstrip()+' (함께 정리: '+add+')'
    elif C['k']=='struct':
      C.setdefault('note',[]).append(add)
    LOG['merge'].append((dup,can,'+'+add[:60]))
# ---------- 2. 앞면·뒷면 제자리 수정 ----------
for k,v in QO.items():
  LOG['front'].append((k,I[k]['q'],v));I[k]['q']=v
for k,v in AO.items():I[k]['a']=v
for k,v in SQ.items():
  LOG['front'].append((k,I[k]['q'],v));I[k]['q']=v
# ---------- 3. 힌트 ----------
LABW=set('개념 정의 특징 장점 단점 한계 효과 예 사례 목적 원리 방법 절차 비판 시사점 기능 목표 내용 평가 차이 구조 조직 방식 의의 문제 역할 기준 함께 정리 원천 체 범위 계기 양상 근거 배경 가정 순기능 역기능 공통 관련 영역 지속성 가치 방향 통제 가능성 최저 최고 도입 전개 정리 장점 단점 학습자 교사 분석 설계 개발 실행 이론 대표 사례 핵심'.split())
STOPM=set('교육과정 교육 평가 이론 모형 학습 수업 교사 학생 학교 개념 원리 관점 단계 방법 기능 특징 지도성 장학 역량 지능 전략 요소 목표 내용 조직 과정 활동 결과 능력 가치 태도 사회 문제 경험 지식 관계 상황 정보 도구 구조 형식 기준 참여 자율성 전문성 영역 방식 효과 사람 개인 집단 문화 행동 신념 성취 동기 자아 의미 체제 관리'.split())
def splitterms(s):
  s=strip_b(s);out=set()
  for t in re.split(r'[,/·→()\[\]「」"“”‘’\'·:;=+]|\s-\s|\s—\s|\n| 및 | 또는 | 와 | 과 ',s):
    t=t.strip(' .~-—①②③④⑤⑥⑦⑧⑨')
    if 2<=len(t)<=30:out.add(t)
  return out
def bolds(s):return [b for b in re.findall(r'\*\*(.+?)\*\*',s or '')]
def is_label(b):return strip_b(b).strip(' :') in LABW or re.fullmatch(r'[①-⑨0-9 ]+',b) is not None
def mterms(x):
  T=set()
  k=x['k']
  if k=='card':
    for b in bolds(x['a']):
      if not is_label(b) and (strip_b(b) not in x.get('q','') or re.search(r'중 (어디|어느|무엇|하나)|어느 쪽|어디에 해당',x.get('q',''))):T|={b}|splitterms(b)
    for c in x.get('ckw') or []:T|={c}|splitterms(c)
  if k=='short':
    T|={x['a']}|splitterms(x['a'])
    for g in x.get('kw2') or []:T|=set(g)
  if k=='disc':T|={x['a']}|splitterms(x['a'])|set(x.get('acc') or [])
  if k=='case':
    for b in x['bl']:
      for a in b['a']:T|={a}|splitterms(a)
  if k in('essay','prob','case'):
    for g in x.get('kw') or []:T|=set(g)
  if k=='struct':
    for p in x['p']:T|={p['k']}|splitterms(p['k'])
  if k=='l22':
    src=x.get('src','');T|=splitterms(src.split('→')[0]) if '→' in src else splitterms(src)
  # 정제
  out=set()
  for t in T:
    t=t.strip()
    if len(t)<2 or t in STOPM or t in LABW:continue
    out.add(t)
    t2=re.sub(r'\(.*?\)','',t).strip()
    if len(t2)>=2 and t2 not in STOPM:out.add(t2)
  return out
def mask(s,T):
  s=strip_b(s)
  for t in sorted(T,key=len,reverse=True):
    if len(t)<2:continue
    s=s.replace(t,'○○')
  s=re.sub(r'(○○[\s·,]*){2,}',lambda m:'○○'+(' · ○○' if m.group(0).count('○○')>1 and ('·' in m.group(0) or ',' in m.group(0)) else ''),s)
  return s
def masked_ratio(s):
  return s.count('○○')*2/max(1,len(s))
def short(s,n=240):
  s=re.sub(r'\s+',' ',s).strip()
  return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+' (이하 생략)'
def leak(s,T):
  return any(t in s for t in T if len(t)>=3 and t not in STOPM)

# 개념 틀 사전
GL={}
for c in d['con']:
  for f in c['f']:
    for nm in {f['k'],re.sub(r'\(.*?\)','',f['k']).strip()}:GL.setdefault(nm,(f['df'],f.get('u'),c['id']))
for x in IT:
  if x['k']=='short' and x.get('a') and len(x['a'])<25 and not re.search(r'[,/→]',x['a']):
    q=re.sub(r'(은|는|란|이란)\s*(무엇인가|무엇이라 하는가)?\?$','',x['q']).strip()
    nm=re.sub(r'\(.*?\)','',x['a']).strip()
    if len(q)>12 and nm not in GL:GL[nm]=(q,None,x['c'])
def comp(x):
  c=CON.get(x['c']);
  if not c:return None,None
  names=[]
  if x.get('hl'):names.append(x['hl'])
  if x['k']=='short':names.append(x['a'])
  for f in c['f']:
    kn=re.sub(r'\(.*?\)','',f['k']).strip()
    for n in names:
      if n and (kn in n or n.split('(')[0].strip() in f['k']):return c,f
  q=x.get('q','')
  for f in sorted(c['f'],key=lambda f:-len(f['k'])):
    kn=re.sub(r'\(.*?\)','',f['k']).strip()
    if len(kn)>=2 and kn in q:return c,f
  return c,None
def partner(x,c,f,T):
  # 혼동 짝: conf → cmp → 같은 틀의 이웃 구성요소
  A=f['k'] if f else (x.get('hl') or '')
  for p in CONF.get(x['c'],[]):
    for a,b,bx in((p['a'],p['b'],p['bx']),(p['b'],p['a'],p['ax'])):
      an=re.sub(r'\(.*?\)','',a).strip()
      if A and (an in A or A.split('(')[0].strip() in a):
        return b,bx+(' — 예: '+p['bc' if b==p['b'] else 'ac'] if p.get('bc') else '')
  if c and f and len(c['f'])>1:
    i=c['f'].index(f);g=c['f'][i+1] if i+1<len(c['f']) else c['f'][i-1]
    return g['k'],g['df']
  return None,None
def josa(w,a,b):
  ch=strip_b(w).rstrip(' )"\'')[-1:] if w else ''
  if ch and '가'<=ch<='힣':return a if (ord(ch)-0xAC00)%28 else b
  return a+'('+b+')' if a!=b else a
def H(*hs,T=set()):
  out=[]
  for h in hs:
    if not h:continue
    h=re.sub(r'\s*·?\s*v\d+[^·/]*?보강\)?','',h)
    h=short(h)
    body=h.split(' — ',1)[-1]
    if masked_ratio(body)>0.45 or len(re.sub(r'[○\s·,/]','',body))<4:continue
    if leak(h,T):continue
    if h not in out:out.append(h)
  return out
def cloze(text,T):
  m=mask(text,T)
  if m.count('○○')/max(1,len(m.split()))>0.35:
    h=half(text,T)
    if h:return h.split(' — ',1)[1]
  if m==strip_b(text):
    ws=sorted({w for w in re.findall(r'[가-힣A-Za-z]{3,}',m) if w not in STOPT and w not in STOPM},key=len,reverse=True)[:3]
    for w in ws:m=m.replace(w,'○○')
  return m.replace('\n',' / ')
def sentences(s):
  return [t.strip() for t in re.split(r'(?<=[\.\?!])\s+',strip_b(s)) if len(t.strip())>8]
def apply_u(c,f,T):
  if f and f.get('u'):return '수업 장면 — '+mask(re.sub(r'\s*·?\s*v\d+[^·/]*?보강','',f['u']),T)
  return None
def core_h(c,T,lab='개념 틀'):
  if c and c.get('core'):return lab+' — '+mask(c['core'],T)
  return None

def host_h(x,c,items,T):
  if not c:return None
  for f in c['f']:
    hit=sum(1 for t in items if len(t)>=2 and t in f['df'])
    if hit>=max(1,len(items)//2):return '개념 틀 속 위치 — '+f['k']+': '+mask(f['df'],T|set(items))
  return None
def half(text,T):
  t=strip_b(text).replace('\n',' / ')
  parts=re.split(r'(\s*(?:,|/|→|·)\s*)',t)
  items=[i for i in range(0,len(parts),2) if len(parts[i].strip())>=2]
  if len(items)<2 or (len(items)==2 and '/' not in t):return None
  for n,i in enumerate(items):
    if n%2==1:parts[i]='○○'
  return '절반 공개(나머지를 떠올리기) — '+''.join(parts)
def sib_h(x,T):
  best=None;bs=0;qa=toks(x.get('q',''))
  for y in IT:
    if y is x or y['c']!=x['c'] or y.get('dup') or y['k'] not in('card','short') or not y.get('a'):continue
    if strip_b(y['a'])==strip_b(x.get('a','')):continue
    sc=len(qa&toks(y['q']))
    if sc>bs:bs,best=sc,y
  if best and bs>=2:
    a2=re.split(r'\n',strip_b(best['a']))[0]
    return f"비슷한 질문과 구별 — '{best['q']}'의 답은 {mask(a2,T)}. 이 문항은 그것과 무엇이 다른가?"
  return None
def gen(x):
  k=x['k'];T=mterms(x);c,f=comp(x)
  if k=='card':
    e=x.get('e') or ''
    ctx=None
    if e.startswith('수업 적용'):ctx='수업 장면 — '+mask(e.split(':',1)[-1].strip(),T)
    elif f and f.get('u') and x.get('t')!='전체 구조':ctx=apply_u(c,f,T)
    con=None
    if x.get('cmp'):
      h0,h1=x['cmp']['h'];r=x['cmp']['r'][0]
      con=f"비교 축 — '{r[0]}'에서 {h0}{josa(h0,'은','는')} {mask(r[1],T)}, {h1}{josa(h1,'은','는')} {mask(r[2],T)}"
    else:
      b,bd=partner(x,c,f,T)
      if b and not any(t in b for t in T if len(t)>=3):con=f"헷갈리는 짝과 구별 — {b}{josa(b,'은','는')} {mask(bd,T)}"
    if x.get('t') in('전체 구조','비교(빈출)'):
      hs=H(core_h(c,T),'정의를 보고 이름 떠올리기 — '+cloze(x['a'],T),T=T)
    elif x.get('t')=='2022 연계':
      hs=H(core_h(c,T,'이론 쪽 핵심'),'총론 연결 방향 — '+cloze(x['a'],T),T=T)
    else:
      hs=H(ctx,con,'답의 뼈대(핵심어 가림) — '+cloze(x['a'],T),T=T)
      if len(hs)<2:hs=H(ctx,con,core_h(c,T),sib_h(x,T),'답의 뼈대(핵심어 가림) — '+cloze(x['a'],T),half(x['a'],T),T=T)[:3]
    if len(hs)<2:hs=H(*(hs+[sib_h(x,T),half(x['a'],T)]),T=T)[:3]
    return hs
  if k=='short':
    a=x['a'];items=[t.strip() for t in re.split(r'[,/→]|·(?=[가-힣])',re.sub(r'\(.*?\)','',a)) if t.strip()]
    if len(items)>=2:
      defs=[]
      for i,t in enumerate(items):
        g=GL.get(t) or next((v for kk,v in GL.items() if len(t)>=2 and (kk.startswith(t) or t.startswith(kk)) and len(kk)>=2),None)
        if g:defs.append(f"{'①②③④⑤⑥⑦⑧⑨'[i] if i<9 else i+1} {mask(g[0],T)}")
      h1=('항목별 설명 — '+' '.join(defs)) if len(defs)>=2 else None
      hs=H(h1,host_h(x,c,items,T),core_h(c,T),('보충 단서 — '+mask(x['e'],T)) if x.get('e') else None,T=T)[:3]
      if len(hs)<2:hs=H(*(hs+[half(a,set())]),T=set())[:3]
      return hs
    b,bd=partner(x,c,f,T)
    con=f"헷갈리는 짝과 구별 — {b}{josa(b,'은','는')} {mask(bd,T)}" if b and not any(t in b for t in T if len(t)>=3) else None
    g=GL.get(re.sub(r'\(.*?\)','',a).strip())
    df=('정의로 다시 보기 — '+mask(g[0],T)) if g and difflib.SequenceMatcher(None,g[0],x['q']).ratio()<.6 else None
    hs=H(con,apply_u(c,f,T),('보충 단서 — '+mask(x['e'],T)) if x.get('e') else None,df,core_h(c,T),T=T)[:3]
    if len(hs)<2:hs=H(*(hs+[sib_h(x,T)]),T=T)[:3]
    return hs
  if k=='struct':
    out=[]
    for i,p in enumerate(x['p'][:6]):
      out.append(f"{i+1}번 항목의 설명 — "+mask(p['s'],T))
    return H(*out,T=T)
  if k=='frame':
    c=CON[x['c']];T={f['k'] for f in c['f']}
    for f in c['f']:T|=splitterms(f['k'])
    T={t for t in T if len(t)>=2 and t not in STOPM}
    return H(*[f"{i+1}번 구성요소의 정의 — "+mask(f['df'],T) for i,f in enumerate(c['f'][:7])],T=set())
  if k in('essay','prob'):
    ss=sentences(x['model'])
    if len(ss)==1 and len(ss[0])>70:
      cl=[t for t in re.split(r'(?<=[,，])\s+',ss[0]) if t.strip()]
      if len(cl)>=2:
        n=min(3,len(cl));step=-(-len(cl)//n);ss=[' '.join(cl[i:i+step]) for i in range(0,len(cl),step)]
        out=[f"모범 답안 {i+1}/{len(ss)}부분(핵심어 가림) — "+mask(s,T) for i,s in enumerate(ss)]
      else:out=["모범 답안(핵심어 가림) — "+mask(ss[0],T)]
    else:
      out=[f"모범 답안 {i+1}문장(핵심어 가림) — "+mask(s,T) for i,s in enumerate(ss[:3])]
    hs=H(*out,T=set())
    if not hs:hs=H(core_h(c,T),T=T)
    return hs
  if k=='case':
    out=[]
    lab='㉠㉡㉢㉣'
    for i,b in enumerate(x['bl']):
      w=[w for w in (x.get('wr') or []) if True]
    for w in (x.get('wr') or [])[:2]:
      out.append(f"혼동 주의 — '{mask(w['a'],T)}'{josa(w['a'],'이','가')} 아닌 이유: "+mask(w['why'],T))
    ss=sentences(x.get('model',''))
    if ss:out.append('서술 방향(핵심어 가림) — '+mask(ss[0],T))
    if len(out)<2:
      cc=core_h(c,T)
      if cc:out.insert(0,cc)
    return H(*out,T=set())[:3]
  if k=='disc':
    out=[]
    if x.get('sent'):out.append('지문에서 이 문장에 주목 — '+x['sent'][0])
    for o in x['x'][:2]:
      g=GL.get(re.sub(r'\(.*?\)','',o).strip()) or GL.get(o)
      if g:
        g0=re.split(r'\s(?=장점:|단점:|특징:|한계:)|(?<=다)\. ',re.sub(r'^개념:\s*','',g[0]))[0].rstrip('. ')
        out.append(f"보기 '{o}' 점검 — {o}{josa(o,'은','는')} {mask(g0,T)}. 지문 상황과 맞는가?")
    if len(out)<2:
      cc=core_h(c,T,'판별 기준')
      if cc:out.append(cc)
    return H(*out,T=T)
  if k=='mcq':
    out=[]
    cc=core_h(c,set(),'판별 기준')
    hx=x.get('hx') or []
    old=x['h']
    if old and not old[0].startswith('영역'):return None  # 손으로 쓴 힌트는 유지
    new=[cc] if cc else []
    new+=[h for h in old if not h.startswith('영역') and not h.startswith('❌')]
    for i in range(1,len(hx)):
      o=hx[i]
      if o is None:continue
      why=(x.get('why') or {}).get(o,'')
      new.append(f"❌ 제외: {o}"+(f" — {why}" if why else ''))
    x['hx']=[None]*(len(new)-sum(1 for h in new if h.startswith('❌')))+[h for h in hx[1:] if h is not None]
    return new
  if k=='l22':
    hs=H(core_h(c,set(),'이론 쪽 핵심'),'총론 연결 방향(총론 표현 가림) — '+mask(x.get('src',''),T),T=set())
    if len(hs)<2:hs=H(*(hs+['답 문장의 뼈대(총론 표현 가림) — '+mask(x['a'],T)]),T=set())
    return hs
  if k=='wt' and x.get('s')=='fix':
    q,a=x['q'],x['a'];sm=difflib.SequenceMatcher(None,q,a)
    seg=[q[i1:i2] for op,i1,i2,j1,j2 in sm.get_opcodes() if op in('replace','delete') and i2>i1]
    span=''
    if seg:
      ops=[(i1,i2) for op,i1,i2,j1,j2 in sm.get_opcodes() if op in('replace','delete','insert')]
      s0=min(o[0] for o in ops);s1=max(o[1] for o in ops)
      while s0>0 and q[s0-1]!=' ':s0-=1
      while s1<len(q) and q[s1] not in ' .':s1+=1
      span=q[s0:s1].strip()
    why=(x.get('why') or '').split('. ')[0]
    out=[]
    if span and len(span)<len(q)*0.8:out.append(f"문제가 있는 곳 — '{span}'")
    out.append(f"고칠 곳 유형 — {x['t'].split('·')[-1].strip()}"+(f": {why.rstrip('.')}." if why and not any(t in why for t in re.findall(r'[가-힣]{3,}',a) if t not in q) else ''))
    return out
  return None

MECH=re.compile(r'첫 글자|\d+자|앞부분|하나 공개|핵심어 \d+개 공개|필수 핵심어 \d|답안 항목 수|^영역:|단서 문장 수|채점 핵심어 \d+개|구성요소 \d+가지$|^\d+가지 ·|서술 핵심어|총론 핵심 표현|2022 총론 문서 위치|고칠 곳 유형')
for x in IT:
  old=x.get('h') or []
  if x['k'] in('pat',) or (x['k']=='wt' and x.get('s')!='fix'):continue
  new=gen(x)
  if new is None:continue
  keep=[h for h in old if not MECH.search(h) and not h.startswith('❌')] if x['k']!='mcq' else []
  new=new+[h for h in keep if h not in new]
  if not new:new=[h for h in old if not MECH.search(h)]
  if x['id'] in HM:new=list(HM[x['id']])
  if new!=old:
    LOG['hint']+=1;LOG['hint_items'].append(x['id'])
  x['h']=new
json.dump(d,open('/workspace/edu/v24/items.json','w'),ensure_ascii=False,indent=1)
json.dump(LOG,open('/workspace/edu/v24/log.json','w'),ensure_ascii=False,indent=1)
print('dups',len(LOG['dup']),'merges',len(LOG['merge']),'fronts',len(LOG['front']),'hints changed',LOG['hint'])
from collections import Counter
print(Counter(len(x['h']) for x in IT))
print('still mechanical',sum(1 for x in IT for h in x['h'] if MECH.search(h)))
