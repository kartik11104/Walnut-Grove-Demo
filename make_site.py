"""Builds the deployable demo site into site/ (full HTML document, noindex)."""
import subprocess, os, re
subprocess.run(["python3","build.py","dist/index.html"],check=True)
body=open("dist/index.html").read()
i=body.index('<a class="skip"')
head,main=body[:i],body[i:]
doc=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
     +head+'</head>\n<body>\n'+main+'\n</body>\n</html>\n')
os.makedirs("site",exist_ok=True)
open("site/index.html","w").write(doc)
open("site/robots.txt","w").write("User-agent: *\nDisallow: /\n")
print("site/index.html",len(doc)//1024,"KB")
