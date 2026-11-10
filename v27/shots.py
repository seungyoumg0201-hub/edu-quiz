import sys
from playwright.sync_api import sync_playwright
U=sys.argv[1] if len(sys.argv)>1 else "http://localhost:8765/"
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);pg=b.new_page(viewport={'width':430,'height':1100})
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto(U);pg.wait_for_timeout(2500)
  print('sw', pg.evaluate("fetch('sw.js',{cache:'no-store'}).then(r=>r.text()).then(t=>t.slice(0,30))"))
  print('n', pg.evaluate("DATA.items.length"))
  for iid,n in [('v4clek1277',2),('ybcle0',3),('v4plck1280',1),('v4orgk1281',1),('ybsup0',1),('v4expk1283',1),('v4coopk4',3)]:
    pg.evaluate(f"()=>{{Q=[DATA.items.find(x=>x.id==='{iid}')];qi=0;M='all';show()}}")
    pg.wait_for_timeout(300)
    for _ in range(n):
      try: pg.click('#hb',timeout=1500);pg.wait_for_timeout(150)
      except Exception as e: print('nohb',iid)
    print(iid,'|',pg.inner_text('#app')[:300].replace('\n',' / '))
  print('errors',errs)
  b.close()
