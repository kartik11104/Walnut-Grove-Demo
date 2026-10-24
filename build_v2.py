"""Build V2 only. Install requirements-v2.txt, then python3 build_v2.py."""
from pathlib import Path
import sys,json,re,html,shutil,os
sys.path.insert(0,str(Path(__file__).parent/'.build-deps'))
from jinja2 import Environment,FileSystemLoader,select_autoescape
from markupsafe import Markup
import markdown
from PIL import Image
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
SHOW_CONFIRM=True
SITE_URL=os.environ.get('SITE_URL','https://example.invalid').rstrip('/')
def clean(t):
 t=t.replace('—',', ').replace('!', '.').replace('deepy','deeply')
 for a,b in {'comprehensive':'thorough','state-of-the-art':'modern','cutting-edge':'modern','seamless':'simple','elevate':'improve','unparalleled':'dedicated','journey':'care','peace of mind':'reassurance','furry friends':'pets','fur babies':'pets'}.items():t=re.sub(re.escape(a),b,t,flags=re.I)
 for a,b in {'behavior':'behaviour','Behavior':'Behaviour','anemia':'anaemia','tumors':'tumours','personalized':'personalised','customized':'customised','center':'centre','color':'colour','recognize':'recognise','orthopedic':'orthopaedic'}.items():t=t.replace(a,b)
 return t

def source(name):return (ROOT/'source/text'/name).read_text()
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def paras(t):return [re.sub(r'\s+',' ',x).strip() for x in re.split(r'\n\s*\n',t) if x.strip() and not x.lstrip().startswith(('#','*','●'))]
def md(t):return Markup(markdown.markdown(clean(t),extensions=['tables','toc','sane_lists']))
def confirm(text):return Markup('<span class="confirm">[CONFIRM: '+html.escape(text)+']</span>') if SHOW_CONFIRM else Markup('')
def photo(name,alt,limit=None,eager=False):
 path=ROOT/'assets/photos'/f'{name}.webp';w,h=Image.open(path).size
 return Markup(f'<img src="/assets/photos/{name}.webp" alt="{html.escape(alt,quote=True)}" width="{w}" height="{h}" style="max-width:{min(w,limit or w)}px" decoding="async" loading="{"eager" if eager else "lazy"}">')
