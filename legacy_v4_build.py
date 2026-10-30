import json,re
d=json.load(open('bank.json'));IT=d['items'];exec(open('split.py').read());CON=apply_split(d['con'],IT);CI={c['id']:c for c in CON}
exec(open('keep.py').read().split('def keep')[0])  # M list
M2=M+[('Eisner','cur_b'),('Taba','cur_b'),('인간중심 교육','cur_b'),('ASSURE','inst_b'),('선행조직자','inst_b'),('Gagné','gagne'),('수업사태','gagne'),('Jigsaw','coop'),('STAD','coop'),('CAT','eval_view'),('총평관','eval_view'),('측정관','eval_view'),('탈목표','emodel'),('CIPP','emodel'),('의사결정','adm_etc'),('쓰레기통','adm_etc'),('학교운영위원회','adm_etc'),('Hersey','lead_b'),('비공식','lead_b'),('Herzberg','motv_adm'),('Erikson','erik'),('Marcia','erik'),('Gardner','gard'),('다중지능','gard'),('Rogers','couns'),('REBT','couns'),('Glasser','couns'),('현실치료','couns'),('평등','equal'),('기능론','socio'),('문화실조','socio'),('문화다원','socio'),('Peters','phil'),('자유교육','phil'),('Vygotsky','vyg'),('ZPD','vyg'),('근접발달','vyg'),('Weiner','motiv'),('귀인','motiv'),('숙달목표','motiv'),('Katz','lead'),('분산적','lead'),('변혁적','lead'),('Weick','org'),('PBL','pbl'),('문제중심','pbl'),('Dick','isd'),('Keller','arcs'),('Bruner','exp'),('나선형','exp'),('지식의 구조','exp'),('Dewey','exp'),('광역형','exp'),('중핵','exp'),('공식적 교육과정','hid'),('영 교육과정','hid'),('Jackson','hid'),('정착','appr'),('상황학습','appr'),('인지적 유연성','appr'),('플립드','online'),('블렌디드','online'),('규준','ref'),('성장참조','ref'),('능력참조','ref'),('신뢰도','vr'),('객관도','vr'),('루브릭','perf'),('포트폴리오','perf'),('임상장학','sup'),('동료장학','sup'),('컨설팅','sup'),('Senge','lo'),('메타인지','ip'),('정교화','ip'),('부호화','ip'),('자기효능감','sr'),('Bandura','sr'),('Piaget','vyg'),('Mintzberg','org'),('관료제','org')]
old=json.load(open('/workspace/edu/old_items.json'))['items'];fl=json.load(open('/workspace/edu/flags.json'))
bad={'원문 빈칸 암기','맥락 없는 단편 정의','단답: 긴 답 한 표현만 인정','단답: 다항 나열을 단답으로','수치 단편'}
seen=set();shorts=[]
for x in old:
  if x['k']!='short' or set(fl.get(x['id'],[]))&bad or x['q'] in seen:continue
  if x['d']=='2022 개정':continue
  txt=x['q']+' '+x['a'];cid=next((v for k,v in M2 if k in txt),None)
  if not cid:continue
  seen.add(x['q'])
  kw=[[s for s in g.split('|') if s] for g in x['kw'].split(';') if g]
  if any(min(len(s) for s in g)<2 for g in kw):kw=[[x['a'].split('(')[0].strip()]]+[g for g in kw if min(len(s) for s in g)>=2]
  shorts.append(dict(id=x['id'],k='short',c=cid,d=CI[cid]['d'],g=x['g'],q=x['q'],a=x['a'],e=x.get('e',''),kw2=kw))
def fc(s):s=re.sub(r'\s','',s);return f"첫 글자 '{s[0]}', {len(s)}자"
assign(shorts)
for x in IT+shorts:x.pop('_as',None);x['d']=CI[x['c']]['d']
# flashcards v6 (hand-written pairs + natural fronts + leak QA)
exec(open('pairs.py').read());exec(open('fq.py').read());exec(open('hj.py').read());exec(open('dffix.py').read());exec(open('hjn.py').read());exec(open('v15c.py').read());exec(open('hjw.py').read());KEEP_PAIRS|={'pbl','online','adm_etc','vyg','emodel'}
def jo(w,a,b):
  w=re.sub(r'\([^)]*\)$','',w.strip()).strip(" '」\"")
  ch=w[-1] if w else '가'
  if '가'<=ch<='힣':return a if (ord(ch)-0xAC00)%28 else b
  return b if ch.lower() in 'aeiouwy' else a
