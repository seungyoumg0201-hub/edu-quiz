import html,re,sys
E=html.escape
TAG={'외':('tw','띵크맵 외'),'강':('tk','강의 반영'),'표':('ts','교재 표준')}
def tags(s):
    t=re.findall(r'#(외|강|표)',s);s=re.sub(r'\s*#(외|강|표)','',s).strip();return s,''.join(f'<span class="tg {TAG[x][0]}">{TAG[x][1]}</span>' for x in t)
days=[];cur=None
for l in open('data.txt'):
    l=l.rstrip('\n')
    if not l.strip():continue
    if l.startswith('@'):
        k,t=l[1:].split('|');cur={'k':k,'t':t,'sk':[],'tr':[]};days.append(cur);sec=None;continue
    if l.startswith('%'):sec=l[1:];continue
    if sec=='뼈대':cur['sk'].append(l)
    else:cur['tr'].append(l)
def node(s):
    s,tg=tags(s);st=''
    if s.startswith('★'):st='s';s=s[1:]
    elif s.startswith('◇'):st='d';s=s[1:]
    if '|' in s:a,b=[x.strip() for x in s.split('|',1)]
    else:a,b=s.strip(),''
    mark='<i class="st">★</i>' if st=='s' else '<i class="df">방어</i>' if st=='d' else ''
    return f'{mark}<b>{E(a)}</b>{tg}'+(f'<span class="ds">{E(b)}</span>' if b else '')
def day_html(d):
    sk=''.join(f'<li>{node(x)}</li>' for x in d['sk'])
    out=[];prev=-1
    for l in d['tr']:
        lv=len(l)-len(l.lstrip(' '))
        if lv==0:out.append(f'<h3>{node(l)}</h3>');continue
        out.append(f'<div class="n l{lv}">{node(l.strip())}</div>')
    return f'''<section class="day" id="d{d['k']}"><header><span class="dk">{d['k']}</span><h2>{E(d['t'])}</h2></header>
<div class="sk"><div class="skh">백지 재생용 뼈대 <small>먼저 이것만 보고 백지에 위계를 써 본 뒤 아래와 맞춰 보세요</small></div><ul>{sk}</ul></div>
<div class="tree">{''.join(out)}</div></section>'''
CSS=open('style.css').read()
LEG='<div class="leg"><i class="st">★</i> 최우선(S) · <i class="df">방어</i> 방어용 · <span class="tg tw">띵크맵 외</span> 띵크맵에 없는 개념 · <span class="tg tk">강의 반영</span> v21·v22 홍지완 강의로 추가 · <span class="tg ts">교재 표준</span> 출처 미확인</div>'
def page(body,title,nav=''):
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{CSS}</style></head><body>{nav}{body}</body></html>'
nav='<nav>'+''.join(f'<a href="#d{d["k"]}">{d["k"]}</a>' for d in days)+'<span>토 모의고사 · 일 오답 정리</span></nav>'
open('교육학_위계도_요일별.html','w').write(page('<h1>교육학 위계도 · 요일별</h1>'+LEG+''.join(day_html(d) for d in days),'교육학 위계도 요일별',nav))
for d in days:
    open(f'day_{d["k"]}.html','w').write(page(LEG+day_html(d),f'{d["k"]}요일 위계도'))
print([ (d['k'],len(d['tr'])) for d in days])
