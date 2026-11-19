import fitz,os
d=fitz.open("SI886-S15-TALLER-Grupo4.pdf")
for i,p in enumerate(d):
    p.get_pixmap(dpi=70).save("p%02d.png"%(i+1))
print(len(d)); os._exit(0)
