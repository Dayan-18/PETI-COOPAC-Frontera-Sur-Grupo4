# Sección 8. Gestión de riesgos del plan — COOPAC Frontera Sur

> Clasificación: **Confidencial**. Los riesgos de personas se redactan por cargo.

## 8.1 Alcance, contexto y criterios
Esta sección gestiona los riesgos que amenazan la **ejecución del PETI Año 1 – Año 3**. Excluye los riesgos operativos de TI del portafolio y los riesgos de negocio (PEI). Las escalas de probabilidad e impacto (1 a 5, con definición operativa) y el criterio de aceptación están en [`RG01_contexto.md`](RG01_contexto.md), fijados antes de evaluar (commit `d9a9c80`, 19/11/2026). Criterio: ≤ 6 aceptable con documentación · 7–14 tratamiento con plazo · ≥ 15 decisión de la gerencia general antes de aprobar el plan.

## 8.2 Método
ISO 31000:2018. Fuentes de identificación: política de respaldo (POL-TI-011), BIA, universo auditable y registro de riesgos de la organización, y el contraste entre lo declarado y la práctica real.

## 8.3 Registro de riesgos

| id | Categoría | Riesgo | P | I | Valor | Nivel |
|---|---|---|---|---|---|---|
| R-01 | Personal clave | Que el Jefe de TI, único custodio de la copia fuera de las instalaciones (lleva un disco los viernes), se ausente o deje el cargo, dejando a la cooperativa sin copia externa vigente y sin quien ejecute la restauración. | 4 | 4 | **16** | Crítico |
| R-02 | Técnico | Que un respaldo que nunca se ha restaurado resulte inservible cuando se necesite, porque se asume correcto solo porque termina sin error, y se pierda información del core financiero. | 4 | 5 | **20** | Crítico |
| R-03 | Normativo | Que la SBS verifique el incumplimiento de la Resolución SBS 504-2021 y sancione a la cooperativa porque no existe plan de continuidad ni pruebas documentadas. | 3 | 5 | **15** | Crítico |
| R-04 | Normativo | Que ocurra una fuga o acceso indebido a datos personales de socios y no pueda reconstruirse quién accedió porque no hay registro de accesos de lectura, exponiendo a la cooperativa a sanción y a pérdida de confianza. | 4 | 4 | **16** | Crítico |
| R-05 | Proveedor | Que el proveedor de nube, del que depende el respaldo cifrado, falle o cambie sus condiciones sin que la cooperativa pueda verificar el cifrado ni exigir la recuperación, dejando respaldo y sistemas sin garantía. | 4 | 4 | **16** | Crítico |
| R-06 | Capacidad de ejecución | Que TI y Auditoría Interna no puedan sostener el plan (BIA, pruebas de restauración, continuidad) junto con la operación, porque auditoría dispone de 310 horas-auditor al año para 17 entidades auditables y esa carga nunca se ha calculado. | 4 | 3 | **12** | Alto |
| R-07 | Presupuestal | Que no se asigne presupuesto para respaldo externo cifrado, sitio alterno y pruebas de continuidad porque la Gerencia aprueba los tratamientos solo «cuando se le presentan», y los controles queden sin recursos. | 3 | 4 | **12** | Alto |
| R-08 | Patrocinio | Que el plan no tenga patrocinador activo ni apetito de riesgo definido y la Gerencia siga aceptando riesgos sin firma ni análisis (RG-02, RG-07 y RG-09 figuran como «Aceptado»), dejando al plan sin autoridad para exigir controles. | 4 | 4 | **16** | Crítico |
| R-09 | Resistencia al cambio | Que usuarios y jefes de área no adopten los procedimientos de respaldo, el registro de restauraciones y la validación del BIA porque la política se difundió solo «por correo» y nunca se revisó, y el plan quede en papel. | 4 | 3 | **12** | Alto |
| R-10 | De alcance | Que el alcance de la continuidad se defina sobre un BIA elaborado por un practicante y no validado (p. ej. BIA02: criticidad «Alta» con RTO de 72 h e impacto a 24 h «Bajo»; BIA01: RTO de 2 h con RPO de 26 h), obligando a rehacer metas y proyectos durante la ejecución. | 4 | 3 | **12** | Alto |
| R-11 | Técnico | Que el core financiero sufra una interrupción prolongada sin plan de continuidad, deteniendo la captación, la cobranza y el cierre contable con sus reportes a la SBS. | 3 | 5 | **15** | Crítico |
| R-12 | Presupuestal | Que el gasto operativo recurrente de los controles (nube, cifrado, pruebas, sitio alterno) supere la capacidad presupuestal de los años 2 y 3 y obligue a abandonar controles ya implementados. | 3 | 3 | **9** | Medio |

Las nueve categorías (presupuestal, patrocinio, capacidad de ejecución, personal clave, resistencia al cambio, proveedor, técnico, normativo y de alcance) tienen al menos un riesgo. No hay categorías omitidas.

## 8.4 Evaluación y mapa de calor
Distribución: 7 críticos, 4 altos, 1 medio, 0 bajos. Mapa de calor: [`../graficos/RG_mapa_calor.png`](../graficos/RG_mapa_calor.png).

Riesgos ≥ 15 que requieren decisión de la gerencia general: R-02 (20), R-01 (16), R-04 (16), R-05 (16), R-08 (16), R-03 (15), R-11 (15).

## 8.5 Tratamiento y riesgo residual

