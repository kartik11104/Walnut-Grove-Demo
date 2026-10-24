import os,sys
from playwright.sync_api import sync_playwright
body=open("dist/index.html").read()
doc="<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'></head><body>"+body+"</body></html>"
open("dist/_w.html","w").write(doc); url="file://"+os.path.abspath("dist/_w.html")
errs=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for scheme in ("light","dark"):
    for w,h,tag in ((1300,900,"desk"),(390,844,"phone")):
      pg=b.new_page(viewport={"width":w,"height":h},color_scheme=scheme,device_scale_factor=1)
      pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None); pg.on("pageerror",lambda e: errs.append(str(e)))
      for v in ("home","services","book","team","petcare","faq","visit"):
        pg.goto(url+"#"+v); pg.wait_for_timeout(500 if v=="home" else 150)
        sw=pg.evaluate("document.documentElement.scrollWidth")
        if sw>w: errs.append(f"{scheme} {tag} {v} overflow {sw}")
        if scheme=="light" or v in ("home","book"):
          pg.screenshot(path=f"dist/s_{scheme}_{tag}_{v}.png",full_page=(v in("home","services")))
      pg.close()
  # booking flow test
  pg=b.new_page(viewport={"width":1300,"height":900}); pg.on("pageerror",lambda e: errs.append(str(e)))
  pg.goto(url+"#book"); pg.wait_for_timeout(300)
  pg.click("#next"); assert pg.is_visible("#err0"), "validation 0"
  pg.check("#sp-dog"); pg.fill("#petName","Biscuit"); pg.check("#cl-new"); pg.click("#next")
  pg.select_option("#reason","vaccines"); pg.fill("#notes","he ate chocolate last night"); pg.wait_for_timeout(100)
  emerg=pg.is_visible("#emergencyBox"); pg.fill("#notes","annual shots"); pg.wait_for_timeout(100); emerg_off=not pg.is_visible("#emergencyBox")
  pg.click("#next"); pg.click(".date >> nth=2"); pg.click(".slot:not([disabled]) >> nth=1"); pg.click("#next")
  pg.fill("#ownerName","Test Owner"); pg.fill("#phone","604 555 0100"); pg.check("#remind")
  pg.screenshot(path="dist/s_book_step4.png"); pg.click("#next"); pg.wait_for_timeout(200)
  done=pg.is_visible("#doneBox"); title=pg.text_content("#doneTitle"); summ=pg.text_content("#summary")
  pg.screenshot(path="dist/s_book_done.png")
  # service drawer
  pg.goto(url+"#services"); pg.wait_for_timeout(200); pg.click("#svcGrid .svc >> nth=3"); pg.wait_for_timeout(400); pg.screenshot(path="dist/s_drawer.png")
  drawer=pg.evaluate("document.querySelector('#drawer').classList.contains('on')"); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
  closed=not pg.evaluate("document.querySelector('#drawer').classList.contains('on')")
  # filter
  pg.click("#svcFilter .pill >> text=Surgery"); n=pg.locator("#svcGrid .svc").count()
  # book this from drawer presets reason
  pg.click("#svcGrid .svc >> nth=0"); pg.wait_for_timeout(300); pg.click("#dBook"); pg.wait_for_timeout(300); pre=pg.input_value("#reason")
  print(dict(emerg=emerg,emerg_off=emerg_off,done=done,title=title,summary=summ,drawer=drawer,closed=closed,surgery_count=n,preset=pre))
  b.close()
print("ERRORS:",errs)
