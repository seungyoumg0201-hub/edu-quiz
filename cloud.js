// ---- 계정 동기화(전공퀴즈 geo-vocab과 같은 Firebase 프로젝트·같은 Google 로그인). 공개 클라이언트 설정만 포함. 앱은 로그인 없이도 전부 동작 ----
var FBV='10.12.2',FB_CFG={apiKey:'AIzaSyD_1gGwE9fuurmdR3OFKiTy5RfWRGpPIEU',authDomain:'geo-vocab.firebaseapp.com',projectId:'geo-vocab',storageBucket:'geo-vocab.firebasestorage.app',messagingSenderId:'871138215339',appId:'1:871138215339:web:4221ec7bff77e8cae73eee',databaseURL:'https://geo-vocab-default-rtdb.asia-southeast1.firebasedatabase.app'};
var CL={st:'off',user:null,msg:'',dirty:false,last:+(localStorage.getItem('edu_cloud_last')||0)},fb=null,fbP=null,EDU_NODE='eduquiz';
function cloudLoad(){if(fbP)return fbP;const u=m=>`https://www.gstatic.com/firebasejs/${FBV}/firebase-${m}.js`;CL.st='loading';
 fbP=Promise.all(['app','auth','database'].map(m=>import(u(m)))).then(([A,Au,D])=>{const app=A.initializeApp(FB_CFG,'edu');let auth;try{auth=Au.initializeAuth(app,{persistence:[Au.indexedDBLocalPersistence,Au.browserLocalPersistence],popupRedirectResolver:Au.browserPopupRedirectResolver})}catch(e){auth=Au.getAuth(app)}
  fb={A,Au,D,app,auth,rt:D.getDatabase(app)};CL.st='ready';Au.onAuthStateChanged(auth,u=>{const was=CL.user&&CL.user.uid;CL.user=u||null;localStorage.setItem('edu_fb',u?'1':'0');if(u&&was!==u.uid)onLogin(u);cloudUI()});return fb})
 .catch(e=>{CL.st='fail';CL.msg=navigator.onLine?'클라우드 기능을 불러오지 못했어요':'오프라인 — 동기화는 온라인에서 돼요';fbP=null;cloudUI();throw e});return fbP}
function eduRef(){return fb.D.ref(fb.rt,'review/'+CL.user.uid+'/devices/'+EDU_NODE)}
// 병합: 로컬 기록을 절대 버리지 않음. 오답은 합집합(마지막 오답 시각 > 해제 시각이면 유지), 횟수·통계는 큰 값
function mergeSt(c){if(!c||typeof c!=='object')return;const mx=(a,b)=>Math.max(a||0,b||0);st.wrAt=st.wrAt||{};st.wrDel=st.wrDel||{};
 const ca=c.wrAt||{},cd=c.wrDel||{};for(const k in ca)st.wrAt[k]=mx(st.wrAt[k],ca[k]);for(const k in cd)st.wrDel[k]=mx(st.wrDel[k],cd[k]);
 const ids=new Set(DATA.items.map(x=>x.id)),all=new Set([...Object.keys(st.wr),...Object.keys(c.wr||{})]);
 for(const k of all){if(!ids.has(k))continue;const n=mx(st.wr[k],(c.wr||{})[k]);if((st.wrAt[k]||1)>(st.wrDel[k]||0))st.wr[k]=n;else delete st.wr[k]}
 for(const k in (c.sr||{})){const a=st.sr[k],b=c.sr[k];if(!a||(b&&b.d>a.d))st.sr[k]=b}
 for(const k in (c.hist||{})){const a=st.hist[k]||{c:0,w:0},b=c.hist[k]||{};const h={c:mx(a.c,b.c),w:mx(a.w,b.w)};if(a.hc||b.hc)h.hc=mx(a.hc,b.hc);if(a.p||b.p)h.p=mx(a.p,b.p);st.hist[k]=h}
 for(const k in (c.days||{}))st.days[k]=mx(st.days[k],c.days[k]);
 for(const k in c)if(!(k in st))st[k]=c[k]}
