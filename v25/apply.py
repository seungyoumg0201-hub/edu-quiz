import json,re,sys,copy,collections
sys.path.insert(0,'/workspace/edu/v25')
from overrides import R
SRC='/workspace/edu/src/items.json'
d=json.load(open(SRC));IT=d['items'];I={x['id']:x for x in IT};CON={c['id']:c for c in d['con']}
orig=copy.deepcopy(I)
LOG=collections.defaultdict(list)
R['v4sbcdk5']['h']=["Skilbeck 모형의 마지막 단계. 결과를 다음 개발로 되돌려 보내는 순환 구조의 고리"]
# ---------- 1. 카드·단답 발문/뒷면 ----------
for i,v in R.items():
  x=I[i];assert x['k'] in('card','short'),(i,x['k'])
  kind=v['_kind']
  for f in('q','a','e','kw2'):
    if f in v:x[f]=v[f]
  if 'h' in v:x['h']=v['h']
  if kind=='conv' and x['k']=='card':
    nm=re.findall(r'\*\*(.+?)\*\*',x['a'])
    if nm:x['ckw']=[re.sub(r'\(.*?\)','',nm[0]).strip()]+[c for c in (x.get('ckw') or []) if c not in nm]
  LOG[kind].append(i)
# ---------- 2. 사례 판별(disc) 오답 보기: 범주 밖 채움 보기 → 같은 범주 혼동 개념 ----------
DX={
 'v4hidc0d0':['영 교육과정','공식적 교육과정','실천된 교육과정'],
 'v4hidc0d1':['잠재적 교육과정','공식적 교육과정','실천된 교육과정'],
 'v4hidc1d0':['영 교육과정','공식적 교육과정','실천된 교육과정'],
 'v4tylerc0d2':['학습 가능성의 원리와 일경험 다성과의 원리','계속성과 계열성','교육철학과 학습심리학'],
 'v4expc0d1':['경험중심 교육과정','나선형 교육과정','광역형'],
 'v4expc0d2':['경험중심 교육과정','중핵형','광역형'],
 'v4expmk1d0':['경험중심 교육과정','학문중심(Bruner)','인간중심 교육과정'],
 'v4integc0d0':['다학문적 통합','탈학문적 통합','광역형'],
 'v4integc0d1':['간학문적 통합','탈학문적 통합','광역형'],
 'v4integc0d2':['간학문적 통합','다학문적 통합','광역형'],
 'v4pblc0d1':['지식 전달자','강의자','감독자'],
 'v4onlinec0d0':['플립드 러닝','블렌디드 러닝','학습자-교수자 상호작용'],
 'v4onlinec0d1':['학습자-학습자 상호작용','블렌디드 러닝','학습자-내용 상호작용'],
 'v4coopc0d1':['모집단(원래 모둠)','STAD 학습팀','개별 책무성'],
 'v4orgc0d1':['관료제(Weber)','조직화된 무질서','비공식조직'],
 'v4orgmk7d0':['관료제(Weber)','조직화된 무질서','비공식조직'],
 'v4supc0d0':['임상장학','컨설팅 장학','자기장학'],
 'v4supc0d1':['전문적 학습공동체','컨설팅 장학','약식장학'],
 'v4supmk0d0':['임상장학','동료장학','자기장학'],
 'v4adm_etcc0d0':['만족 모형','점증 모형','합리 모형'],
 'v4planc0d0':['교육정책','교육재정','교육평가'],
 'v4lead_bc0d0':['공식조직','관료제(Weber)','이완결합체제'],
 'v4src0d2':['자기효능감','관찰학습','언어적 설득'],
 'v4vygc0d1':['근접발달영역','사적 언어','인지적 갈등(평형화)'],
 'v4ipc0d2':['조직화','정교화','시연'],
 'v4gardc0d0':['삼원지능이론(Sternberg)','일반지능(g) 이론','유동·결정지능 이론(Cattell)'],
 'v4careerc0d1':['탐구형','진취형','예술형'],
 'v4equalc0d0':['보장적 평등','과정적(조건적) 평등','허용적 평등'],
 'v4equalc0d1':['사회통제이론','차별접촉이론','아노미이론'],
 'v4philc0d0':['진보주의 교육','재건주의 교육','직업교육(도구적 교육)'],
 'v4k_autoc0d1':['학교자율시간','학업성취율','공통과목'],
 'v4eval_viewc0d0':['리커트 척도','표준화 검사','수행평가'],
 'v4eval_viewc0d1':['CAT','의미변별척도','사회성 측정법'],
 'v4motv_admc0d0':['공정성 이론','기대 이론','욕구위계 이론'],
 'v4motv_admc0d1':['동기-위생 이론','기대 이론','욕구위계 이론'],
 'v4mediac0d0':['Kozma','Dale','Hoban'],
 'v4mediac0d1':['Clark','Dale','Hoban'],
 'v4mediac1d1':['PSI(개별화 교수체제)','완전학습 기준(숙달 기준)','동기유발용 강의'],
 'v4inst_bmk10d0':['학습자 분석','과제 분석','환경 분석'],
 'v4lomk3d0':['Weick','Mintzberg','Sergiovanni'],
}
for i,xs in DX.items():
  x=I[i];assert x['k']=='disc' and x['a'] not in xs,(i)
  old=x['x'];x['x']=xs
  x['h']=[h for h in x['h'] if not (h.startswith("보기 '") and h.split("'")[1] not in xs)]
  LOG['disc_x'].append((i,old,xs))
