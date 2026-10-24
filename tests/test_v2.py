"""Run python3 tests/test_v2.py after python3 build_v2.py. Never sends booking data."""
import contextlib,json,threading,http.server,functools,sys,re,shutil
from pathlib import Path
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'site')))
threading.Thread(target=server.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{server.server_port}'
paths=['/'+str(p.relative_to(ROOT/'site')).replace('index.html','') for p in sorted((ROOT/'site').rglob('*.html'))]
errors=[];screenshots=0;loads=0;posted=[]
def check(good,message):
 if not good:errors.append(message)
def tab_to(page,selector):
 for _ in range(180):
  if page.locator(selector).first.evaluate('(el)=>el===document.activeElement'):return
  page.keyboard.press('Tab')
 raise AssertionError('Tab could not reach '+selector)
def contrast_ratio(a,b):
 def lum(colour):
  values=[int(colour[i:i+2],16)/255 for i in (1,3,5)]
  values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
  return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))
 x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)

def computed_band_contrast(page):
 pairs=page.locator('.band-dark h2,.band-dark h3,.band-dark p,.band-dark a,.band-dark button,.band-soft h2,.band-soft p,.band-soft label,.band-soft a,.band-soft button').evaluate_all("""els=>els.filter(el=>el.offsetParent!==null&&el.textContent.trim()).map(el=>{const hex=rgb=>'#'+rgb.match(/[0-9.]+/g).slice(0,3).map(n=>Math.round(Number(n)).toString(16).padStart(2,'0')).join('');let parent=el,bg;while(parent){bg=getComputedStyle(parent).backgroundColor;if(bg!=='transparent'&&bg!=='rgba(0, 0, 0, 0)')break;parent=parent.parentElement}return {fg:hex(getComputedStyle(el).color),bg:hex(bg),text:el.textContent.trim().slice(0,50)}})""")
 for pair in pairs:check(contrast_ratio(pair['fg'],pair['bg'])>=4.5,'B: computed AA contrast '+str(pair))

