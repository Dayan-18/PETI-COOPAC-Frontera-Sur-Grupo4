# -*- coding: utf-8 -*-
"""Datos del taller S15 - COOPAC Frontera Sur (empresa 04). Una sola fuente para CSV y Word."""

def nivel(v):
    return "Bajo" if v <= 6 else "Medio" if v <= 11 else "Alto" if v <= 14 else "Crítico"

# id, categoria, riesgo, afecta, origen, P, I, dato que justifica P, dato que justifica I
RIESGOS = [
 ("R-01","Personal clave",
  "Que el Jefe de TI, único custodio de la copia fuera de las instalaciones (lleva un disco los viernes), se ausente o deje el cargo, dejando a la cooperativa sin copia externa vigente y sin quien ejecute la restauración.",
  "Continuidad de todos los procesos (BIA01–BIA06)","Política de respaldo §6",4,4,
  "La custodia depende de una sola persona y de un solo día de la semana, y el disco no está cifrado.",
  "La copia externa es única: se perdería hasta una semana de información."),
 ("R-02","Técnico",
  "Que un respaldo que nunca se ha restaurado resulte inservible cuando se necesite, porque se asume correcto solo porque termina sin error, y se pierda información del core financiero.",
  "BIA01, BIA03, BIA06 (core financiero)","Política §6 · BIA (última prueba «Nunca»)",4,5,
  "La prueba trimestral del punto 3.4 no se ha hecho nunca; 3 de los 6 procesos del BIA figuran con última prueba «Nunca».",
  "El BIA06 (cierre contable y reportes a la SBS) tiene RPO de 1 h e impacto a 24 h «Alto»."),
 ("R-03","Normativo",
  "Que la SBS verifique el incumplimiento de la Resolución SBS 504-2021 y sancione a la cooperativa porque no existe plan de continuidad ni pruebas documentadas.",
  "Cierre contable y reportes a la SBS · todos los procesos","Registro RG-01, RG-03 · Política §6",3,5,
  "El regulador exige revisiones que no están calendarizadas y la organización califica el riesgo como «Bajo» sin escala escrita.",
  "Una sanción afecta la autorización de operación de la COOPAC y la confianza de los socios."),
 ("R-04","Normativo",
  "Que ocurra una fuga o acceso indebido a datos personales de socios y no pueda reconstruirse quién accedió porque no hay registro de accesos de lectura, exponiendo a la cooperativa a sanción y a pérdida de confianza.",
  "UA-07, UA-11, UA-17","Registro RG-02 (Extremo, «Aceptado»), RG-07",4,4,
  "RG-02 está calificado «Alta» por la propia organización y la protección de datos (UA-17) nunca se ha auditado.",
  "Los datos de socios son el activo central de una cooperativa de ahorro y crédito."),
 ("R-05","Proveedor",
  "Que el proveedor de nube, del que depende el respaldo cifrado, falle o cambie sus condiciones sin que la cooperativa pueda verificar el cifrado ni exigir la recuperación, dejando respaldo y sistemas sin garantía.",
  "UA-16, UA-13 · todos los procesos","Registro RG-08 · Política §6 (cifrado «según el proveedor»)",4,4,
  "RG-08 está en probabilidad «Alta»; el proveedor de nube (UA-16) nunca ha sido auditado.",
  "El cifrado y la recuperación se aceptan solo por la palabra del proveedor."),
 ("R-06","Capacidad de ejecución",
  "Que TI y Auditoría Interna no puedan sostener el plan (BIA, pruebas de restauración, continuidad) junto con la operación, porque auditoría dispone de 310 horas-auditor al año para 17 entidades auditables y esa carga nunca se ha calculado.",
  "Toda la hoja de ruta","Universo auditable §2 y §4",4,3,
  "17 entidades auditables y 310 horas al año: ninguna se auditó de forma sistemática.",
  "El retraso demora controles, pero no detiene la operación por sí solo."),
 ("R-07","Presupuestal",
  "Que no se asigne presupuesto para respaldo externo cifrado, sitio alterno y pruebas de continuidad porque la Gerencia aprueba los tratamientos solo «cuando se le presentan», y los controles queden sin recursos.",
  "Proyectos de respaldo y continuidad","Universo auditable §4 · Política §4",3,4,
  "La organización no tiene apetito de riesgo ni proceso de aprobación definido.",
  "Sin recursos, los riesgos R-01, R-02 y R-11 no pueden tratarse."),
 ("R-08","Patrocinio",
  "Que el plan no tenga patrocinador activo ni apetito de riesgo definido y la Gerencia siga aceptando riesgos sin firma ni análisis (RG-02, RG-07 y RG-09 figuran como «Aceptado»), dejando al plan sin autoridad para exigir controles.",
  "Todos","Universo auditable §3 y §4",4,4,
  "Tres riesgos están «Aceptado» sin documentación y no existe apetito de riesgo.",
  "Sin patrocinio, ningún otro tratamiento se sostiene."),
 ("R-09","Resistencia al cambio",
  "Que usuarios y jefes de área no adopten los procedimientos de respaldo, el registro de restauraciones y la validación del BIA porque la política se difundió solo «por correo» y nunca se revisó, y el plan quede en papel.",
  "Respaldo · BIA · todos los procesos","Política de respaldo (ficha)",4,3,
  "La política (POL-TI-011) venció su revisión en noviembre de 2024 y no se revisó; el registro de restauraciones «no se lleva».",
  "El efecto es de adopción parcial, corregible con capacitación y seguimiento."),
 ("R-10","De alcance",
  "Que el alcance de la continuidad se defina sobre un BIA elaborado por un practicante y no validado (p. ej. BIA02: criticidad «Alta» con RTO de 72 h e impacto a 24 h «Bajo»; BIA01: RTO de 2 h con RPO de 26 h), obligando a rehacer metas y proyectos durante la ejecución.",
  "BIA01–BIA06 · proyectos de continuidad","BIA (incoherencias) · Política §6",4,3,
  "El BIA es el único existente, no fue revisado y varias filas son incoherentes entre sí.",
  "Obliga a rehacer metas, pero se detecta antes de ejecutar si se revalida."),
 ("R-11","Técnico",
  "Que el core financiero sufra una interrupción prolongada sin plan de continuidad, deteniendo la captación, la cobranza y el cierre contable con sus reportes a la SBS.",
  "UA-07 · BIA01, BIA03, BIA06","Registro RG-04 («Sin definir») · Política §6 («No» hay plan)",3,5,
  "La propia organización califica RG-04 como probabilidad «Media» y no tiene tratamiento definido.",
  "Tres procesos dependen del core financiero y no existe plan de continuidad."),
 ("R-12","Presupuestal",
  "Que el gasto operativo recurrente de los controles (nube, cifrado, pruebas, sitio alterno) supere la capacidad presupuestal de los años 2 y 3 y obligue a abandonar controles ya implementados.",
  "Proyectos de respaldo y continuidad","Curva de OPEX del PETI (sección 7.4)",3,3,
  "Los controles generan costos recurrentes que hoy no están presupuestados.",
  "Se puede reducir el alcance de un control sin dejar de operar."),
]