I['v4lomk3d0']['q']="제시문 ㉠의 개념(조직 전체가 지속적으로 학습하며 스스로 변화하는 조직)을 체계화하고 그 구축 원리 5가지를 제시한 학자는?"
LOG['disc_q'].append('v4lomk3d0')
LOMH=["지문에서 이 부분에 주목 — ㉠ 학습조직(㉡ 전문적 학습공동체는 그 한 유형). 이 개념을 체계화한 학자를 묻는다.","5가지 원리(개인적 숙련·정신모형·공유비전·팀학습·시스템 사고)를 제시한 학자"]
# disc 첫 힌트: ㉠ 표시 부분만(문장 통째·'이하 생략' 제거)
for x in IT:
  if x['k']!='disc':continue
  lab=x['lab'];ctx=x['ctx']
  m=re.search(re.escape(lab)+r'(.+?)(?=[㉠-㉭]|$)',ctx,re.S)
  seg=None
  if m:
    seg=lab+m.group(1)
    seg=re.split(r'(?<=[\.\?!])\s|"\s',seg)[0].strip().rstrip('"')
  nh=[]
  for h in x['h']:
    if h.startswith('지문에서 이 문장에 주목'):
      if seg:h='지문에서 이 부분에 주목 — '+seg
      else:continue
    if '(이하 생략)' in h:continue
    nh.append(h)
  if x['id']=='v4lomk3d0':nh=LOMH
  if nh!=x['h']:LOG['disc_h'].append(x['id']);x['h']=nh
# ---------- 3. 객관식 ----------
I['v4clem0']['a']='정보 자원 제공';I['v4clem0']['e']="Jonassen CLE에서 교사의 교수활동은 모델링·코칭·비계설정 3가지이다. 정보 자원은 교수활동이 아니라 학습 지원 요소(관련 사례·정보 자원·인지 도구·대화·협력 도구·사회적·맥락적 지원) 중 하나이다. (기출에서는 형태주의 용어인 '통찰'이 오답지로 나왔다.)"
I['v4srm0']['a']='메타인지적 점검(계획·점검·평가)';I['v4srm0']['e']="시간 관리·환경 구조화·도움 구하기는 행동적 요소이다. 계획·점검·평가 같은 메타인지 활동은 인지(메타인지) 요소에 속한다. (기존 문항의 정답이던 '통찰'은 형태주의 용어로, 기출 오답지로 쓰였다.)"
LOG['mcq']+=['v4clem0','v4srm0']
# ---------- 4. 구조화: 부호화 전략에 메타인지가 섞인 오류 ----------
st=I['st59']
assert st['p'][2]['k']=='메타인지'
st['p'][2]={"k":"심상","s":"개념을 지도·그림·도식 같은 시각적 이미지로 함께 제시해 언어와 이미지로 이중 부호화하게 한다."}
st.setdefault('note',[]) if isinstance(st.get('note'),list) else None
st['note']="메타인지(학습 전략을 선택하고 점검·조절하게 한다)는 부호화 전략이 아니라 정보 흐름 전체를 조절하는 상위 인지이므로 항목에서 빼고 여기에 남긴다(v25)."
st['h'][2]="3번 항목의 설명 — 개념을 지도·그림·도식 같은 시각적 ○○로 함께 제시해 언어와 ○○로 이중 부호화하게 한다."
LOG['struct'].append('st59')
# ---------- 5. 새 카드 (id 새 번호, 재번호 없음) ----------
mx=max(x['r'] for x in IT if isinstance(x.get('r'),int))
def newcard(i,c,t,q,a,h,ckw,base,e=''):
  b=I[base];x={"id":i,"k":"card","c":c,"d":b['d'],"g":b['g'],"q":q,"a":a,"e":e,"hl":None,"t":t,"ckw":ckw,"cmp":None,"basis":b['basis'],"r":0,"h":h,"wd":b['wd']}
  if b.get('hj'):x['hj']=1
  assert i not in I;IT.append(x);I[i]=x;LOG['new'].append(i)