| id | Valor | Decisión | Acciones | Responsable · plazo | Residual |
|---|---|---|---|---|---|
| R-02 | 20 | Mitigar | Ejecutar la prueba de restauración trimestral sobre el core financiero con acta y registro de restauraciones; verificación diaria del respaldo con comprobación de integridad. | Jefe de TI · 30 días | 2×4 = **8** |
| R-01 | 16 | Mitigar | Cifrar el disco, designar un custodio suplente, mantener una segunda copia en nube cifrada y llevar registro de entrega de cada viernes. | Jefe de TI · 60 días | 2×3 = **6** |
| R-04 | 16 | Mitigar | Activar el registro de accesos de lectura en el core financiero y en la gestión documental; revisión mensual de accesos; auditar la protección de datos personales (UA-17). | Responsable de protección de datos y Jefe de TI · 90 días | 2×4 = **8** |
| R-05 | 16 | Transferir + Mitigar | Incluir en el contrato cláusulas de nivel de servicio, derecho de auditoría y evidencia de cifrado; probar la restauración desde la nube; documentar un plan de salida del proveedor. | Gerencia de Administración y Finanzas · 90 días | 2×4 = **8** |
| R-08 | 16 | Mitigar | Designar por resolución al responsable del plan, constituir el comité de TI como órgano de seguimiento, definir por escrito el apetito de riesgo y exigir firma para todo residual > 6. | Gerencia General · Al aprobar el plan | 2×4 = **8** |
| R-03 | 15 | Mitigar | Aprobar un plan de continuidad del negocio con pruebas anuales documentadas y calendarizar las revisiones que exige el regulador; matriz de cumplimiento de la Resolución SBS 504-2021. | Jefe de TI y Gerencia de Administración y Finanzas · 6 meses | 2×4 = **8** |
| R-11 | 15 | Mitigar + Contingencia | Elaborar el plan de recuperación del core financiero, definir un sitio o proveedor alterno y ejecutar un simulacro con medición del tiempo de recuperación. | Jefe de TI · 6 meses | 2×4 = **8** |
| R-06 | 12 | Mitigar | Calcular las horas-auditor por entidad, priorizar el universo por riesgo (≥ 15 primero) y programar las revisiones exigidas por el regulador dentro de las 310 horas. | Jefe de Auditoría Interna y Jefe de TI · 60 días | 2×3 = **6** |
| R-07 | 12 | Mitigar | Aprobación plurianual del presupuesto de continuidad por acta, con un escenario reducido que prioriza respaldo y pruebas de restauración. | Gerencia de Administración y Finanzas · Al aprobar el plan | 2×3 = **6** |
| R-09 | 12 | Mitigar | Difusión formal de la política con firma de recibido, capacitación a jefes de agencia e indicador de cumplimiento del registro de restauraciones por agencia. | Jefe de TI y Gerencia de Administración y Finanzas · 90 días | 2×3 = **6** |
| R-10 | 12 | Mitigar | Revalidar el BIA con los dueños de proceso, aprobarlo formalmente y actualizarlo cada año; corregir las filas incoherentes antes de fijar metas de recuperación. | Jefe de TI y jefes de proceso · 45 días | 2×3 = **6** |
| R-12 | 9 | Mitigar | Revisión semestral del gasto operativo recurrente contra el presupuesto; priorizar controles por valor de riesgo reducido. | Gerencia de Administración y Finanzas · Continuo | 2×3 = **6** |

Reducción total lograda por el plan de tratamiento: **171 → 84 puntos (51%)**.

## 8.6 Señales tempranas y umbrales de alerta

| id | Señal temprana | Umbral de alerta |
|---|---|---|
| R-02 | Trimestre sin acta de restauración | 1 trimestre sin acta |
| R-01 | Viernes sin entrega registrada del disco | 2 viernes seguidos |
| R-04 | Sistema con datos de socios sin registro de accesos activo | Cualquier sistema sin registro |
| R-05 | Proveedor sin evidencia de cifrado ni informe de servicio | 60 días sin evidencia |
| R-08 | Comité de TI sin sesionar | 1 trimestre sin acta |
| R-03 | Revisión exigida por el regulador sin fecha en el calendario | 1 requisito sin fecha |
| R-11 | Simulacro que supera el RTO acordado | Cualquier simulacro fuera del RTO |
| R-06 | Horas ejecutadas por debajo de lo programado a mitad de trimestre | Desviación > 20 % |
| R-07 | Presupuesto de TI sin aprobar en la fecha habitual | 30 días de retraso |
| R-09 | Agencia sin registro de cumplimiento | 1 agencia durante 2 meses |
| R-10 | BIA sin aprobación formal | 45 días sin aprobar |
| R-12 | Gasto de TI por encima de lo presupuestado | Desviación > 10 % |

## 8.7 Matriz de comunicación del riesgo
Ver [`RG06_comunicacion.csv`](RG06_comunicacion.csv) (ocho columnas). La última fila es la más importante: la gerencia aprueba el plan conociendo y firmando los riesgos críticos residuales.

## 8.8 Riesgos residuales que requieren aceptación formal

| id | Residual | Responsable de la aceptación |
|---|---|---|
| R-02 | 8 | Gerencia General |
| R-04 | 8 | Gerencia General |
| R-05 | 8 | Gerencia General |
| R-08 | 8 | Gerencia General |
| R-03 | 8 | Gerencia General |
| R-11 | 8 | Gerencia General |

Anexo de firmas en la sección 9 del PETI. Un residual sin firma del dueño del riesgo no está aceptado: está ignorado.

## 8.9 Seguimiento y revisión
Revisión trimestral por el comité de TI y ante cualquier hito de decisión de la hoja de ruta. Responsable: Gerencia General (responsable del plan). Disparadores de revisión extraordinaria: cualquier umbral de alerta de 8.6, un incidente que afecte el core financiero, o una nueva exigencia del regulador.