def core(k):
  k=re.sub(r'^[①-⑨]\s*','',re.sub(r'^(도입|전개|정리|인간상|역량):\s*','',k));k=re.sub(r'^[①-⑨]\s*','',k)
  k=re.sub(r'^[가-사]\s(?=\S)','',k);k=re.sub(r'^([A-Z])\s(\S+)$',r'\2(\1)',k);return k
def bold1(df):
  m=re.split(r'[,;:→(.]| - ',df)[0].strip()
  return df.replace(m,f'**{m}**',1) if 2<=len(m)<=24 else df
GEN={'특징','성격','한계','효용성','수업 적용','비교','대표 모형','방법','교수·학습 원칙','재구성 근거','과정','문제','학습자 역할','교사 역할','6가지 이해','수직적 연계성','기능'}
SN={'hid':'교육과정 유형론','tyler':'Tyler의 합리적 모형','exp':'교육과정 사조','walker':'Walker의 숙의 모형','snyder':'Snyder의 교육과정 실행 관점','sbcd':'Skilbeck의 학교중심 교육과정 개발','bwd':'백워드 설계','cle':'Jonassen의 구성주의 학습환경(CLE)','pbl':'문제중심학습(PBL)','online':'온라인 수업','arcs':'Keller의 ARCS 모형','gagne':'Gagné의 9가지 수업사태','coop':'협동학습','form':'평가 시기에 따른 유형','ref':'평가 참조틀','vr':'검사 양호도','perf':'수행평가·과정 중심 평가','org':'학교 조직론','lead':'지도성 이론','ip':'정보처리이론','vyg':'Vygotsky 이론','k_human':'2022 개정 교육과정','k_focus':'2022 개정 교육과정 구성의 중점','k_eval':'2022 개정 교육과정의 평가','k_auto':'2022 개정 교육과정 편성·운영','integ':'통합 교육과정','plan':'교육기획','gard':'Gardner의 다중지능 이론','phil':'자유교육론','k_match':'2022 총론 지문 해석'}
def sn(c):return SN.get(c['id'],re.sub(r'\(([^)]*)\)$',r'(\1)',c['n']))
def pair_sub(p):
  subs=SPLIT[p[0]];t=p[2]+p[3]+p[1]
  sc=[(sum(t.count(k) for k in s[3]),-i,s[0]) for i,s in enumerate(subs)];return max(sc)[2]
cards=[];QA=[]
def card(c,n,q,a,e='',hl=None,t='',kw=(),cmp=None,h=None):
  cards.append(dict(id=f"v4{c['id']}k{n}",k='card',c=c['id'],d=c['d'],g=c['g'],q=q,a=a,e=e,hl=hl,t=t,ckw=list(kw),cmp=cmp,h0=h))