def v3_checks(context,page,width):
 # B: exact prescribed pairings, including buttons and their hover state.
 for fg,bg in [('#F7F3EC','#2B201A'),('#E6DDCF','#2B201A'),('#F2C98A','#2B201A'),('#2B201A','#F7F3EC'),('#2B201A','#FFFFFF'),('#211E1A','#EFE7DA'),('#57514A','#EFE7DA'),('#FFFFFF','#1E4E79'),('#E6DDCF','#3A2C24')]:
  check(contrast_ratio(fg,bg)>=4.5,f'B: contrast failed {fg}/{bg}')
 page.goto(BASE+'/')
 check(page.locator('.home-doctor.band-dark').count()==1,'B: home dark band missing')
 check(page.locator('.band-soft').count()==3,'B/C1: soft surfaces missing')
 computed_band_contrast(page)
 # C1 and C8: keyboard selection followed by the prefilled booking link.
 tab_to(page,'input[name="picker-pet"][value="dog"]');page.keyboard.press('Space')
 tab_to(page,'input[name="picker-need"][value="wellness"]');page.keyboard.press('Space')
 check(page.locator('#picker-content').inner_text().startswith('A yearly exam and vaccines keep small problems small.'),'C1: result copy')
 tab_to(page,'#picker-content a[href^="/book/"]');page.keyboard.press('Enter');page.wait_for_url('**/book/**')
 check(page.locator('input[name=species][value=Dog]').is_checked(),'C8: species not prefilled')
 check(page.locator('input[name=reason][value="Wellness exam or vaccines"]').is_checked(),'C8: reason not prefilled')
 check(page.locator('#prefill-pet').inner_text()=="We've filled in what you picked.",'C8: missing announcement')
 # Remaining picker branches and Rabbit-specific supplemental link.
 for need,expected in [('sick','Is it urgent?'),('dental','Bad breath or a sore mouth'),('surgery',"We'll start with a consult"),('young','First vaccines'),('goodbye',"We're here to help")]:
  page.goto(BASE+'/');page.locator('input[name="picker-pet"][value="rabbit"]').focus();page.keyboard.press('Space');page.locator(f'input[name="picker-need"][value="{need}"]').focus();page.keyboard.press('Space')
  check(expected in page.locator('#picker-content').inner_text(),'C1: '+need+' result')
  check(page.locator('#picker-content a[href="/services/small-mammal-medicine/"]').count()==1,'C1: rabbit link')
  if need=='goodbye':check(page.locator('#picker-content a[href^="/book/"]').count()==0,'C1: goodbye must not book')
 # C3: native combobox keyboard hit, miss, Escape and full list retention.
 page.goto(BASE+'/pet-care/');tab_to(page,'#plant-checker');page.keyboard.type('lily');page.keyboard.press('ArrowDown');page.keyboard.press('Enter')
 check('is on our poisonous plant list.' in page.locator('#plant-result').inner_text(),'C3: hit missing')
 check(page.locator('#plant-result a[href="tel:+16045141711"]').count()==1,'C3: after-hours Call missing')
 page.locator('#plant-checker').press('ControlOrMeta+A');page.keyboard.type('zzzznotaplant')
 check("isn't on our list. That doesn't mean it's safe." in page.locator('#plant-result').inner_text(),'C3: miss must not promise safety')
 page.locator('#plant-checker').press('ControlOrMeta+A');page.keyboard.type('lily');page.keyboard.press('ArrowDown');page.keyboard.press('Escape')
 check(page.locator('#plant-checker').get_attribute('aria-expanded')=='false','C3: Escape did not close list')
 check(page.locator('[data-plant-group]').count()>0,'C3: full grouped list removed')
 # C4: keyboard navigation, native card size, focus containment and Esc return.
 page.goto(BASE+'/');tab_to(page,'[data-wall-photo]');page.keyboard.press('Enter')
 check(page.locator('#wall-lightbox').is_visible(),'C4: lightbox did not open')
 first=page.locator('#wall-image').get_attribute('src');check(page.locator('#wall-image').get_attribute('width')=='514','C4: thank-you card native width')
 page.keyboard.press('ArrowRight');check(page.locator('#wall-image').get_attribute('src')!=first,'C4: next arrow')
 page.keyboard.press('ArrowLeft');check(page.locator('#wall-image').get_attribute('src')==first,'C4: previous arrow')
 if width<900:
  page.locator('#wall-lightbox').evaluate("el=>{for(const [type,x] of [['touchstart',200],['touchend',100]])el.dispatchEvent(new TouchEvent(type,{bubbles:true,changedTouches:[new Touch({identifier:1,target:el,clientX:x})]}))}");check(page.locator('#wall-image').get_attribute('src')!=first,'C4: swipe navigation')
 page.keyboard.press('Shift+Tab');check(page.locator('#wall-next').evaluate('(e)=>e===document.activeElement'),'C4: focus trap')
 page.keyboard.press('Escape');check(page.locator('[data-wall-photo]').first.evaluate('(e)=>e===document.activeElement'),'C4: focus not returned')
 # C5: desktop keyboard group links and scroll-spy; sidebar absent on phone.
 page.goto(BASE+'/services/')
 computed_band_contrast(page)
 page.locator('.band-dark .button.primary').hover();computed_band_contrast(page)
 if width>=900:
  tab_to(page,'.service-group-index a[href="#group-ongoing-care"]');page.keyboard.press('Enter')
  page.wait_for_function("selector=>document.querySelector(selector).classList.contains('active')",arg='.service-group-index a[href="#group-ongoing-care"]')
  check(page.locator('.service-group-index [aria-current="location"]').inner_text()=='Ongoing care','C5: scroll spy')
 else:check(not page.locator('.service-group-index').is_visible(),'C5: sidebar visible on phone')
 # C6: keyboard page navigation and reduced-motion opt-out.
 page.goto(BASE+'/')
 if width<900:
  tab_to(page,'[data-menu]');page.keyboard.press('Enter');tab_to(page,'#menu-sheet a[href="/services/"]')
 else:tab_to(page,'header nav a[href="/services/"]')
 page.keyboard.press('Enter');page.wait_for_url('**/services/')
 check(page.locator('header').evaluate('(e)=>getComputedStyle(e).viewTransitionName')=='site-header','C6: header not named')
 page.emulate_media(reduced_motion='reduce')
 check(page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches'),'C6: reduced-motion environment')
 check(page.locator('header').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s','C6/C7: reduced motion did not disable header transition')
 page.emulate_media(reduced_motion='no-preference')
 # C7: keyboard PageDown/PageUp drives phone header; desktop never hides.
 page.goto(BASE+'/');page.locator('h1').focus();page.keyboard.press('PageDown');page.wait_for_timeout(250)
 if width<900:
  check(page.locator('header').evaluate('(e)=>e.classList.contains("phone-hidden")'),'C7: header did not hide')
  page.keyboard.press('PageUp');page.wait_for_timeout(250);check(not page.locator('header').evaluate('(e)=>e.classList.contains("phone-hidden")'),'C7: header did not return')
  page.locator('[data-menu]').focus();page.keyboard.press('Enter');page.keyboard.press('PageDown');check(not page.locator('header').evaluate('(e)=>e.classList.contains("phone-hidden")'),'C7: hid with menu open');page.keyboard.press('Escape')
 else:check(not page.locator('header').evaluate('(e)=>e.classList.contains("phone-hidden")'),'C7: desktop header hid')
 # C9 tags preserve the pet names and are noninteractive plain text.
 page.goto(BASE+'/team/');check(page.locator('.pet-tags').count()==4,'C9: pets missing')
 check(page.locator('.pet-tags a,.pet-tags button').count()==0,'C9: tags must be plain text')
 check('Cinder' in page.locator('.pet-tags').first.inner_text(),'C9: pet names changed')
 computed_band_contrast(page)
 print(f'V3 keyboard/interaction checks completed at {width}px',flush=True)

# Static checks still run when Chromium is unavailable.
from html.parser import HTMLParser
from urllib.request import urlopen
class StaticPage(HTMLParser):
 def __init__(self):
  super().__init__();self.h1=0;self.images=[];self.links=[];self.ids=[];self.title=False;self.title_text='';self.lang=False;self.description=False;self.canonical=False;self.copy=[];self.skip_copy=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['script','style']:self.skip_copy.append(tag)
  if tag=='img':self.copy.append(a.get('alt',''))
  if tag=='meta' and a.get('name')=='description':self.copy.append(a.get('content',''))
  if tag=='h1':self.h1+=1
  if tag=='img':self.images.append(a)
  if tag=='a':self.links.append(a.get('href',''))
  if 'id' in a:self.ids.append(a['id'])
  if tag=='title':self.title=True
  if tag=='html':self.lang=a.get('lang')=='en-CA'
  if tag=='meta' and a.get('name')=='description':self.description=0<len(a.get('content',''))<=155
  if tag=='link' and a.get('rel')=='canonical':self.canonical=True
 def handle_endtag(self,tag):
  if tag in ['script','style'] and self.skip_copy:self.skip_copy.pop()
  if tag=='title':self.title=False
 def handle_data(self,text):
  if not self.skip_copy:self.copy.append(text)
  if self.title:self.title_text+=text
static={}
for path in paths:
 with urlopen(BASE+path) as response:
  page=StaticPage();page.feed(response.read().decode());static[path]=page
 copy=' '.join(page.copy)
 for pending in re.findall(r'\[CONFIRM:([^\]]+)\]',copy):
  check(pending.strip() in ['a newer, larger portrait of Dr. Garg','photo of Carrie'],path+': unexpected confirmation '+pending)
 banned=['furry friends','fur babies','state-of-the-art','cutting-edge','comprehensive','seamless','elevate','unparalleled','journey','peace of mind']
 check('—' not in copy and '!' not in copy,path+': forbidden punctuation')
 for phrase in banned:check(not re.search(r'\b'+re.escape(phrase)+r'\b',copy,re.I),path+': banned copy '+phrase)
 if path.startswith('/services/') and path!='/services/':
  for phrase in ['plays a critical role','comprehensive','thorough','ensure','designed to','optimal','foundation']:
   check(not re.search(r'\b'+re.escape(phrase)+r'\b',copy,re.I),path+': banned service copy '+phrase)
 check(page.h1==1 and page.lang and page.description and page.canonical,path+': static metadata/H1')
 check(len(page.ids)==len(set(page.ids)),path+': duplicate IDs')
 for image in page.images:check(all(k in image for k in ['alt','width','height','decoding']),path+': image attributes')
for path,page in static.items():
 for link in page.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=u.path or path
  if u.path:
   try:
    with urlopen(BASE+u.path) as response:
     check(response.status==200,path+': broken link '+link);response.read()
   except Exception:errors.append(path+': broken link '+link)
  if u.fragment and not u.fragment.startswith('step-') and target in static:check(unquote(u.fragment) in static[target].ids,path+': missing fragment '+link)
check(len({p.title_text for p in static.values()})==len(static),'Duplicate page titles')
check(json.loads((ROOT/'data/clinic.json').read_text())['bookingLive'] is False,'bookingLive must be false')
service_data=json.loads((ROOT/'data/services.json').read_text())
for service in service_data:
 check(len(service['summary'].split())<=45,service['slug']+': summary word limit')
 check(len(service['description'].split())<=16,service['slug']+': index word limit')
 check(service['summary'] not in service['body'],service['slug']+': repeated summary')
print(f'Static checks: {len(static)} pages, {len(errors)} errors')
if errors:
 print('ERRORS:',json.dumps(errors));server.shutdown();sys.exit(1)
try:
 with sync_playwright() as p:
  try:
   executable=p.chromium.executable_path
   browser=p.chromium.launch(**({} if Path(executable).exists() else {'executable_path':shutil.which('chromium') or executable}))
  except Exception as e:
   print('BLOCKED: Chromium unavailable. Browser tests and screenshots were not run.');print(str(e).splitlines()[0]);sys.exit(2)
  for w,h in [(390,844),(1280,800)]:
   context=browser.new_context(viewport={'width':w,'height':h},timezone_id='America/Vancouver')
   # Belt and braces: any real Google Form submission fails the suite and is aborted.
   def prevent_form(route):posted.append(route.request.url);route.abort()
   context.route('**/forms/**',prevent_form)
   page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append('console: '+m.text) if m.type=='error' else None)
   for path in paths:
    response=page.goto(BASE+path);page.wait_for_load_state('networkidle');loads+=1
    check(response.status==200,f'{path}: HTTP {response.status}')
    check(page.locator('h1').count()==1,f'{path}: H1 count')
    check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{path}: horizontal scroll at {w}')
    check(page.locator('img:not([alt])').count()==0,f'{path}: missing image alt')
    page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode()}))')
    check(page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)'),f'{path}: broken image')
    # Rotation expands an axis-aligned bounding rectangle without enlarging image pixels.
    check(page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.offsetWidth<=i.naturalWidth)'),f'{path}: upscaled image')
    check(page.locator('main img').evaluate_all('(imgs)=>imgs.every(i=>i.offsetWidth<=i.parentElement.clientWidth)'),f'{path}: image wider than its column')
    for link in page.locator('a[href]').evaluate_all('(as)=>as.map(a=>a.getAttribute("href"))'):
     u=urlsplit(link)
     if u.scheme or u.netloc or not u.path:continue
     check(context.request.get(BASE+u.path).status==200,f'{path}: broken link {link}')
    out=ROOT/'review'/f'{path.strip("/").replace("/","-") or "home"}-{w}.png';out.parent.mkdir(exist_ok=True);page.screenshot(path=str(out),full_page=True);screenshots+=1
   page.goto(BASE+'/visit/');page.get_by_role('link',name='Pet emergency?',exact=True).click();check(page.locator('#emergency').is_visible(),'Emergency did not open');page.keyboard.press('Escape');check(not page.locator('#emergency').is_visible(),'Emergency did not close with Escape')
   page.goto(BASE+'/faq/#q-hours');check(page.locator('#q-hours button').get_attribute('aria-expanded')=='true','FAQ hash not open')
   page.goto(BASE+'/book/');check(page.locator('#clinic-data').evaluate('(el)=>JSON.parse(el.textContent).bookingLive') is False,'bookingLive must be false')
   tab_to(page,'#booking-next');page.keyboard.press('Enter');check(page.locator('#err-name').is_visible(),'Name validation absent');check(page.locator('#err-phone').is_visible(),'Phone validation absent')
   tab_to(page,'#name');page.keyboard.type('Review Tester');tab_to(page,'#phone');page.keyboard.type('6045550100');tab_to(page,'#pet');page.keyboard.type('Review Pet')
   tab_to(page,'input[name=species][value=Dog]');page.keyboard.press('Space');tab_to(page,'#booking-next');page.keyboard.press('Enter');check(page.locator('[data-step="2"]').is_visible(),'Step 2 not shown')
   tab_to(page,'input[name=reason]');page.keyboard.press('Space');tab_to(page,'input[name=date]');page.keyboard.press('Space');tab_to(page,'input[name=time][value=Morning]');page.keyboard.press('Space');tab_to(page,'#booking-next');page.keyboard.press('Enter');tab_to(page,'#booking-next');page.keyboard.press('Enter');check(page.locator('#review-mode').is_visible(),'Review mode success absent');check(not posted,'Real booking POST attempted')
   v3_checks(context,page,w)
   context.close()
  for instant,expected in [('2026-10-27T17:00:00Z','Open today until 7 pm'),('2026-10-28T01:45:00Z','Closing soon, at 7 pm'),('2026-10-26T01:00:00Z','Closed now · Opens tomorrow at 8:30 am')]:
   context=browser.new_context(timezone_id='America/Vancouver');page=context.new_page();page.clock.install(time=instant);page.goto(BASE+'/');check(expected in page.locator('[data-today]').first.inner_text(),f'Today line incorrect at {instant}');context.close()
  for instant,kind in [('2026-10-27T17:00:00Z','clinic'),('2026-10-28T04:00:00Z','after-hours')]:
   context=browser.new_context(timezone_id='America/Vancouver');page=context.new_page();page.clock.install(time=instant);page.goto(BASE+'/visit/');page.get_by_role('link',name='Pet emergency?',exact=True).click()
   check(page.locator('#emergency [data-emergency-contacts]>div').first.get_attribute('data-contact-kind')==kind,'A1: emergency order at '+instant)
   if kind=='after-hours':check(page.locator('#emergency h2').inner_text()=="We're closed right now.",'A1: closed heading')
   page.keyboard.press('Escape');check(page.locator('.chart-row.is-today').count()==1,'C2: today chart row missing')
   check(page.locator('.chart-row.is-today .now-marker').is_visible(),'C2: now marker missing')
   check('Open now · closes at 7 pm' in page.locator('[data-chart-status]').inner_text() if kind=='clinic' else 'Closed now' in page.locator('[data-chart-status]').inner_text(),'C2: chart live status')
   check(page.locator('.sr-only .hours').count()==1,'C2: accessible table missing');context.close()
  browser.close()
except SystemExit:raise
except Exception as e:errors.append(str(e))
finally:server.shutdown()
print(f'Page loads: {loads}; screenshots: {screenshots}; real form submissions: {len(posted)}')
print('ERRORS:',json.dumps(errors,ensure_ascii=False))
sys.exit(bool(errors))