newcard('v4vrk1270','vr','전체 구조',"고전검사이론에서 문항의 질을 분석하는 세 가지 지표는 무엇이며, 각각 무엇을 보는가?",
 "**문항난이도** — 전체 응답자 중 정답자의 비율(P = 정답자 수 ÷ 전체 응답자 수). 값이 클수록 쉬운 문항\n**문항변별도** — 능력이 높은 학생과 낮은 학생을 구별하는 정도(상위 집단 정답률 − 하위 집단 정답률). 값이 클수록 변별력이 높음\n**오답지 매력도** — 각 오답지가 정답을 모르는 학생을 끌어들이는 정도. 기준: (1 − P) ÷ (답지 수 − 1) 이상이면 매력적인 오답지\n**함께 정리** — 고전검사이론의 문항 지수는 응답 집단이 바뀌면 달라진다(집단 의존적). 문항반응이론은 집단과 관계없이 문항 특성이 일정하다고 본다(문항 불변성, CAT의 기반).",
 ["개념 틀 — 얼마나 쉬운가 / 잘하는 학생과 못하는 학생을 가르는가 / 틀린 보기가 제 역할을 하는가","자체 6회 모의고사에서 변별도·오답지 매력도를 물었다"],
 ["문항난이도","문항변별도","오답지 매력도"],'v4vrk0',e="교재 표준(고전검사이론 문항분석) · 사용자 질문(학습조직, 고전 문항검사 세 가지) 반영")
newcard('v4vrk1271','vr','핵심 인출',"응답자 100명 중 정답자가 80명인 문항의 문항난이도 지수와 그 해석은? 이 지수가 가리키는 문항 분석 지표의 명칭은?",
 "**문항난이도**(문항 곤란도) — P = 80 ÷ 100 = **0.80**. 값이 클수록 쉬운 문항이므로 **쉬운 문항**으로 해석한다. 일반적으로 0.3~0.7 정도를 적절한 난이도로 보며, 0.5 근처에서 변별도가 가장 커질 수 있다(교재 표준).",
 ["정답자 비율이 높다는 것은 쉽다는 뜻이다. '곤란도'라는 이름과 값의 방향이 반대인 점에 주의"],["문항난이도"],'v4vrk0')
newcard('v4vrk1272','vr','핵심 인출',"상위 집단 20명 중 18명, 하위 집단 20명 중 6명이 맞힌 문항이 있다. 이 문항이 능력이 높은 학생과 낮은 학생을 구별하는 정도를 나타내는 지표의 명칭과 값, 그리고 하위 집단이 더 많이 맞힌 문항은 어떻게 처리하는가?",
 "**문항변별도** — DI = (18 − 6) ÷ 20 = **0.60** → 변별력이 높은 문항. 변별도 지수는 −1.0~+1.0이며, 0.40 이상이면 매우 양호, 0.30대는 양호, 0.20대는 수정이 필요하고 0.20 미만은 변별력이 낮다(Ebel 기준, 교재 표준). 하위 집단이 더 많이 맞힌 **부적 변별도** 문항은 정답·문항 진술에 문제가 있으므로 수정하거나 제거한다.",
 ["(상위 집단 정답자 수 − 하위 집단 정답자 수) ÷ 한 집단의 인원"],["문항변별도","부적 변별도"],'v4vrk0')
newcard('v4vrk1273','vr','핵심 인출',"사지선다 문항의 정답률이 0.40일 때, 어떤 오답지가 '매력적인 오답지'로 인정되려면 그 오답지를 고른 비율이 얼마 이상이어야 하는가? 이 지표의 명칭은?",
 "**오답지 매력도** — 기준 = (1 − P) ÷ (답지 수 − 1) = (1 − 0.40) ÷ (4 − 1) = **0.20**. 오답지를 고른 비율이 0.20 이상이면 매력적인 오답지, 미만이면 정답을 모르는 학생도 끌어들이지 못하는 오답지이므로 수정한다. 또 상위 집단이 하위 집단보다 더 많이 고른 오답지는 정답 시비가 있을 수 있어 점검한다.",
 ["틀린 학생의 비율(1 − P)을 오답지 수로 똑같이 나눈 값이 기준이 된다"],["오답지 매력도"],'v4vrk0')
