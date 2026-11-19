import json,re,sys
P=sys.argv[1] if len(sys.argv)>1 else '/workspace/edu/src/items.json'
D=json.load(open(P))
GEO=r"지리|지교론|답사|지형|기후|GIS|등고선|위도|경도|축척|하천|산맥|화산|해안|지구본|국토|대륙|강수|기온|계절풍|촌락|빙하|판 구조|지표면|지역 ?조사|야외 ?조사|공간적 (관점|사고|분포|상호작용)|공간 상호작용|장소감|피커링|Pickering|세계 ?지도|지도를 ?(보|읽|그|활용|만들|펼|이용|제작|해석)|지도에(서)? |지도와 (위성|통계|사진|그래프|도표)|지도 ?읽|지도·(위성|통계|그래프|사진|지구본)|지도 위|백지도|위성 ?사진|도시 구조|인구 이동|열대|사막|툰드라|지역 개발|입지|지명|해발|지형 고도|경관|지도 단원|폭염|홍수|범람|수위|해륙풍|기압|농업|최고기온|탄소중립|우리 고장|위험 지도|기후변화|문명의 발생|침식|퇴적|파랑의 침식|침수|집중호우|급경사|경사가|지역 지도|태블릿 지도|인간과 자연|개발과 보전|실제 거리|두 지점(의| 사이)|우리 동네 어느 곳|지도 제작|지도를 조작|·지도 자료|그림·지도|관광 안내"
# 교육학 고유 용어/총론 원문/동음이의 허용 목록 (근거: QA 로그)
ALLOW=["아지리스","경제·지리 장애","경제적·지리적","지리적 장애","지리적·","보장적 평등은 ○○적·○○적","Hoban","기후·생태환경 변화","진로지도에","독해력 지도에","지도에 쓰","사고도","이라고도","경제·지리·사회적","생활지도·","재지도·","지도·조언","사진 → 지도·도표","지도·그림·도식","농업 체험","남대천 범람","남대천의 잦은 범람"]
R=re.compile(GEO)
def walk(o,p=''):
    if isinstance(o,str): yield p,o
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f'{p}[{i}]')
    elif isinstance(o,dict):
        for k,v in o.items():
            yield f'{p}.<key>',k
            yield from walk(v,f'{p}.{k}')
def clean(s):
    for a in ALLOW: s=s.replace(a,'□'*len(a))
    return s
bad=[]
src=[('item:'+x['id'],x) for x in D['items']]+[('__'+k,D[k]) for k in ['con','conf','kwcl','sets'] if k in D]
for cid,o in src:
    for p,s in walk(o):
        if p.endswith('.<key>') and False: pass
        if s=='지리' and '.kw' in p: continue
        c=clean(s)
        for m in R.finditer(c): bad.append((cid,p,m.group(0),s[max(0,m.start()-30):m.end()+30].replace('\n',' ')))
for b in bad: print(*b,sep=' | ')
print('GEO_HITS',len(bad),'items',len({b[0] for b in bad}))
sys.exit(1 if bad else 0)
