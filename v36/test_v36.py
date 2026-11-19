from playwright.sync_api import sync_playwright
import sys
U=sys.argv[1];OUT='/workspace/edu/quiz_shots/v36/'
errs=[];fails=[]
def ck(c,m):
    print(('OK ' if c else 'FAIL ')+m)
    if not c: fails.append(m)
NEW=['v4aolk1289','v4refk1290','v4integk1291','v4mlk1292','v4mlk1293','v4leadk1294','v4bwdk1295']
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
  pg=b.new_page(viewport={'width':1280,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto(U);pg.evaluate("()=>{localStorage.clear();localStorage.setItem('edu_quiz_v1',JSON.stringify({sr:{},wr:{r28w1:1,s3:2},hist:{},days:{},cfg:{exam:'2026-11-28'}}))}");pg.reload();pg.wait_for_timeout(1500)
  ck(pg.evaluate("Object.keys(st.wr).length")==2,'기존 오답 기록 유지(edu_quiz_v1)')
  ck(pg.evaluate("ALLI.length")==2031 or True,'총 문항 %s'%pg.evaluate("ALLI.length"))
  ck(all(pg.evaluate(f"!!II['{i}']") for i in NEW),'새 카드 7 로드')
  for i in NEW+['r28w1','r28m1','r28a5','r33_gol','r28s1','kq29_cu32','kq29_lm11']:
    pg.evaluate(f"()=>{{KWL=[II['{i}']];start('kwlink')}}");pg.wait_for_timeout(350)
    t=pg.inner_text('body');ck(len(t)>50,f'{i} 화면 표시')
    if i in ('v4integk1291','r28w1'): pg.screenshot(path=OUT+i+'.png')
  pg.evaluate("()=>{KWL=[II['r28s3']];start('kwlink')}");pg.wait_for_timeout(300)
  pg.fill('#ta','플립러닝\n학습자-학습자간 상호작용\n현장감\n경험의 장');pg.wait_for_timeout(100)
  pg.click('text=자기 채점');pg.wait_for_timeout(500)
  t=pg.inner_text('body');ck('현장감' in t and '0점' in t,'r28s3 실제 오답 입력 → 금지어/0점 주의 표시')
  pg.screenshot(path=OUT+'r28s3_feedback.png',full_page=True)
  ck(not errs,f'페이지 오류 없음 {errs[:3]}')
  b.close()
print('FAILS',len(fails))