newcard('v4lok1274','lo','비교(빈출)',"학교를 학습조직으로 만들자고 할 때, Senge의 학습조직과 전문적 학습공동체는 어떤 관계이며 각각 무엇을 강조하는가?",
 "**학습조직**(Senge) — 조직 전체가 지속적으로 학습하여 스스로 변화하는 조직. 구축 원리: 개인적 숙련, 정신모형, 공유비전, 팀학습, 시스템 사고\n**전문적 학습공동체** — 학습조직의 한 유형. 교사들이 공유 비전 아래 협력적으로 탐구하고, 수업을 공개·성찰하며, 학생 학습에 공동 책임을 지는 교사 공동체\n**함께 정리** — 기출 지문 표현: '학습조직의 한 유형인 전문적 학습공동체'. 앞의 것을 물으면 Senge의 원리로, 뒤의 것을 물으면 공유 비전·협력적 탐구·공동 책임으로 쓴다.",
 ["하나는 상위 개념(조직 전체), 하나는 그 안의 교사 모임 형태"],["학습조직","전문적 학습공동체"],'v4lok0',e="사용자 질문(학습조직) 반영 · 교재 표준")
newcard('v4leadk1275','lead','사례 판별',"제시문 속 일상어를 Bass 변혁적 지도성의 공식 명칭으로 바꾸면? ① '교장 선생님이 먼저 솔선수범해서 다들 존경하고 따른다' ② '우리 학교가 나아갈 미래를 생생하게 그려 보이며 의욕을 북돋운다' ③ '늘 해 오던 방식이 맞는지 의문을 던지고 다른 관점에서 생각해 보게 한다' ④ '선생님 한 분 한 분의 고민과 성장 요구를 따로 살피고 맞춤형으로 지원한다'",
 "① **이상적 영향력**(이상화된 영향력, 카리스마) ② **영감적 동기부여**(영감적 동기화) ③ **지적 자극** ④ **개별적 배려**\n**함께 정리** — '개별적 지원', '맞춤형 지원', '새로운 관점 제시', '솔선수범', '비전 제시'처럼 제시문 표현을 그대로 옮기면 명칭으로 인정되지 않는다(명칭 오기는 0점). 답안에는 공식 명칭을 쓰고, 제시문 표현은 근거로만 덧붙인다.",
 ["모의고사 오답: '개별적 배려'를 '개별적 지원'으로, '지적 자극'을 '새로운 관점'으로 씀","4I: 이상적 ○○○ · 영감적 ○○○○ · 지적 ○○ · 개별적 ○○"],
 ["이상적 영향력","영감적 동기부여","지적 자극","개별적 배려"],'v4leadk1',e="사용자 채점 약점(제시문 일상어를 명칭으로 씀) 보강")
newcard('v4srk1276','sr','사례 판별',"제시문 속 일상어를 Bandura 자기효능감 원천의 공식 명칭으로 바꾸면? ① '쉬운 과제부터 직접 해내 보게 했다' ② '비슷한 수준의 친구가 해내는 영상을 보여 주었다' ③ '\"너도 충분히 할 수 있어\"라고 격려했다' ④ '시험 전에 긴장을 풀도록 호흡 연습을 시켰다' 또, 원천 2가지를 쓰라는 문항에서 주의할 점은?",
 "① **성취 경험**(숙달 경험, mastery experience · 가장 강력) ② **대리 경험**(모델 관찰) ③ **언어적 설득**(사회적 설득) ④ **정서적·생리적 상태**\n**함께 정리** — 2가지를 쓰라고 하면 서로 다른 원천 2가지를 쓴다. '쉬운 과제부터 성공시키기'와 '단계별로 성공 경험 쌓기'는 둘 다 성취 경험이어서 1가지로만 인정된다.",
 ["직접 해 봄 / 남을 봄 / 말을 들음 / 몸과 마음의 상태"],["성취 경험","대리 경험","언어적 설득","정서적·생리적 상태"],'v4srk1',e="사용자 채점 약점(같은 범주 2개 중복) 보강")
