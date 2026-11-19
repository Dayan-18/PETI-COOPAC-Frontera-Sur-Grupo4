s=open('build_docx.py',encoding='utf8').read()
s=s.replace('next(r[2] for r in RIESGOS if r[0] == i)[:95] + "…"','next(r[1] for r in RIESGOS if r[0] == i)')
s=s.replace('"Riesgo (resumen)", "Residual"','"Categoría del riesgo", "Residual"')
open('build_docx.py','w',encoding='utf8').write(s)
