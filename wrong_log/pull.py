#!/usr/bin/env python3
"""교육학 퀴즈 앱 계정 동기화 데이터 → /workspace/edu/wrong_log/YYYY-MM-DD.json + latest.json
공개 읽기 경로(review/<uid>)만 사용 — 자격증명 불필요. 데이터가 없으면 아무 파일도 만들지 않음(가짜 데이터 금지)."""
import json,sys,os,urllib.request,datetime
DB='https://geo-vocab-default-rtdb.asia-southeast1.firebasedatabase.app'
UID=os.environ.get('EDU_UID') or (sys.argv[1] if len(sys.argv)>1 else 'snw9XbdP1Xbf0Z3o0ISkTusAhdB3')
D=os.path.dirname(os.path.abspath(__file__))
get=lambda p:json.load(urllib.request.urlopen(f'{DB}/review/{UID}/{p}.json',timeout=30))
dev=get('devices/eduquiz')
misses=get('misses') or {}
edu=sorted([dict(v,key=k) for k,v in misses.items() if isinstance(v,dict) and v.get('d')=='edu'],key=lambda x:x.get('at',0))
if not dev and not edu:
    print('아직 동기화된 교육학 데이터 없음 (앱에서 로그인 필요)');sys.exit(2)
st=json.loads(dev['p']) if dev and dev.get('p') else {}
KST=datetime.timezone(datetime.timedelta(hours=9));now=datetime.datetime.now(KST)
for m in edu:m['at_kst']=datetime.datetime.fromtimestamp(m['at']/1000,KST).isoformat(timespec='seconds')
out={'pulled_at_kst':now.isoformat(timespec='seconds'),'uid':UID,'seen':dev.get('seen') if dev else None,
     'wrong_now':st.get('wr',{}),'wrong_at':st.get('wrAt',{}),'cleared_at':st.get('wrDel',{}),'hist':st.get('hist',{}),'days':st.get('days',{}),
     'miss_events':edu}
for f in (now.strftime('%Y-%m-%d')+'.json','latest.json'):
    json.dump(out,open(os.path.join(D,f),'w'),ensure_ascii=False,indent=1)
print('ok wrong_now',len(out['wrong_now']),'miss_events',len(edu))
