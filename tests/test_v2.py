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
   context.close()
  for instant,expected in [('2026-10-27T17:00:00Z','Open today until 7 pm'),('2026-10-28T01:45:00Z','Closing soon, at 7 pm'),('2026-10-26T01:00:00Z','Closed now · Opens tomorrow at 8:30 am')]:
   context=browser.new_context(timezone_id='America/Vancouver');page=context.new_page();page.clock.install(time=instant);page.goto(BASE+'/');check(expected in page.locator('[data-today]').first.inner_text(),f'Today line incorrect at {instant}');context.close()
  browser.close()
except SystemExit:raise
except Exception as e:errors.append(str(e))
finally:server.shutdown()
print(f'Page loads: {loads}; screenshots: {screenshots}; real form submissions: {len(posted)}')
print('ERRORS:',json.dumps(errors,ensure_ascii=False))
sys.exit(bool(errors))
