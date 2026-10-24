import json, re, sys
OUT = sys.argv[1] if len(sys.argv)>1 else 'dist/index.html'
C = json.load(open("data/content.json"))
tpl = open("template.html").read()
import os; os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)

# --- services: tidy names and typos
NAMES = {"Preventative Care":"Preventive care","Vaccinations":"Vaccinations","Parasite Prevention":"Parasite prevention","Microchipping":"Microchipping",
 "Chronic Pain Management":"Chronic pain management","Small Mammal Medicine":"Small mammal medicine","Bloodwork":"Bloodwork","Anesthesia":"Anesthesia",
 "Dog Breeding":"Breeding support for dogs","Boarding":"Cat boarding"}
FIX = [("deepy","deeply"),("surgery ,","surgery,"),(" ,",","),("  "," ")]
svc = []
for s in C["services"]:
    s = dict(s); s["name"] = NAMES.get(s["name"], s["name"])
    for k in ("intro",):
        for a,b in FIX: s[k] = s[k].replace(a,b)
    s["more"] = [re.sub(r"\s+([,.])",r"\1",p).replace("deepy","deeply") for p in s["more"]]
    s["intro"] = re.sub(r"\s+([,.])",r"\1",s["intro"]); s["points"]=[re.sub(r"\s+([,.])",r"\1",p) for p in s["points"]]
    svc.append(s)

# --- plants (exported once from the original code; the starter never needs the developer repo)
_p = json.load(open("data/plants.json")); plants = _p["plants"]; tox = _p["tox"]

FAQ = [
 dict(q="What are your opening hours?", a="Monday to Friday 8:30am to 7pm, and Saturday and Sunday 9am to 5pm."),
 dict(q="Where are you?", a="Unit 101A, 20995 88 Avenue, Langley, BC V1M 2C9, in Walnut Grove. Call us at (604) 888-2628."),
 dict(q="Which animals do you see?", a="Dogs, cats, and small mammals such as rabbits and pocket pets. Our boarding is for cats."),
 dict(q="What should I do in an emergency?", a="During opening hours, come straight to the hospital and call (604) 888-2628 on the way so we can be ready. Outside opening hours, contact the nearest 24-hour emergency clinic.", confirm=True),
 dict(q="Can I book online?", a="Yes. Choose your pet, the reason and a time on the <a href='#book'>booking page</a>, any time of day. You can also call us."),
 dict(q="Are you taking new patients?", a="Yes, we welcome new patients. Book online or call to arrange a first visit.", confirm=True),
 dict(q="What should I bring to my pet's first visit?", a="Any past vet records, a list of your pet's food and medicines, and a carrier for cats or a leash for dogs."),
 dict(q="Do you offer boarding?", a="Yes, we offer boarding for cats, with individual care. Ask us about availability."),
 dict(q="What if my pet eats something poisonous?", a="Call us right away at (604) 888-2628. See our <a href='#petcare'>pet care page</a> for plants and foods to keep away from pets."),
]
schema = {"@context":"https://schema.org","@graph":[
 {"@type":"VeterinaryCare","name":"Walnut Grove Animal Hospital","telephone":"+1-604-888-2628",
  "address":{"@type":"PostalAddress","streetAddress":"101A-20995 88 Ave","addressLocality":"Langley","addressRegion":"BC","postalCode":"V1M 2C9","addressCountry":"CA"},
  "geo":{"@type":"GeoCoordinates","latitude":49.1628596,"longitude":-122.655538},
  "hasMap":"https://www.google.com/maps/place/Walnut+Grove+Animal+Hospital+Langley/@49.1629613,-122.6546539,17z",
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:30","closes":"19:00"},
   {"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday"],"opens":"09:00","closes":"17:00"}],
  "sameAs":["https://www.facebook.com/walnutgroveanimalhospitalbc","https://www.instagram.com/walnutgroveanimalhospitalbc/"],
  "availableService":[{"@type":"MedicalProcedure","name":s["name"]} for s in svc]},
 {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",f["a"])}} for f in FAQ if not f.get("confirm")]}]}

I = C["imgs"]
js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
html = (tpl.replace("__SCHEMA__", js(schema)).replace("__SERVICES__", js(svc)).replace("__PLANTS__", js(plants)).replace("__TOX__", js(tox)).replace("__FAQ__", js(FAQ))
        .replace("__LOGO__", I["logo"]).replace("__HERO__", I["hero"]).replace("__EXTERIOR__", I["exterior"]).replace("__ENTRANCE__", I["entrance"]).replace("__DESKCAT__", I["deskcat"]))
assert "__" not in re.sub(r"data:[^\"']+", "", html).replace("__proto__",""), [m for m in re.findall(r"__[A-Z]+__", html)]
open(OUT, "w").write(html)
print("plants groups", len(plants), "tox", tox, "size KB", len(html)//1024)
