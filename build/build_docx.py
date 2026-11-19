# -*- coding: utf-8 -*-
import os, re, sys, shutil, zipfile
from xml.sax.saxutils import escape
from lxml import etree
sys.path.insert(0, os.path.dirname(__file__))
from data import *

SRC = r"C:\Users\HP\Downloads\aaaaaaaa\SI886-PLANTILLA-TALLER (1).docx"
OUT = r"C:\Users\HP\Downloads\aaaaaaaa\SI886-S15-TALLER-Grupo4.docx"
UN = r"C:\Users\HP\Downloads\aaaaaaaa\build\un"
PNG = r"C:\Users\HP\Downloads\aaaaaaaa\graficos\RG_mapa_calor.png"

shutil.rmtree(UN, ignore_errors=True)
zipfile.ZipFile(SRC).extractall(UN)

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = ('xmlns:w="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"' % W)

# ---------- helpers ----------
def runs(text, sz=None, bold=False):
    out = []
    for part in re.split(r"(\*\*.+?\*\*|`.+?`)", text):
        if not part: continue
        rpr = ""
        if part.startswith("**"):
            part = part[2:-2]; rpr = "<w:b/><w:bCs/>"
        elif part.startswith("`"):
            part = part[1:-1]; rpr = '<w:rStyle w:val="VerbatimChar"/>'
        if bold and "<w:b/>" not in rpr: rpr += "<w:b/><w:bCs/>"
        if sz: rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % ("<w:rPr>%s</w:rPr>" % rpr if rpr else "", escape(part)))
    return "".join(out)

def P(text, style="FirstParagraph", keep=False):
    k = "<w:keepNext/>" if keep else ""
    return '<w:p><w:pPr><w:pStyle w:val="%s"/>%s</w:pPr>%s</w:p>' % (style, k, runs(text))

def H2(text):
    return '<w:p><w:pPr><w:pStyle w:val="Ttulo2"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>' % escape(text)

