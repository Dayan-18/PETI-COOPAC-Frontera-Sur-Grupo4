import re
s=open('build_docx.py',encoding='utf8').read()
a=s.index("# --- cover"); b=s.index("children = list(body)")
new='''# --- cover
def setpar(p, txt):
    ts = list(p.iter(q("t")))
    ts[0].text = txt
    for t in ts[1:]: t.text = ""
for p in tree.getroot().iter(q("p")):
    tx = ptext(p)
    if "……" in tx and pstyle(p) == "Centrado":
        if not hasattr(setpar, "n"): setpar.n = 0
        setpar(p, ["REGISTRO DE RIESGOS DEL PLAN Y MATRIZ DE COMUNICACIÓN — COOPAC FRONTERA SUR (SEMANA 15)", "SI-886 PLANEAMIENTO ESTRATÉGICO DE TI"][setpar.n]); setpar.n += 1
    elif "20232023077090" in tx:
        for t in p.iter(q("t")):
            if t.text and "20232023077090" in t.text: t.text = t.text.replace("20232023077090", "2023077090")
        if "20232023077090" in ptext(p): setpar(p, "SIERRA RUIZ, IKER ALBERTO - 2023077090")

'''
s=s[:a]+new+s[b:]
s=s.replace("[520, 1000, 3640, 1250, 1100, 300, 300, 450, 790]","[500, 950, 3700, 1200, 1050, 300, 300, 550, 800]")
open('build_docx.py','w',encoding='utf8').write(s)