# id: decision, acciones, responsable, plazo, costo, Pres, Ires, senal, umbral, acepta
TRAT = {
 "R-02":("Mitigar","Ejecutar la prueba de restauración trimestral sobre el core financiero con acta y registro de restauraciones; verificación diaria del respaldo con comprobación de integridad.","Jefe de TI","30 días","Bajo",2,4,"Trimestre sin acta de restauración","1 trimestre sin acta","Gerencia General"),
 "R-01":("Mitigar","Cifrar el disco, designar un custodio suplente, mantener una segunda copia en nube cifrada y llevar registro de entrega de cada viernes.","Jefe de TI","60 días","Bajo",2,3,"Viernes sin entrega registrada del disco","2 viernes seguidos","Gerencia de Administración y Finanzas"),
 "R-03":("Mitigar","Aprobar un plan de continuidad del negocio con pruebas anuales documentadas y calendarizar las revisiones que exige el regulador; matriz de cumplimiento de la Resolución SBS 504-2021.","Jefe de TI y Gerencia de Administración y Finanzas","6 meses","Medio",2,4,"Revisión exigida por el regulador sin fecha en el calendario","1 requisito sin fecha","Gerencia General"),
 "R-04":("Mitigar","Activar el registro de accesos de lectura en el core financiero y en la gestión documental; revisión mensual de accesos; auditar la protección de datos personales (UA-17).","Responsable de protección de datos y Jefe de TI","90 días","Medio",2,4,"Sistema con datos de socios sin registro de accesos activo","Cualquier sistema sin registro","Gerencia General"),
 "R-05":("Transferir + Mitigar","Incluir en el contrato cláusulas de nivel de servicio, derecho de auditoría y evidencia de cifrado; probar la restauración desde la nube; documentar un plan de salida del proveedor.","Gerencia de Administración y Finanzas","90 días","Medio",2,4,"Proveedor sin evidencia de cifrado ni informe de servicio","60 días sin evidencia","Gerencia General"),
 "R-06":("Mitigar","Calcular las horas-auditor por entidad, priorizar el universo por riesgo (≥ 15 primero) y programar las revisiones exigidas por el regulador dentro de las 310 horas.","Jefe de Auditoría Interna y Jefe de TI","60 días","Bajo",2,3,"Horas ejecutadas por debajo de lo programado a mitad de trimestre","Desviación > 20 %","Gerencia General"),
 "R-07":("Mitigar","Aprobación plurianual del presupuesto de continuidad por acta, con un escenario reducido que prioriza respaldo y pruebas de restauración.","Gerencia de Administración y Finanzas","Al aprobar el plan","Bajo",2,3,"Presupuesto de TI sin aprobar en la fecha habitual","30 días de retraso","Gerencia General"),
 "R-08":("Mitigar","Designar por resolución al responsable del plan, constituir el comité de TI como órgano de seguimiento, definir por escrito el apetito de riesgo y exigir firma para todo residual > 6.","Gerencia General","Al aprobar el plan","Bajo",2,4,"Comité de TI sin sesionar","1 trimestre sin acta","Gerencia General"),
 "R-09":("Mitigar","Difusión formal de la política con firma de recibido, capacitación a jefes de agencia e indicador de cumplimiento del registro de restauraciones por agencia.","Jefe de TI y Gerencia de Administración y Finanzas","90 días","Bajo",2,3,"Agencia sin registro de cumplimiento","1 agencia durante 2 meses","Gerencia de Administración y Finanzas"),
 "R-10":("Mitigar","Revalidar el BIA con los dueños de proceso, aprobarlo formalmente y actualizarlo cada año; corregir las filas incoherentes antes de fijar metas de recuperación.","Jefe de TI y jefes de proceso","45 días","Bajo",2,3,"BIA sin aprobación formal","45 días sin aprobar","Gerencia de Administración y Finanzas"),
 "R-11":("Mitigar + Contingencia","Elaborar el plan de recuperación del core financiero, definir un sitio o proveedor alterno y ejecutar un simulacro con medición del tiempo de recuperación.","Jefe de TI","6 meses","Alto",2,4,"Simulacro que supera el RTO acordado","Cualquier simulacro fuera del RTO","Gerencia General"),
 "R-12":("Mitigar","Revisión semestral del gasto operativo recurrente contra el presupuesto; priorizar controles por valor de riesgo reducido.","Gerencia de Administración y Finanzas","Continuo","Bajo",2,3,"Gasto de TI por encima de lo presupuestado","Desviación > 10 %","Gerencia de Administración y Finanzas"),
}

