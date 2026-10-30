#!/usr/bin/env python3
"""items.json을 shell.html에 주입해 index.html 생성. id 재번호 금지·중복 금지 검사."""
import json,sys
import os;D=os.path.dirname(os.path.abspath(__file__))+'/';OUT=sys.argv[1] if len(sys.argv)>1 else '/workspace/quizsite/index.html'
obj=json.load(open(D+'items.json'))
ids=[x['id'] for x in obj['items']];assert len(ids)==len(set(ids)),'dup id'
s=open(D+'shell.html').read();assert s.count('/*__DATA__*/')==1
open(OUT,'w').write(s.replace('/*__DATA__*/',json.dumps(obj,ensure_ascii=False,separators=(',',':'))))
print('items',len(ids),'->',OUT)