def CODE(lines):
    return "".join('<w:p><w:pPr><w:pStyle w:val="SourceCode"/><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:rPr><w:rStyle w:val="VerbatimChar"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(l) for l in lines)

def CAP(text):
    return '<w:p><w:pPr><w:pStyle w:val="Compact"/><w:spacing w:before="60" w:after="160"/></w:pPr>%s</w:p>' % runs("*"+text if False else text, sz=18)

def TABLE(widths, header, rows, sz=16):
    total = sum(widths)
    b = '<w:top w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:left w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:right w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>'
    x = '<w:tbl><w:tblPr><w:tblStyle w:val="Table"/><w:tblW w:w="%d" w:type="dxa"/><w:tblBorders>%s</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="60" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="0420" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>' % (total, b, "".join('<w:gridCol w:w="%d"/>' % w for w in widths))
    def cell(t, w, head=False):
        shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if head else ""
        return '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/><w:spacing w:before="20" w:after="20"/><w:jc w:val="left"/></w:pPr>%s</w:p></w:tc>' % (w, shade, runs(str(t), sz=sz, bold=head))
    x += '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>%s</w:tr>' % "".join(cell(h, w, True) for h, w in zip(header, widths))
    for r in rows:
        x += '<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>' % "".join(cell(c, w) for c, w in zip(r, widths))
    return x + '</w:tbl>' + '<w:p><w:pPr><w:pStyle w:val="Compact"/><w:spacing w:before="0" w:after="60"/></w:pPr></w:p>'

def IMG(rid, cx, cy, name):
    return ('<w:p><w:pPr><w:pStyle w:val="Compact"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="%d" cy="%d"/><wp:docPr id="900" name="%s"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="900" name="%s"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>' % (cx, cy, name, name, rid, cx, cy))

def frag(s):
    root = etree.fromstring("<w:body %s>%s</w:body>" % (NS, s))
    return list(root)

# ---------- load ----------
dpath = UN + r"\word\document.xml"
tree = etree.parse(dpath)
body = tree.getroot().find("{%s}body" % W)
q = lambda t: "{%s}%s" % (W, t)

def ptext(e):
    return "".join(t.text or "" for t in e.iter(q("t")))
def pstyle(e):
    s = e.find("%s/%s" % (q("pPr"), q("pStyle")))
    return s.get(q("val")) if s is not None else None

# --- cover
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

children = list(body)
# --- index: drop "Cómo se usa" entry
for e in children:
    if pstyle(e) == "TDC1" and ptext(e).startswith("Cómo se usa"):
        body.remove(e)
children = list(body)
# --- remove "Cómo se usa" section
i_como = next(i for i, e in enumerate(children) if pstyle(e) == "Ttulo1" and ptext(e).startswith("Cómo se usa"))
i_info = next(i for i, e in enumerate(children) if pstyle(e) == "Ttulo1" and ptext(e).startswith("1. Información"))
for e in children[i_como:i_info - 1]:   # conserva el párrafo previo al encabezado 1
    body.remove(e)
children = list(body)
i_info = next(i for i, e in enumerate(children) if pstyle(e) == "Ttulo1" and ptext(e).startswith("1. Información"))
sect = children[-1]
assert sect.tag == q("sectPr")
old = children[i_info + 1:-1]
heads = {}
for e in old:
    if pstyle(e) in ("Ttulo1", "Ttulo2"):
        heads[ptext(e).strip()] = e
for e in old: body.remove(e)

import copy
def head(text_old, text_new=None):
    e = copy.deepcopy(heads[text_old])
    if text_new:
        ts = list(e.iter(q("t")))
        ts[0].text = text_new
        for t in ts[1:]: t.text = ""
    return e
def newhead(text):
    return frag(H2(text))[0]

out = []
def add(s):
    out.extend(frag(s))

# ---------- 1.1 ... 1.6 ----------
out.append(head("1.1 Título del evento práctico"))
add(P("**Registro de riesgos del plan y matriz de comunicación** — Semana 15, SI-886 Planeamiento Estratégico de TI. Caso de la organización asignada al equipo: **COOPAC Frontera Sur** (empresa 04 del banco de casos)."))
out.append(head("1.2 Objetivos"))
for i, o in enumerate([
    "Definir el contexto y los criterios de riesgo del plan, acordados con la gerencia **antes** de evaluar.",
    "Identificar riesgos sobre las nueve categorías, sin omitir ninguna.",
    "Evaluar cada riesgo con escalas definidas previamente y justificar la probabilidad y el impacto con un dato.",
    "Determinar el tratamiento y el riesgo residual de cada riesgo, con su señal temprana y su umbral de alerta.",
    "Registrar los riesgos en SimpleRisk, generar el mapa de calor y construir la matriz de comunicación del riesgo.",
    "Redactar la Sección 8 del PETI (Plan Estratégico de Tecnologías de Información)."], 1):
    add(P("**O%d.** %s" % (i, o), "Compact"))
out.append(head("1.3 Tiempo de duración"))
add(P("100 minutos de taller en laboratorio (Sesión 2 de la Semana 15), más el tiempo de consolidación del informe y del repositorio del equipo."))
out.append(head("1.4 Resultados de aprendizaje"))
add(P("**RA1.** Aplica la guía metodológica para la elaboración de un Plan. Contenido procedimental del sílabo: identificar los riesgos y definir la acción para su tratamiento; comunicar las acciones para tratar el riesgo."))
out.append(head("1.5 Recursos"))
add(TABLE([2600, 1500, 5250], ["Recurso", "Versión", "Para qué se usó"], [
    ("Python", "3.13", "Ejecución de `RG03_evaluacion.py` y `RG05_residual.py`"),
    ("pandas / numpy", "3.0.5 / 2.5.3", "Cálculo de probabilidad × impacto, riesgo residual y detección de riesgos sin señal temprana"),
    ("matplotlib", "3.11.2", "Mapa de calor de riesgos (`RG_mapa_calor.png`)"),
    ("Docker (SimpleRisk + MariaDB)", "[completar]", "Registro de los riesgos ≥ 12 con escalas y criterio de aceptación — **pendiente de ejecutar**"),
    ("Git y GitHub", "Git 2.55", "Control de versiones; el historial prueba que los criterios se fijaron antes de evaluar"),
    ("ISO 31000:2018", "—", "Marco del proceso de gestión de riesgos"),
    ("Casos de COOPAC Frontera Sur", "mayo–junio 2026", "`politica-de-respaldo.md`, `bia.csv` y `universo-auditable-y-riesgos.md` como fuentes de identificación"),
], sz=17))
out.append(head("1.6 Seguridad"))
add(P("El registro de riesgos expone vulnerabilidades de ejecución de la organización: es información **Confidencial**. Los riesgos que involucran a personas (patrocinio, personal clave) se redactaron por **cargo**, describiendo el riesgo estructural y no la conducta de un individuo. Los criterios se fijaron antes de evaluar, y la aceptación del riesgo residual requiere la firma del dueño del riesgo: el equipo formulador no la da en su nombre (ver Anexo F).", "FirstParagraph"))

# ---------- 2 ----------
out.append(head("2. Procedimiento o metodología"))
add(P("Cada paso indica qué se buscaba, el archivo que se crea (ruta dentro del repositorio del equipo), el comando y la evidencia. Las cifras provienen de los documentos de COOPAC Frontera Sur; las probabilidades e impactos son una **propuesta del equipo**, sujeta a validación con la gerencia."))

# Paso A
out.append(head("Paso A", "Paso A — Contexto y criterios"))
add(P("**Se buscaba** fijar el alcance, las escalas y el criterio de aceptación antes de evaluar cualquier riesgo. **Archivo:** `08_riesgos/RG01_contexto.md`."))
add(TABLE([2300, 7050], ["Campo", "Contenido"], [
    ("Alcance", "Riesgos que amenazan la **ejecución del PETI Año 1 – Año 3** de COOPAC Frontera Sur. Excluye los riesgos operativos de TI ya tratados en el portafolio y los riesgos de negocio (PEI)."),
    ("Horizonte", "3 años"),
    ("Escalas", "Probabilidad e impacto de 1 a 5, con la definición operativa de las tablas siguientes"),
    ("Criterio de aceptación", "≤ 6 aceptable con documentación · 7–14 requiere tratamiento con plazo · ≥ 15 requiere decisión de la gerencia general antes de aprobar el plan"),
    ("Dueños de riesgo", "Por cargo: Gerencia General, Gerencia de Administración y Finanzas, Jefe de TI, Jefe de Auditoría Interna"),
    ("Frecuencia de revisión", "Trimestral, y ante cualquier hito de decisión de la hoja de ruta"),
    ("Fecha de acuerdo de los criterios", "**[completar: fecha del commit de RG01_contexto.md, anterior a la evaluación]**"),
], sz=17))
add(TABLE([700, 1500, 7150], ["P", "Probabilidad", "Definición operativa"], [(a, b, c) for a, b, c in ESCALA_P], sz=17))
add(TABLE([700, 1500, 7150], ["I", "Impacto", "Definición operativa"], [(a, b, c) for a, b, c in ESCALA_I], sz=17))
add(P("**Evidencia de fecha:** `git log --follow --date=iso --format=\"%h %ad %s\" 08_riesgos/RG01_contexto.md` — **[pegar salida y URL del archivo]**.", "Compact"))

# Paso B
out.append(head("Paso B", "Paso B — Identificar sobre las nueve categorías"))
add(P("**Se buscaba** un registro con las nueve categorías cubiertas y cada riesgo redactado como evento + causa + consecuencia. **Archivo:** `08_riesgos/RG02_registro.csv`. Las fuentes fueron la política de respaldo, el BIA y el universo auditable de la organización; la política declara lo que la organización dice hacer y las respuestas de la sección «Lo que la organización responde» muestran lo que hace. **[Agregar los riesgos del pre-mortem de la dinámica del equipo, si aportan alguno distinto.]**"))
add(TABLE([500, 950, 3700, 1200, 1050, 300, 300, 550, 800],
          ["id", "Categoría", "Riesgo (evento + causa + consecuencia)", "Afecta", "Origen", "P", "I", "Valor", "Nivel"],
          [(i, c, r, a, o, p, im, "**%d**" % v, n) for i, c, r, a, o, p, im, v, n in filas_registro()], sz=14))
add(P("**Hallazgos del contraste entre lo declarado y lo real** (insumo del registro): la política exige una prueba de restauración trimestral y no se ha hecho nunca; la copia fuera de las instalaciones es un disco que el jefe de sistemas se lleva los viernes y no está cifrado; el registro de restauraciones «no se lleva»; el BIA lo elaboró un practicante y nadie lo validó; no existe plan de continuidad; y tres riesgos del registro propio de la organización figuran como «Aceptado» sin documentación."))
add(P("**Justificación de P e I con un dato (verificación 2 del Paso F):**", "Compact", keep=True))
add(TABLE([520, 4415, 4415], ["id", "Dato que justifica la probabilidad", "Dato que justifica el impacto"],
          [(r[0], r[7], r[8]) for r in RIESGOS], sz=14))
add(P("**Evaluación.** Se copió `RG03_evaluacion.py` a `08_riesgos/` y se ejecutó sobre `RG02_registro.csv`. Salida (`evidencias/S15/salidas/RG03_salida.txt`):", "Compact", keep=True))
add(CODE([
 "Riesgos evaluados : 12",
 "Crítico  7   Alto 4   Medio 1   Bajo 0",
 "Categorías SIN riesgo identificado: ninguna",
 "Riesgos ≥ 15 (decisión de la gerencia general): R-02(20) R-01(16) R-04(16)",
 "                                                  R-05(16) R-08(16) R-03(15) R-11(15)",
]))
add(P("Mapa de calor generado (`graficos/RG_mapa_calor.png`, también en el Anexo B):", "Compact", keep=True))
out.extend(frag(IMG("rIdHeat", 4320000, 3780000, "Mapa de calor")))

# Paso C
out.append(head("Paso C", "Paso C — Tratamiento, señal temprana y riesgo residual"))
add(P("**Se buscaba** que todo riesgo de valor > 6 tuviera tratamiento, responsable por cargo, señal temprana, umbral de alerta y un residual calculado. **Archivo:** `08_riesgos/RG04_tratamiento.csv` (13 columnas; aquí se muestran las principales)."))
val = {r[0]: r[5] * r[6] for r in RIESGOS}
trows = []
for i, t in sorted(TRAT.items(), key=lambda kv: -val[kv[0]]):
    dec, acc, resp, plazo, costo, pr, ir, sen, umb, acepta = t
    trows.append((i, val[i], "**%s.** %s" % (dec, acc), "%s · %s" % (resp, plazo), "%d×%d = **%d**" % (pr, ir, pr * ir), "%s — umbral: %s" % (sen, umb), acepta))
add(TABLE([480, 480, 3100, 1500, 800, 1800, 1190],
          ["id", "Valor", "Decisión y acciones", "Responsable · plazo", "Residual", "Señal temprana — umbral", "Acepta el residual"], trows, sz=14))
tot_before = sum(val.values()); tot_after = sum(t[5] * t[6] for t in TRAT.values())
sobre = [i for i, t in TRAT.items() if t[5] * t[6] > 6]
add(P("**Residual.** Se ejecutó `RG05_residual.py` sobre `RG04_tratamiento.csv` (`evidencias/S15/salidas/RG05_salida.txt`): el plan reduce el valor agregado de **%d a %d puntos (%d de reducción, %.0f %%)**. Hay **%d riesgos residuales por encima del criterio** (%s), todos con aceptación a cargo de la Gerencia General, que deben firmarse antes de aprobar el plan (Anexo F). No hay riesgos sin señal temprana." % (tot_before, tot_after, tot_before - tot_after, (tot_before - tot_after) / tot_before * 100, len(sobre), ", ".join(sorted(sobre)))))
add(P("**Registro en SimpleRisk.** **[Pendiente: desplegar los contenedores con los comandos siguientes, configurar la fórmula probabilidad × impacto, las escalas con su definición, el criterio de aceptación y cargar los riesgos de valor ≥ 12 (11 riesgos); adjuntar las capturas en evidencias/S15/.]**", "Compact", keep=True))
add(CODE([
 "docker run -d --name peti_srdb -e MARIADB_ROOT_PASSWORD=peti_sr \\",
 "  -e MARIADB_DATABASE=simplerisk mariadb:11",
 "docker run -d --name peti_simplerisk --link peti_srdb:db \\",
 "  -p 127.0.0.1:8084:80 simplerisk/simplerisk:latest",
]))

# Paso D
out.append(newhead("Paso D — Matriz de comunicación del riesgo"))
add(P("**Se buscaba** comunicar las acciones de tratamiento: qué, a quién, cuándo, por qué canal y con qué decisión. **Archivo:** `08_riesgos/RG06_comunicacion.csv`."))
add(TABLE([700, 1500, 1300, 1050, 950, 1150, 1000, 1700],
          ["id", "Qué se comunica", "A quién (cargo)", "Cuándo", "Canal", "Quién comunica", "Formato", "Decisión que habilita"],
          COMUNICACION, sz=14))
add(P("La última fila es la más importante: la gerencia aprueba el plan conociendo y firmando los riesgos críticos residuales."))

# Paso E
out.append(newhead("Paso E — Redacción de la Sección 8"))
add(P("La Sección 8 del PETI se redacta en el repositorio del equipo con la estructura de la guía. Correspondencia con este informe:"))
add(TABLE([1500, 4000, 3850], ["Subsección", "Contenido", "Dónde está"], [
    ("8.1", "Alcance, contexto y criterios", "Paso A · `RG01_contexto.md`"),
    ("8.2", "Método (ISO 31000:2018) y fuentes", "Paso B"),
    ("8.3 – 8.4", "Registro, evaluación y mapa de calor", "Paso B · `RG02`, `RG03`"),
    ("8.5 – 8.6", "Tratamiento, residual, señales y umbrales", "Paso C · `RG04`, `RG05`"),
    ("8.7", "Matriz de comunicación", "Paso D · `RG06`"),
    ("8.8", "Residuales que requieren aceptación formal", "Paso C y Anexo F"),
    ("8.9", "Seguimiento y revisión", "Trimestral, según `RG01_contexto.md`"),
], sz=17))
add(P("**[Pendiente: redactar la Sección 8 en el PETI del equipo y enlazarla en la tabla de resultados.]**", "Compact"))

# Paso F
out.append(newhead("Paso F — Validar y corregir"))
add(TABLE([3600, 1500, 4250], ["Comprobación", "Resultado", "Evidencia"], [
    ("1. Las nueve categorías tienen al menos un riesgo", "Cumple", "Salida de `RG03_evaluacion.py`: «Categorías SIN riesgo identificado: ninguna»"),
    ("2. P e I justificados con un dato, no por intuición", "Cumple (a validar con la gerencia)", "Tabla de justificación del Paso B"),
    ("3. Todo riesgo de valor alto tiene tratamiento y responsable por cargo", "Cumple", "`RG04_tratamiento.csv`: 12 de 12 riesgos con tratamiento, responsable, señal y umbral"),
], sz=17))
add(P("Lo que quedó pendiente se registra en la sección 3 («Problemas y mejoras»)."))

# Paso G
out.append(newhead("Paso G — Registrar la evidencia y cerrar"))
add(CODE([
 "git add . && git commit -m \"S15: registro de riesgos del plan, tratamiento y comunicacion — seccion 8\"",
 "git tag -a v0.15 -m \"PETI v0.15 — gestion de riesgos\"",
 "git tag -a taller-15 -m \"Taller 15 · SI886\"",
 "git push origin taller-15",
]))
add(P("**URL de la etiqueta `taller-15`:** **[pegar `https://github.com/<organizacion>/<repositorio>/tree/taller-15`]**", "Compact"))

# ---------- 3 ----------
out.append(head("3. Resultados"))
URL = "URL: [pegar]"
add(TABLE([360, 3300, 1200, 4490], ["#", "Resultado esperado", "¿Se logró?", "Evidencia"], [
    (1, "Contexto y criterios con fecha de acuerdo anterior a la evaluación", "Parcial", "`08_riesgos/RG01_contexto.md` + `git log`. Falta la fecha de acuerdo y la URL."),
    (2, "Escalas con definición operativa escrita", "Sí", "Paso A, tablas de probabilidad e impacto. %s" % URL),
    (3, "Las nueve categorías evaluadas", "Sí", "`evidencias/S15/salidas/RG03_salida.txt`. %s" % URL),
    (4, "Registro con ≥ 12 riesgos (evento + causa + consecuencia)", "Sí", "`08_riesgos/RG02_registro.csv` (12 riesgos). %s" % URL),
    (5, "Cada riesgo trazado a los objetivos y proyectos que afecta", "Sí", "Columna «Afecta» de `RG02_registro.csv`. %s" % URL),
    (6, "Mapa de calor generado", "Sí", "`graficos/RG_mapa_calor.png`. %s" % URL),
    (7, "Riesgos ≥ 15 identificados como decisión de la gerencia general", "Sí", "Salida de `RG03_evaluacion.py` (7 riesgos). %s" % URL),
    (8, "Tratamiento para todos los riesgos de valor > 6", "Sí", "`08_riesgos/RG04_tratamiento.csv`. %s" % URL),
    (9, "Riesgo residual calculado, con la reducción lograda", "Sí", "`evidencias/S15/salidas/RG05_salida.txt` (%d → %d puntos)." % (tot_before, tot_after)),
    (10, "Señal temprana y umbral en cada riesgo > 6", "Sí", "Salida de `RG05_residual.py`: 0 riesgos sin señal."),
    (11, "Residuales sobre el criterio con responsable de la aceptación", "Parcial", "Identificado (6 riesgos, Gerencia General); **faltan las firmas** del Anexo F."),
    (12, "Registro cargado en SimpleRisk", "No", "Pendiente: no se desplegó SimpleRisk. Sin capturas."),
    (13, "Matriz de comunicación con las ocho columnas", "Sí", "`08_riesgos/RG06_comunicacion.csv`. %s" % URL),
    (14, "Sección 8 redactada · etiqueta `v0.15`", "No", "Pendiente: redactar la sección y crear la etiqueta."),
], sz=15))
add(P("**Problemas y mejoras.** (a) SimpleRisk no se desplegó: falta instalar Docker y cargar los 11 riesgos de valor ≥ 12; los resultados 12 y 14 quedan como no logrados hasta entonces. (b) La fecha de acuerdo de los criterios (resultado 1) solo se prueba con el historial de Git: los criterios deben confirmarse con la gerencia y subirse al repositorio antes que `RG02_registro.csv`. (c) Las probabilidades e impactos son propuestas del equipo y deben validarse con la gerencia. (d) No se incorporaron los riesgos del pre-mortem de la dinámica de aula. (e) Un resultado sin su URL se califica como no logrado: falta pegar las URL del repositorio.", "Textoindependiente"))

# ---------- 4 ----------
out.append(head("4. Conclusiones"))
add(P("**1.** El contraste entre la política de respaldo y la práctica real produjo los riesgos más graves del registro: la política exige una prueba de restauración trimestral y la organización «asume que el respaldo funciona porque termina sin error». Ese dato, y no la pregunta genérica «¿qué puede salir mal?», llevó al riesgo de mayor valor (R-02, 20 puntos)."))
add(P("**2.** Siete de los doce riesgos alcanzan valor ≥ 15 y requieren decisión de la Gerencia General. El tratamiento propuesto reduce el valor agregado de %d a %d puntos, pero deja seis residuales de 8 puntos que siguen por encima del criterio de aceptación: no se pueden dar por aceptados hasta que el dueño del riesgo los firme." % (tot_before, tot_after)))
add(P("**3.** La organización mantiene tres riesgos «Aceptado» (RG-02, RG-07, RG-09) sin escala escrita, sin apetito de riesgo y sin firma. Fijar primero criterios y escalas, y registrar la señal temprana y el umbral de cada riesgo, es lo que convierte el registro en un instrumento de control y no en un inventario."))

# ---------- 5 ----------
out.append(head("5. Cuestionario"))
add(P("**Pregunta de transferencia: ¿qué riesgo correría una organización real si esto se hiciera mal?**", "FirstParagraph"))
add(P("Una cooperativa que acepta riesgos extremos sin escala, sin firma y sin señal temprana descubre el problema cuando ya ocurrió: en un fallo del core financiero, descubriría que el respaldo nunca se probó y perdería información de socios, además de exponerse a una sanción del regulador. Además, la gerencia aprobaría el plan sin saber qué riesgo queda, y el equipo formulador cargaría con una responsabilidad que no le corresponde.", "Textoindependiente"))

# ---------- 6 ----------
out.append(head("6. Referencias bibliográficas"))
for ref in [
    "ISO. (2018). *ISO 31000:2018 Risk management — Guidelines*. https://www.iso.org/standard/65694.html",
    "ISO/IEC. (2022). *ISO/IEC 27005:2022 Guidance on managing information security risks*. https://www.iso.org/standard/80585.html",
    "IEC. (2019). *IEC 31010:2019 Risk management — Risk assessment techniques*. https://www.iso.org/standard/72140.html",
    "ISACA. (2018). *COBIT 2019 — APO12 Managed Risk y EDM03 Ensured Risk Optimization*. https://www.isaca.org/resources/cobit",
    "Klein, G. (2007). Performing a project premortem. *Harvard Business Review, 85*(9), 18–19.",
    "Superintendencia de Banca, Seguros y AFP. (2021). *Resolución SBS N.º 504-2021*.",
    "SimpleRisk. (s. f.). *Documentation*. https://www.simplerisk.com/documentation",
    "Secretaría de Gobierno Digital. (2018). *Resolución 005-2018-PCM/SEGDI, Anexo I — Lineamientos del Plan de Gobierno Digital*. https://cdn.www.gob.pe/uploads/document/file/356863/Anexo_I_Lineamientos_PGD.pdf",
]:
    add(P(ref.replace("*", ""), "Compact"))

# ---------- 7 ----------
out.append(head("7. Anexos"))
add(P("**Anexo A.** Registro de riesgos: `08_riesgos/RG02_registro.csv` (tabla del Paso B). **Anexo C.** Plan de tratamiento: `RG04_tratamiento.csv` (Paso C). **Anexo D.** Matriz de comunicación: `RG06_comunicacion.csv` (Paso D). **Anexo E.** Pre-mortem: **[pendiente: adjuntar `anexo_E_premortem.pdf` de la dinámica]**."))
add(P("**Anexo B. Mapa de calor de riesgos de ejecución del PETI**", "Compact", keep=True))
out.extend(frag(IMG("rIdHeat", 4320000, 3780000, "Anexo B mapa de calor")))
add(P("**Anexo F. Aceptación del riesgo residual (formato de firmas, sección 9 del PETI)**", "Compact", keep=True))
add(TABLE([700, 3300, 800, 2300, 1100, 1150],
          ["id", "Categoría del riesgo", "Residual", "Responsable de la aceptación", "Firma", "Fecha"],
          [(i, next(r[1] for r in RIESGOS if r[0] == i), t[5] * t[6], t[9], "", "") for i, t in sorted(TRAT.items(), key=lambda kv: -val[kv[0]]) if t[5] * t[6] > 6], sz=15))

for e in frag(""): pass
for e in out: body.insert(len(body) - 1, e)   # antes de sectPr

tree.write(dpath, xml_declaration=True, encoding="UTF-8", standalone=True)

# ---------- imagen + rels ----------
shutil.copy(PNG, UN + r"\word\media\RG_mapa_calor.png")
rp = UN + r"\word\_rels\document.xml.rels"
r = open(rp, encoding="utf8").read()
r = r.replace("</Relationships>", '<Relationship Id="rIdHeat" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/RG_mapa_calor.png"/></Relationships>')
open(rp, "w", encoding="utf8").write(r)

# ---------- actualizar índice al abrir ----------
sp = UN + r"\word\settings.xml"
s = open(sp, encoding="utf8").read()
if "updateFields" not in s:
    for key in ["<w:hdrShapeDefaults", "<w:footnotePr", "<w:endnotePr", "<w:compat"]:
        if key in s:
            s = s.replace(key, '<w:updateFields w:val="true"/>' + key, 1); break
    open(sp, "w", encoding="utf8").write(s)

# ---------- zip ----------
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    # [Content_Types].xml primero
    z.write(UN + r"\[Content_Types].xml", "[Content_Types].xml")
    for root, _, files in os.walk(UN):
        for f in files:
            full = os.path.join(root, f)
            arc = os.path.relpath(full, UN).replace("\\", "/")
            if arc != "[Content_Types].xml":
                z.write(full, arc)
print("OK", OUT)
sys.stdout.flush(); os._exit(0)