async function onLogin(u){CL.msg='동기화 중…';cloudUI();try{const s=await fb.D.get(eduRef());const v=s.val();if(v&&v.p){try{mergeSt(JSON.parse(v.p))}catch(e){}}
  localStorage.setItem(LS,JSON.stringify(st));await cloudPush(true);await missBackfill();CL.msg='✅ 동기화됨';try{badge();if(VIEW==='home')home()}catch(e){}}
 catch(e){CL.msg='⚠️ 동기화 실패: '+(e.code||e.message);toast('동기화 실패 ['+(e.code||e.message)+']')}cloudUI()}
async function cloudPush(force){if(!fb||!CL.user)return;if(!force&&!CL.dirty)return;CL.dirty=false;
 await fb.D.set(eduRef(),{name:'교육학 퀴즈 앱(edu-quiz)',app:'edu',v:1,p:JSON.stringify(st),wrN:Object.keys(st.wr).length,seen:fb.D.serverTimestamp()});CL.last=Date.now();localStorage.setItem('edu_cloud_last',CL.last);cloudUI()}
var _cpT=null;window.cloudDirty=()=>{if(!CL.user)return;CL.dirty=true;cloudUI();clearTimeout(_cpT);_cpT=setTimeout(()=>cloudPush().catch(e=>{CL.msg='⚠️ 동기화 실패: '+(e.code||'');cloudUI()}),4000)};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&CL.dirty)cloudPush().catch(()=>{})});
// 오답 1건 = 실시간 로그(review/<uid>/misses, d:'edu'). 비로그인 시 대기열에 보관 후 로그인 때 업로드
function missObj(id){const x=DATA.items.find(i=>i.id===id)||{};return {at:Date.now(),d:'edu',id:id,k:String(x.k||''),area:String(x.d||'').slice(0,60),q:String(x.q||'').replace(/<[^>]+>/g,'').slice(0,200),n:st.wr[id]||1}}
window.eduMiss=(id,lv)=>{st.wrAt=st.wrAt||{};st.wrAt[id]=Date.now();const o=missObj(id);if(lv)o.lv=lv;if(fb&&CL.user){fb.D.push(fb.D.ref(fb.rt,'review/'+CL.user.uid+'/misses'),o).catch(()=>{queueMiss(o)})}else queueMiss(o)};
function queueMiss(o){const q=JSON.parse(localStorage.getItem('edu_missq')||'[]');q.push(o);while(q.length>2000)q.shift();localStorage.setItem('edu_missq',JSON.stringify(q))}
async function missBackfill(){const q=JSON.parse(localStorage.getItem('edu_missq')||'[]');const first=!localStorage.getItem('edu_missbf');
 if(first){const now=Date.now();for(const id in st.wr)if(!q.some(o=>o.id===id)){const o=missObj(id);o.at=(st.wrAt&&st.wrAt[id])||now;o.how='backfill';q.push(o)}}
 if(!q.length){localStorage.setItem('edu_missbf','1');return}const u={};q.forEach((o,i)=>{u['e'+o.at+'_'+i+'_'+String(o.id).replace(/[.#$\/\[\]]/g,'_')]=o});
 await fb.D.update(fb.D.ref(fb.rt,'review/'+CL.user.uid+'/misses'),u);localStorage.setItem('edu_missq','[]');localStorage.setItem('edu_missbf','1');toast('오답 '+q.length+'건을 계정에 올렸어요')}
async function login(){try{await cloudLoad();const {Au}=fb,pv=new Au.GoogleAuthProvider();pv.setCustomParameters({prompt:'select_account'});
 try{const r=await Au.signInWithPopup(fb.auth,pv);if(r&&r.user)toast('✅ 로그인됨: '+(r.user.email||''))}catch(e){const c=e&&e.code||'';if(/popup-blocked|operation-not-supported|web-storage-unsupported/.test(c)){localStorage.setItem('edu_lpend','1');await Au.signInWithRedirect(fb.auth,pv)}else throw e}}
 catch(e){const c=(e&&e.code)||String(e);localStorage.removeItem('edu_lpend');toast('로그인 실패 ['+c+']');cloudUI()}}
async function logout(){if(!fb)return;try{await cloudPush(true)}catch(e){}await fb.Au.signOut(fb.auth);toast('로그아웃 — 이 기기의 기록은 그대로 남아요')}
function cloudState(){const u=CL.user;if(!u)return ['off',CL.st=='loading'&&localStorage.getItem('edu_fb')=='1'?'연결 중…':'로그인'];if(/실패/.test(CL.msg))return ['err','동기화 실패'];if(CL.dirty||/중/.test(CL.msg))return ['pend','동기화 대기'];return ['ok','동기화됨']}
function cloudUI(){let c=$('#authchip');if(!c){const t=$('#theme');if(!t)return;t.insertAdjacentHTML('beforebegin','<button id="authchip" class="achip" aria-label="계정 동기화"></button>');c=$('#authchip');c.onclick=()=>{if(!CL.user)login();else{CL.dirty=true;cloudPush(true).then(()=>{CL.msg='✅ 동기화됨';cloudUI();toast('✅ 동기화됨')}).catch(e=>{CL.msg='⚠️ 동기화 실패: '+(e.code||'');cloudUI()})}}}
 const [s,tx]=cloudState(),u=CL.user;c.className='achip '+s;c.title=u?'로그인됨 — 탭하면 지금 동기화':'탭해서 Google 로그인(전공퀴즈와 같은 계정)';c.innerHTML=(u?`<span class="av">${esc(((u.displayName||u.email||'나')+'').charAt(0))}</span>`:'')+`<span class="dot"></span><span class="tx">${tx}</span>`;
 const cc=$('#cloudCard');if(cc){cc.innerHTML=cloudCardHTML();bindCloudCard()}}
function cloudCardHTML(){if(!CL)return '<h2>☁️ 계정 동기화</h2>';const u=CL.user,hm=t=>t?new Date(t).toLocaleString('ko-KR',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit',hour12:false}):'—';
 if(!u)return `<h2>☁️ 계정 동기화</h2><p class="mut" style="font-size:14px">전공퀴즈(지리)와 같은 Google 계정으로 로그인하면 오답·복습 기록이 기기 간에 합쳐지고, 매일 자정 이후 오답 검토에 쓰여요. 이 기기의 기존 기록은 지워지지 않고 계정에 합쳐져요.</p>${CL.st=='fail'?`<p class="mut">${esc(CL.msg)}</p>`:''}<button class="btn l" id="cLogin">Google로 로그인</button>`;
 return `<h2>☁️ 계정 동기화</h2><p style="font-size:14px">${esc(u.email||'로그인됨')}<br><span class="mut">${esc(CL.msg||'')} · 마지막 동기화 ${hm(CL.last)} · 오답 ${Object.keys(st.wr).length}개</span></p><button class="btn l" id="cSync">지금 동기화</button><button class="btn l" id="cOut">로그아웃</button>`}
function bindCloudCard(){const a=$('#cLogin'),b=$('#cSync'),o=$('#cOut');if(a)a.onclick=login;if(b)b.onclick=()=>{CL.dirty=true;cloudPush(true).then(()=>{CL.msg='✅ 동기화됨';cloudUI();toast('✅ 동기화됨')}).catch(e=>toast('동기화 실패 ['+(e.code||'')+']'))};if(o)o.onclick=logout}
cloudUI();if(localStorage.getItem('edu_fb')=='1'||localStorage.getItem('edu_lpend')=='1'||localStorage.getItem('gv_fb')=='1'){cloudLoad().then(()=>{if(localStorage.getItem('edu_lpend')=='1'){localStorage.removeItem('edu_lpend');return fb.Au.getRedirectResult(fb.auth).catch(e=>toast('로그인 실패 ['+(e.code||'')+']'))}}).catch(()=>{})}