def save(name,data): (ROOT/'data'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Source slugs deliberately remain unchanged.
GROUPS={'Everyday care':[('preventative-care','Wellness exams'),('vaccines','Vaccines'),('parasite-prevention','Parasite prevention'),('puppy-kitten-care','Puppy and kitten care'),('microchipping','Microchipping')], 'Finding answers':[('bloodwork','Bloodwork'),('lab-services','Lab services'),('pet-x-ray','Digital X-ray'),('ultrasound-services','Ultrasound')], 'Surgery and dental':[('spay-neuter','Spay and neuter'),('pet-surgery','Pet surgery'),('soft-tissue-eye-ear','Soft tissue, eye and ear surgery'),('dental-services','Dental care'),('anesthesia','Anesthesia')], 'Ongoing care':[('skin-ear-infections','Skin and ear problems'),('chronic-pain-management','Chronic pain'),('small-mammal-medicine','Small mammal medicine'),('dog-breeding','Dog breeding'),('pet-boarding-services','Boarding'),('euthanasia','End-of-life care')]}
clinic={'name':'Walnut Grove Animal Hospital','phone':'(604) 888-2628','tel':'+16048882628','address':'101A-20995 88 Ave, Langley, BC V1M 2C9','geo':[49.16296,-122.63920],'hours':[[9,0,17,0],[8,30,19,0],[8,30,19,0],[8,30,19,0],[8,30,19,0],[8,30,19,0],[9,0,17,0]],'bookingLive':False,'instagram':'https://www.instagram.com/walnutgroveanimalhospitalbc/','facebook':'https://www.facebook.com/walnutgroveanimalhospitalbc/','formEndpoint':'https://docs.google.com/forms/d/e/1FAIpQLScJA4N82tv0x5Ek5wLkXZteAvFi0kyf3CBZqdagPe8AmGja3w/formResponse'}
# Preserve the review safety switch; only an explicit owner-approved configuration may enable it.
if Path('data/clinic.json').exists():clinic=json.loads(Path('data/clinic.json').read_text())
save('clinic.json',clinic)
rawfaq=source('faq.md');qparts=re.split(r'^### ',rawfaq,flags=re.M)[1:];faq=[]
for part in qparts:
 q,_,answer=part.partition('\n');answer=clean(re.sub(r'\s+',' ',answer).strip());sentences=re.split(r'(?<=[.?])\s+',answer);short=''
 for sentence in sentences:
  if len((short+' '+sentence).split())>80:break
  short+=' '+sentence
 q=clean(q.strip(' *'));low=q.lower()
 group='Vaccines and prevention'
 if any(k in low for k in ['surg','anesth','anaesth']):group='Surgery and anesthesia'
 if any(k in low for k in ['spay','neuter']):group='Spay and neuter'
 if any(k in low for k in ['breed','pregnan','puppies are born']):group='Breeding'
 if any(k in low for k in ['goodbye','procedure?','after the procedure','comfortable if','environment do you provide','during the process']):group='End-of-life care'
 if any(k in low for k in ['blood','lab test','x-ray','x-rays','ultrasound','cbc','sedated','shaved','meal prior','fast prior']):group='Tests and imaging'
 faq.append({'id':'q-'+slug(q),'q':q,'a':short.strip() or ' '.join(answer.split()[:80]),'group':group})
# Remove repeated IDs if source questions repeat.
faq=list({q['id']:q for q in faq}.values());save('faq.json',faq)
services=[]
for group,items in GROUPS.items():
 for key,name in items:
  text=source('services_'+key+'.md');text=text[text.index('## '):];text=re.split(r'^## Answers|^### RELATED|^## HERE',text,flags=re.M)[0]
  body=text.split('\n',1)[1];ps=paras(body);intro=clean(ps[0]) if ps else '';summary=' '.join(re.split(r'(?<=[.])\s+',intro)[:1]);summary=' '.join(summary.split()[:45])
  # Keep medical content from source, excluding navigation and standalone booking calls to action.
  body=re.sub(r'(?m)^(Schedule|Book|Request|Update|Contact|Explore|Learn More|Call)[^\n]*$','',body)
  symptoms=[]
  if key=='dental-services':symptoms=['Persistent bad breath','Fractured or broken teeth','Oral infections or inflammation']
  related=[{'slug':a,'name':b} for a,b in items if a!=key][:3]
  terms=set(re.findall(r'[a-z]+',name.lower()))-{'and','care','pet','services','medicine','problems'}
  questions=[q for q in faq if any(re.search(r'\b'+re.escape(term)+r'\w*\b',q['q'].lower()) for term in terms)]
  services.append({'slug':key,'name':name,'group':group,'summary':summary,'body':clean(body),'when':symptoms,'questions':questions,'related':related,'before':[q for q in questions if any(x in q['q'].lower() for x in ['fast','meal prior'])]})
save('services.json',services)
# Parse plants directly from the supplied resource, preserving every group/list entry.
plants=[];ptext=source('resources_poisonous-plants.md')
for title,body in re.findall(r'^### (.+)\n(.*?)(?=^#{2,3} |\Z)',ptext,re.M|re.S):
 items=re.findall(r'^\s*\* (.+)',body,re.M)
 if items:plants.append({'name':title,'items':items})
save('plants.json',plants)
posts=[];index=source('blog.md');date_matches=list(re.finditer(r'(Oct|Sep) (\d+), 2026[•\s]*4 min read\s*\n\s*#{2,4} (.+)',index))
for p in sorted(Path('source/text').glob('blog_*.md')):
 key=p.stem[5:];raw=p.read_text();raw=raw.split('Pet Care Tips\n')[-1] if False else raw[raw.index('Pet Care Tips',raw.index('Request Appointment'))+len('Pet Care Tips'):].strip()
 raw=re.split(r'^### Related Articles|^## HAVE QUESTIONS|^Continue Reading|^Walnut Grove Veterinary Team|^Share this|^Topic Tags:|^Written by',raw,flags=re.M)[0].strip()
 topic=next(x for x in ['vaccinations','ultrasound','microchipping','diagnostics','preventative'] if key.startswith('pet-'+x) or key.startswith(x))
 m=next(m for m in date_matches if topic.lower() in m[3].lower())
 title=m[3].strip('* ');date=f'2026-{"10" if m[1]=="Oct" else "09"}-{int(m[2]):02d}'
 intro=paras(raw);posts.append({'slug':key,'title':clean(title),'date':date,'date_label':f'{m[1]} {m[2]}, 2026' if m else date,'read':'4 min read','body':clean(raw),'summary':clean(intro[0]) if intro else title})
posts.sort(key=lambda p:p['date'],reverse=True);save('posts.json',posts)
if not Path('data/reviews.json').exists():save('reviews.json',[])
reviews=json.loads(Path('data/reviews.json').read_text())
env=Environment(loader=FileSystemLoader('templates'),autoescape=select_autoescape(['html']))
env.globals.update(photo=photo,confirm=confirm,md=md,clinic=clinic,groups=GROUPS,services=services,faq=faq,posts=posts,plants=plants,reviews=reviews,SHOW_CONFIRM=SHOW_CONFIRM)
nav=[('/services/','Services'),('/team/','Our team'),('/pet-care/','Pet care'),('/blog/','Blog'),('/visit/','Visit')];env.globals['nav']=nav
schema={'@context':'https://schema.org','@type':'VeterinaryCare','name':clinic['name'],'telephone':clinic['phone'],'address':{'@type':'PostalAddress','streetAddress':'101A-20995 88 Ave','addressLocality':'Langley','addressRegion':'BC','postalCode':'V1M 2C9','addressCountry':'CA'},'geo':{'@type':'GeoCoordinates','latitude':clinic['geo'][0],'longitude':clinic['geo'][1]},'openingHours':['Mo-Fr 08:30-19:00','Sa-Su 09:00-17:00'],'sameAs':[clinic['instagram'],clinic['facebook']]}
Path('site/assets').mkdir(parents=True,exist_ok=True)
for name in ['site.css','site.js']:shutil.copyfile('templates/'+name,'site/assets/'+name)
for directory in ['photos','fonts']:shutil.copytree('assets/'+directory,'site/assets/'+directory,dirs_exist_ok=True)
shutil.copyfile('assets/logo.png','site/assets/logo.png')
pages=[]
def render(path,title,template,**kwargs):
 out=Path('site')/(path.strip('/')+'/index.html' if path!='/' else 'index.html');
 if path=='/404.html':out=Path('site/404.html')
 out.parent.mkdir(parents=True,exist_ok=True)
 description=kwargs.pop('description',title+' at Walnut Grove Animal Hospital in Langley. Call (604) 888-2628.')[:155]
 out.write_text(env.get_template(template).render(path=path,title=title,description=description,canonical=SITE_URL+path,schema=schema,clinic_json=json.dumps(clinic),**kwargs));pages.append(path)
for path,title,template in [('/','Home','home.html'),('/services/','Services','services.html'),('/team/','Our team','team.html'),('/visit/','Visit us','visit.html'),('/pet-care/','Pet care','pet-care.html'),('/faq/','Questions we hear a lot','faq.html'),('/blog/','Pet health blog','blog.html'),('/book/','Book a visit','book.html'),('/privacy/','Privacy','privacy.html'),('/404.html',"We can't find that page.",'404.html')]:
 if Path('templates',template).exists():render(path,title,template)
if Path('templates/service.html').exists():
 for s in services:render('/services/'+s['slug']+'/',s['name'],'service.html',service=s)
if Path('templates/post.html').exists():
 for post in posts:render('/blog/'+post['slug']+'/',post['title'],'post.html',post=post)
Path('site/robots.txt').write_text('User-agent: *\nDisallow: /\n')
Path('site/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(SITE_URL+p)+'</loc></url>' for p in pages if p!='/404.html')+'</urlset>\n')
Path('site/assets/clinic.vcf').write_text('BEGIN:VCARD\nVERSION:3.0\nFN:Walnut Grove Animal Hospital\nTEL;TYPE=WORK:+16048882628\nADR;TYPE=WORK:;;101A-20995 88 Ave;Langley;BC;V1M 2C9;Canada\nEND:VCARD\n')
assert len(Path('site/assets/site.css').read_bytes())<=40000
assert len(Path('site/assets/site.js').read_bytes())<=30000
print(f'V2 build: {len(pages)} pages; {len(services)} services; {len(posts)} posts; bookingLive={clinic["bookingLive"]}; SHOW_CONFIRM={SHOW_CONFIRM}')
print('CSS:',Path('site/assets/site.css').stat().st_size,'bytes; JS:',Path('site/assets/site.js').stat().st_size,'bytes')
print('Canonical origin:',SITE_URL)
