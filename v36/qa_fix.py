#!/usr/bin/env python3
"""v36 2차(풀이자 관점 재풀이) 수정: v4integk1291 발문 모호함(㉠·㉡의 Drake 명칭이 정해지지 않음), v4mlk1292 발문 문장, 힌트 2개(답 일부 누설·글자 수 단서) 교체."""
import json
SRC='/workspace/edu/src/items.json';d=json.load(open(SRC));I={x['id']:x for x in d['items']}
x=I['v4integk1291'];o="를, 교육과정 '조직 형태'로 물을 때와 Drake의 '통합 유형'으로 물을 때 각각 어떤 명칭으로 써야 하는가?"
assert x['q'].endswith(o);x['q']=x['q'][:-len(o)]+"에 대하여, (1) ㉠~㉢을 교육과정 조직 형태의 명칭으로 쓰고, (2) ㉢을 Drake의 통합 유형으로 물으면 어떤 명칭으로 써야 하는지 쓰시오."
x['a']=x['a'].replace("**조직 형태로 물을 때**","**(1) 조직 형태로 물을 때**").replace("**Drake의 통합 유형으로 물을 때**","**(2) Drake의 통합 유형으로 물을 때** — ㉢은 **탈학문적 통합**. 세 유형 전체:")
assert '(2) Drake' in x['a']
x=I['v4mlk1292'];o=" Eccles와 Wigfield의 이론, Keller의 모형이 제시문에 주어졌을 때 ㉠~㉢은 각각 어떤 개념이며, ㉠과 ㉢은 어떻게 구별되는가?"
assert x['q'].endswith(o);x['q']=x['q'][:-len(o)]+" 제시문에는 Eccles와 Wigfield의 기대×가치 이론과 Keller의 ARCS 모형이 함께 나온다. ㉠~㉢은 각각 어느 이론의 어떤 요소이며, ㉠과 ㉢은 어떻게 구별되는가?"
I['v4leadk1294']['h']=["각 행동이 교사들의 무엇을 움직이는지 본다 — 존경과 신뢰, 의욕과 기대, 생각의 틀, 한 사람의 성장"]
I['v4bwdk1295']['h']=["각 문장의 끝말(밝힌다·풀어낸다·써 본다·따져 본다·헤아린다·돌아본다)이 어떤 이해를 보여 주는지 본다"]
json.dump(d,open(SRC,'w'),ensure_ascii=False,indent=1);print('ok')