# id, que, a quien, cuando, canal, quien comunica, formato, decision
COMUNICACION = [
 ("R-08","Estado del plan y de los indicadores de riesgo","Gerencia General y comité de TI","Trimestral","Sesión de comité","Responsable del plan","Tablero + acta","Continuar, ajustar o detener el plan"),
 ("R-02","Resultado de la prueba de restauración y de la verificación diaria","Gerencia General y Gerencia de Administración y Finanzas","Trimestral; inmediata si la prueba falla","Informe escrito","Jefe de TI","Acta de restauración","Corregir el respaldo o invertir en otra solución"),
 ("R-01","Estado de la custodia de la copia externa y del suplente","Gerencia de Administración y Finanzas","Mensual","Correo con tablero","Jefe de TI","Indicador","Priorizar la segunda copia en nube"),
 ("R-04","Cobertura del registro de accesos y hallazgos de la revisión","Gerencia General y responsable de protección de datos","Mensual","Reunión de seguimiento","Jefe de TI","Informe de 1 página","Escalar o sancionar incumplimientos"),
 ("R-05","Evidencia de cifrado y estado de la renegociación del contrato","Gerencia General","Quincenal hasta la firma","Correo","Gerencia de Administración y Finanzas","Estado en una línea","Escalar o activar el plan de salida"),
 ("R-03","Calendario de revisiones del regulador y cumplimiento","Gerencia General","Trimestral","Sesión de comité","Jefe de Auditoría Interna","Matriz de cumplimiento","Asignar horas y recursos"),
 ("R-11","Resultado del simulacro de recuperación del core financiero","Comité de TI","Al concluir cada simulacro","Sesión de comité","Jefe de TI","Informe técnico","Aprobar el plan de recuperación o ajustarlo"),
 ("Todos ≥ 15","Riesgo, tratamiento, residual y responsable de la aceptación","Gerencia General","Antes de aprobar el plan","Sesión formal","Responsable del plan","Anexo del PETI con firmas","Aprobar el plan con conocimiento del riesgo"),
]

def filas_registro():
    return [(i,c,r,a,o,p,im,p*im,nivel(p*im)) for i,c,r,a,o,p,im,_,_ in RIESGOS]

ESCALA_P = [
 (1,"Muy baja","No se espera que ocurra en el horizonte de 3 años (< 5 %)"),
 (2,"Baja","Puede ocurrir una vez en el horizonte del plan (5–20 %)"),
 (3,"Media","Es probable que ocurra al menos una vez en el horizonte (20–50 %)"),
 (4,"Alta","Ya hay señales o antecedentes en la organización (50–80 %)"),
 (5,"Muy alta","Está ocurriendo o ocurrirá casi con certeza (> 80 %)"),
]
ESCALA_I = [
 (1,"Insignificante","Se absorbe en la operación diaria sin retraso en la hoja de ruta"),
 (2,"Menor","Retrasa un proyecto menos de 1 mes, sin costo adicional relevante"),
 (3,"Moderado","Retrasa un proyecto de 1 a 3 meses o exige reasignar recursos"),
 (4,"Mayor","Compromete un objetivo del plan, o detiene un proceso de negocio por más de 24 h"),
 (5,"Catastrófico","Impide cumplir el plan o genera sanción regulatoria o pérdida de información de socios"),
]