for c in CON:
  n=0;F_=c['f'];cores=[re.split(r'[(（]',core(r['k']))[0].strip() for r in F_]
  sq=SQ2.get(c['id']) if c.get('parent') else SQ.get(c['id'])
  if sq and len(F_)>1:card(c,n,sq,'\n'.join(f"**{core(r['k'])}** — {first_line(r['df'])}" for r in F_),c.get('core',''),t='전체 구조',kw=[x for x in cores if x not in GEN],
       h=[f"영역: {c['d']} · 출처: {c['src']}",f"{len(F_)}가지 · 첫 글자: "+' / '.join(x[:1]+'…' for x in cores),f"하나 공개: {core(F_[0]['k'])}"]);n+=1
  N=sn(c)
  for r,cr in zip(F_,cores):
    lab=core(r['k'])
    q=FQ[c['id']+'|'+r['k']]
    _ck=[t.strip() for t in re.split(r'[,·:/()→+.;]|\s-\s',r['df']) if len(t.strip())>=3 and t.strip() not in r['k'] and t.strip() not in c['n']]
    card(c,n,q,bold1(r['df']),('수업 적용: '+r['u']) if r['u'] else '',hl=r['k'],t='구성요소',kw=_ck,
         h=[f"영역: {c['d']} · 개념: {N}","핵심어 첫 글자: '"+re.split(r'[,;:→( ]',r['df'])[0][:1]+"'",f"답안 항목 수: 약 {max(1,len(_ck))}개"]);n+=1
  L22N={'hid':'잠재적·영 교육과정','exp':'경험중심·학문중심 교육과정','form':'진단·형성·총괄평가','lead':'학교 지도성 이론','org':'학교 조직의 특성','vr':'검사의 타당도·신뢰도','perf':'수행평가','ref':'평가 참조틀','online':'온라인 수업의 상호작용'}
  has22=any(x['c']==c['id'] and x['k']=='essay' and '2022' in x['q'] for x in IT)
  if c.get('l22') and c['g']!='B' and not c['id'].startswith('k_') and not has22:
    nm=L22N.get(c['id']) or re.sub(r'\([^)]*\)','',c['n']).split(':')[0].strip()
    card(c,n,f"{nm}{jo(nm,'을','를')} 2022 개정 교육과정과 연결해 서술하면?",bold1(c['l22']),'',t='2022 연계',
         h=[f"영역: {c['d']}","2022 총론 문서 위치: 구성의 중점·교수학습·평가 중 하나","앞부분: "+c['l22'][:max(3,len(c['l22'])//5)]+'…']);n+=1
  for x in IT:
    if x['c']==c['id'] and x['k']=='essay':
      m=x['model'];kws=[]
      for g in x['kw']:
        hit=next((t for t in g if t in m),None)
        if hit:m=m.replace(hit,f'**{hit}**',1);kws.append(hit)
      card(c,n,x['q'],m,'',hl=x.get('hl'),t=x.get('t','') or '논술',kw=[k for k in kws if k not in x['q']],
           h=[f"필수 핵심어 {i+1}: 첫 글자 '{k[0]}', {len(k)}자" for i,k in enumerate(kws)] or [f"영역: {c['d']}"]);n+=1
  for p in [p for p in P if ((p[0]==c['id'] and not c.get('parent')) or (c.get('parent')==p[0] and pair_sub(p)==c['id'])) and (p[0] in KEEP_PAIRS or c['id'] in KEEP_PAIRS)]:
    _,q,A,B,Ad,Bd,Ax,Bx,Ac,Bc=p
    card(c,n,q,f"**{A}**: {Ax}\n**{B}**: {Bx}",'',t='비교(빈출)',kw=[],cmp=dict(h=[A,B],r=[['정의',Ad,Bd],['핵심 차이',Ax,Bx],['구별 단서',Ac,Bc]]),
         h=[f"영역: {c['d']}",f"{A} 쪽 핵심어 첫 글자: '"+re.sub(r'["“”\s]','',Ax)[:1]+"'",f"{B}의 구별 단서: {Bc}"]);n+=1
def _x():pass
for i,(cid,q,a,e) in enumerate(EX):
  c=CI[cid];card(c,900+i,q,a,e,t='핵심 인출',h=[f"영역: {c['d']} · 개념: {sn(c)}","답의 첫 글자: '"+re.sub(r'[*\s]','',a)[:1]+"'"])
TO={'전체 구조':0,'구성요소':1,'핵심 인출':3,'비교(빈출)':4,'2022 연계':5}
def score(c):
  ny=len(re.findall(r'\d{2}',c['src'].split('/')[0])) if '논술' in c['src'] else 0
  return {'S':3,'A':2,'B':1}[c['g']]*1000+ny*60+MCQ.get(c['id'],0)+HJC.get(c['id'],0)*60
for x in cards:
  c=CI[x['c']];ny=re.search(r'논술[^/]*',c['src']);m=MCQ.get(c['id'])
  x['basis']=' · '.join(filter(None,[f"{c['g']}등급",('논술 기출 '+'·'.join('20'+y for y in re.findall(r'\d{2}',ny.group(0)))+'년' if re.findall(r'\d{2}',ny.group(0)) else ny.group(0).strip()) if ny else '논술 미출제',f"객관식 기출 약 {m}문항" if m else '',f"홍지완 출제표 {HJC[c['id']]}회" if c['id'] in HJC else '']))
  x['_s']=(-score(c),c['id'],TO.get(x['t'],2))
from fronts_rw import RW
_seen=set();_cc=[]
for x in cards:
  x['q']=RW.get(x['q'],x['q'])
  if (x['c'],x['q']) in _seen: continue
  _seen.add((x['c'],x['q']));_cc.append(x)
cards[:]=_cc
_mw=0
for x in cards:
  m=MODW.get(x['q'])
  if m:
    if m[0]:x['a']=m[0]
    x['e']=(x['e'] or '')+m[1];_mw+=1
print('MODW',_mw,len(MODW))
cards.sort(key=lambda x:x['_s'])
for i,x in enumerate(cards):x['r']=i;x.pop('_s')
# QA: answer leak on front, unnatural template residue
for x in cards:
  q=re.sub(r'\s','',x['q'])
  for k in [k for k in x['ckw'] if k not in ALLOW]:
    if len(k)>=2 and re.sub(r'\s','',k) in q:QA.append(('LEAK',x['id'],k,x['q']))
  if re.search(r'[가-힣]\((이|가|을|를|은|는)\)|왜 틀릴까|혼동 주의',x['q']):QA.append(('TEMPLATE',x['id'],x['q']))
  if x['t']=='혼동 비교':
    for k in [x['cmp']['r'][1][1],x['cmp']['r'][1][2]]:
      kk=re.findall(r'"([^"]+)"',k)
      for t in kk:
        if any(re.sub(r'\s','',t) in re.sub(r'\s','',z) for z in x['cmp']['h']):continue
        if re.sub(r'\s','',t) in q:QA.append(('LEAK',x['id'],t,x['q']))

exec(open('yb.py').read());_yn={}
for cid,ctx,q,kw,model,sr in YB:
  c=CI[cid];n=_yn.get(cid,0);_yn[cid]=n+1;K=[[a for a in g.split('|') if a] for g in kw.split(';')]
  ny=re.findall(r'\d{2}',c['src'].split('/')[0]) if '논술' in c['src'] else []
  src='교재 표준(핵심정리)' if sr=='T' or not ny else '논술 기출 '+'·'.join('20'+y for y in ny)+'년 개념'
  if f'yb{cid}{n}'=='ybdick0':src+=' · 사용자 키워드 노트(평가도구 선행개발)로 확인'
  it=dict(id=f"yb{cid}{n}",k='prob',c=cid,d=c['d'],g=c['g'],ctx=ctx,q=q,kw=K,model=model,need=max(2,round(len(K)*0.6)),src=src)
  zq=re.sub(r'\s','',q+ctx)
  K=[[a for a in g if re.sub(r'\s','',a) not in zq] for g in K if re.sub(r'\s','',g[0]) not in zq];K=[g for g in K if g];it['kw']=K;it['need']=max(2,round(len(K)*0.6))
  if len(K)<3:QA.append(('YBFEW',it['id'],K))
  shorts.append(it)

exec(open('v13d.py').read())
CONF={}
for p in P:
  cid=p[0];CONF.setdefault(cid,[]).append(dict(a=p[2],b=p[3],ax=p[6],bx=p[7],ac=p[8],bc=p[9]))
  par=CI[cid].get('parent')
for c in CON:
  if c.get('parent') and c['parent'] in CONF and c['id'] not in CONF:CONF[c['id']]=CONF[c['parent']]
_ALLANS={}
for x in IT:
  if x['k']=='case':
    for b in x['bl']:_ALLANS.setdefault(x['d'],[]).append((x['c'],b['a'][0]))
def _toks(c,ans=''):
  out=[];a0=re.sub(r'\s|\(.*?\)','',ans)
  R=[r for r in c['f'] if a0 and (a0 in re.sub(r'\s','',r['k']) or re.sub(r'\s|\(.*?\)|^[①-⑨]','',r['k']) in a0)] or ([c['f'][0]] if len(c['f'])==1 else [])
  for r in R:
    for t in re.split(r'[,·:/()→+.;\s"“”]|\s-\s',r['df']):
      t=t.strip()
      if 2<=len(t)<=8 and t not in out and t[-1] not in '의에을를은는이가과와아고지서도며면' and t not in ('학교','학생','교사','조직','계획','목표','수업','교육','사회','교과','학습','개념','특징','장점','단점','통해','중심으로','교육과정','분석','내용','방법','과정','관점','지식','정도','능력'):out.append(t)
  return out
for x in IT:
  if x['k']!='case':continue
  c=CI[x['c']];sib=[b['a'][0] for b in x['bl']]
  for i,b in enumerate(x['bl']):
    m=re.match(r'^\s*([㉠-㉯]|\([가-하]\))',b['l'])
    if not m:continue
    lab=m.group(1);ans=b['a'][0];al={re.sub(r'\s','',a) for a in b['a']}
    if re.sub(r'\s','',ans) in re.sub(r'\s','',x['ctx']):continue
    cand=[a for a in sib if a!=ans]+[z for p in CONF.get(x['c'],[]) for z in (p['a'],p['b'])]+[a for cc,a in _ALLANS[x['d']] if cc==x['c']]+[a for cc,a in _ALLANS[x['d']]]
    ds=[]
    for a in cand:
      k=re.sub(r'\s|\(.*?\)','',a)
      if len(k)<=2 or k in {re.sub(r'\(.*?\)','',z) for z in al} or any(k==re.sub(r'\s|\(.*?\)','',d) for d in ds) or len(a)>24:continue
      ds.append(a)
      if len(ds)==3:break
    if len(ds)<3:continue
    why={w['a']:w['why'] for w in x.get('wr',[]) if w['a'] in ds}
    sents=[t for t in re.split(r'(?<=[.!?다])\s+',x['ctx']) if lab in t]
    cl=[t for t in _toks(c,ans) if any(t in z for z in sents) and t not in ('위해','함께','만들어','확인','최소','과목별','인정','책임') and re.sub(r'\s','',t) not in al][:6]
    shorts.append(dict(id=f"{x['id']}d{i}",k='disc',c=x['c'],d=x['d'],g=x['g'],ctx=x['ctx'],lab=lab,q=f"제시문의 {lab}에 해당하는 개념은 무엇인가?",a=ans,acc=b['a'],x=ds,why=why,clue=cl,sent=sents,hj=x.get('hj')))
for cid,(q,a) in L22B.items():
  c=CI[cid];shorts.append(dict(id=f"l22{cid}",k='l22',c=cid,d=c['d'],g=c['g'],q=q,a=a,src=c['l22']))
for pid,q,a,ex in PAT:
  shorts.append(dict(id=pid,k='pat',c='k_focus',d='2022 개정',g='S',q=q,a=a,ex=ex,src='교재 표준(논술 답안 작성 일반 원칙)'))
exec(open('wt.py').read())
_A4=['교육과정','교수·공학','교육평가','교육행정'];_PP={a:sorted([y for y in shorts if y['k']=='prob' and (y['d']==a or (a=='교수·공학' and y['d']=='교육심리'))],key=lambda y:(not y['ctx'],not y.get('hj') and y['c'] not in HJTAG,y['g'],y['id'])) for a in _A4}
SETS=[]
for i in range(min(len(v) for v in _PP.values())):
  SETS.append(dict(id=f"set{i+1}",sub=[_PP[a][i]['id'] for a in _A4],areas=[_PP[a][i]['d'] for a in _A4]))
for z in QA:print(*z)
ALL=IT+shorts+cards
for x in ALL:
  if x['c'] in HJTAG or x.get('q') in HJQ or x.get('hj'):x['hj']=1
for x in ALL:
  if x['d']=='2022 개정' or x['id'].startswith('k22') or '2022' in (x.get('t') or '') or (x['k'] in('struct','card','essay','prob') and '2022' in x.get('q','')):x['x22']=1
# hints
def leak(h,ans):
  return any(len(a)>=2 and re.sub(r'\s','',a) in re.sub(r'\s','',h) for a in ans)
for x in ALL:
  c=CI[x['c']];k=x['k'];H=[]
  if k=='case':
    H=[f"영역: {c['d']} · 관련 기출/출처: {c['src']}"," · ".join(f"{b['l'][:1]} {fc(b['a'][0])}" for b in x['bl']),"서술 핵심어: "+', '.join(g[0] for g in x['kw'][:2])]
    ans=[a for b in x['bl'] for a in b['a']]
  elif k=='essay':
    H=[f"필수 핵심어 {i+1}: {g[0]}" for i,g in enumerate(x['kw'])];ans=[]
  elif k=='mcq':
    H=[f"영역: {c['d']} · 개념: {c['n']}","❌ 제외: "+x['x'][0],"❌ 제외: "+x['x'][1]];ans=[x['a']]
    x['hx']=[None,x['x'][0],x['x'][1]]
  elif k=='struct':
    H=[f"{len(x['p'])}가지 · {x.get('ct','')}","첫 글자: "+' / '.join(re.sub(r'\s','',p['k'])[:1]+'…' for p in x['p']),"하나 공개: "+x['p'][0]['k']];ans=[]
  elif k=='frame':
    H=[f"구성요소 {len(c['f'])}가지","첫 글자: "+' / '.join(re.sub(r'\s','',r['k'])[:2]+'…' for r in c['f']),"하나 공개: "+c['f'][0]['k']];ans=[]
  elif k=='card':
    H=x.pop('h0');ans=[t for t in x['ckw'] if len(t)>=2 and t not in ALLOW]
  elif k=='prob':
    K=x['kw'];H=[f"채점 핵심어 {len(K)}개 · 통과 기준 {x['need']}개 · 근거: {x['src']}","첫 글자: "+' / '.join(re.sub(r'\s','',g[0])[:1]+'…' for g in K),"핵심어 2개 공개: "+', '.join(g[0] for g in K[:2])];ans=[]
  elif k=='disc':
    H=[f"영역: {c['d']}",f"단서 문장 수: {len(x['sent'])} · 단서어 {len(x['clue'])}개가 지문에 있음"];ans=[x['a']]
  elif k=='wt':
    H={'fix':['고칠 곳 유형: '+x['t'].split('· ')[-1]],'frm':['틀: '+x.get('tpl','')],'ord':[f"문장 {len(x.get('seq',[]))}개 · 서론 1 → 본론 → 결론 1"],'out':[f"논점 {len(x.get('ol',[]))}개로 나누기"]}[x['s']];ans=[]
  elif k=='l22':
    H=[f"영역: {c['d']}","총론 핵심 표현: "+x['src'].split(',')[0]];ans=[]
  elif k=='short':
    a=x['a'];z=re.sub(r'\s','',a);H=[f"영역: {c['d']} · 개념 범주: {c['n']}",fc(a)]
    if len(z)>=5:H.append("앞부분: "+(z[:2] if len(z)<=20 else re.sub(r'\s+',' ',a)[:len(a)//4])+'…')
    ans=[a] if len(z)<=20 else []
  for i,h in enumerate(H):
    if k=='card' and x['t']=='전체 구조' and i==2:continue
    if ans and leak(h,ans):
      H[i]=f"영역: {c['d']}" if i==0 else H[i]
      if leak(H[i],ans):raise SystemExit(f'LEAK {x["id"]} {H[i]}')
  x['h']=H
d=dict(con=CON,items=ALL,sets=SETS,conf=CONF)
from collections import Counter
print(len(ALL),Counter(x['k'] for x in ALL))
s=open('head.html').read()+'const DATA='+json.dumps(d,ensure_ascii=False)+';\n'+open('top.js').read()+open('mid.js').read()+open('v13.js').read()+open('v16.js').read()+open('bot.js').read()
open('index.html','w').write(s);json.dump(d,open('final.json','w'),ensure_ascii=False)