for k,i in enumerate(LOG['new']):I[i]['r']=mx+1+k
# ---------- 6. 힌트 정리 (카드·단답만; 서술형은 손대지 않음) ----------
STOP=set('있다 한다 하는 것 위해 통해 이다 에서 으로 하고 하며 수업 학생 교사 학교 교육 학습 평가 개념 특징 원리 방법 단계 관점 내용 목표 vs'.split())
def tok(s):return set(w for w in re.findall(r'[가-힣A-Za-z]{2,}',re.sub(r'\*\*','',s or '')) if w not in STOP)
hstat=collections.Counter()
for x in IT:
  if x['k'] not in('card','short') or x['id'] in R or x['id'] in LOG['new']:continue
  H=x.get('h') or []
  if not isinstance(H,list):continue
  base=tok(x['q'])|tok(x.get('a'))|tok(x.get('e'))
  keep=[]
  for h in H:
    if h.startswith('비슷한 질문과 구별'):hstat['비슷한 질문 제거']+=1;continue
    if '(이하 생략)' in h:hstat['잘린 힌트 제거']+=1;continue
    if h.startswith('개념 틀 —'):
      body=h.split('—',1)[1]
      if not (tok(body)&base):hstat['무관한 개념 틀 제거']+=1;continue
    keep.append(h)
  if not keep and H:
    sk=[h for h in H if h.startswith('답의 뼈대') and '(이하 생략)' not in h]
    if sk:keep=sk[:1]
    else:
      a=re.sub(r'\*\*(.+?)\*\*','○○',x['a']).replace('\n',' / ')
      if '○○' in a and len(a)<=300:keep=['답의 뼈대(핵심어 가림) — '+a];hstat['뼈대 새로 생성']+=1
  if not keep and H:
    def m(w):return w[0]+'○'*(len(w)-1) if len(w)>=2 else w
    a=re.sub(r'\*\*','',x['a'])
    keep=['첫 글자 단서 — '+re.sub(r'[가-힣A-Za-z]{2,}',lambda g:m(g.group(0)),a)[:200]];hstat['첫 글자 단서 생성']+=1
  if keep!=H:x['h']=keep;LOG['hint_items'].append(x['id'])
LOG['hint_stat']=dict(hstat)
I['v4hidk1215']['a']=I['v4hidk1215']['a'].replace("'Jackson은 그 원천으로 …'처럼","'Jackson은 잠재적 교육과정의 원천으로 군집성·평가(상찬)·권력을 들었다'처럼");LOG['fix'].append('v4hidk1215')
I['v4sbcdk5']['q']="Skilbeck 모형에서 교육과정 운영 결과를 점검하고 그 결과를 다음 개발에 되돌려 반영하는 마지막 단계의 명칭은?"
# ---------- 7. 검증 ----------
ids=[x['id'] for x in IT];assert len(ids)==len(set(ids))
for x in IT:
  if x['id'] in orig:
    assert x['k']==orig[x['id']]['k']
    if x['k'] in('essay','prob','case','l22','wt','pat'):
      assert x==orig[x['id']],('서술형 변경 금지',x['id'])
    assert x.get('dup')==orig[x['id']].get('dup') and x.get('wd')==orig[x['id']].get('wd')
  assert x.get('wd') in('월','화','수','목','금'),x['id']
  if x['k']=='card':assert '…' not in x['a'] and '(이하 생략)' not in x['a'],x['id']
  for h in (x.get('h') or []) if isinstance(x.get('h'),list) else []:
    if x['k'] in('card','short','disc','mcq','struct') and (x['id'] in R or x['id'] in LOG['new'] or x['id'] in LOG['hint_items']):
      assert '(이하 생략)' not in h,(x['id'],h)
# 새 앞면이 답을 그대로 드러내지 않는지(카드 conv): 굵은 정답 명칭이 앞면에 없는지
for i,v in R.items():
  if v['_kind']=='conv':
    nm=re.sub(r'\(.*?\)','',re.findall(r'\*\*(.+?)\*\*',I[i]['a'])[0]).strip()
    if nm in I[i]['q']:LOG['leak_warn'].append((i,nm))
json.dump(d,open(SRC,'w'),ensure_ascii=False,indent=1)
json.dump(LOG,open('/workspace/edu/v25/log.json','w'),ensure_ascii=False,indent=1)
print({k:(len(v) if isinstance(v,list) else v) for k,v in LOG.items()})
print('leak',LOG['leak_warn']);print('items',len(IT),'visible',sum(1 for x in IT if not x.get('dup')))
