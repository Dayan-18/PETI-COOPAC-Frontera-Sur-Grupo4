import csv, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data import *
out = "08_riesgos"
with open(f"{out}/RG02_registro.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","Categoría","Riesgo (evento + causa + consecuencia)","Objetivos o proyectos afectados","Origen","P","I","Valor","Nivel"])
    for r in filas_registro(): w.writerow(r)
val = {i:p*im for i,_,_,_,_,p,im,_,_ in RIESGOS}
with open(f"{out}/RG04_tratamiento.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","Valor","Decisión","Acciones concretas de tratamiento","Responsable (cargo)","Plazo","Costo","P residual","I residual","Valor residual","Señal temprana","Umbral de alerta","¿Quién acepta el residual?"])
    for i,t in sorted(TRAT.items(), key=lambda kv:-val[kv[0]]):
        dec,acc,resp,plazo,costo,pr,ir,sen,umb,acepta = t
        w.writerow([i,val[i],dec,acc,resp,plazo,costo,pr,ir,pr*ir,sen,umb,acepta])
with open(f"{out}/RG06_comunicacion.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id del riesgo","Qué se comunica","A quién (cargo)","Cuándo / frecuencia","Canal","Quién comunica","Formato","Qué decisión habilita"])
    for r in COMUNICACION: w.writerow(r)
