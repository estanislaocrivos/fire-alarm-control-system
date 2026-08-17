# Requerimientos Funcionales — Sistema Central de Control de Incendio

## 0. Propósito y alcance

Este documento define los requerimientos funcionales del sistema central de
control de incendio (panel), que gestiona sensores de humo, sirenas,
elementos luminosos, botoneras manuales, un display y un teclado como
interfaz de usuario.

Cada requerimiento tiene un identificador único, un enunciado atómico y
verificable ("el sistema deberá..."), una justificación (racional) y una
prioridad según MoSCoW (Must / Should / Could / Won't-for-now).

Referencias de buenas prácticas usadas como guía: NFPA 72 (National Fire
Alarm and Signaling Code), EN 54 (partes 2 y 4), IEC 61508 (functional
safety), ISO/IEC/IEEE 29148 (especificación de requerimientos).

## 0.1 Definiciones y estados del sistema

| Estado               | Descripción                                                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Normal               | Todos los circuitos supervisados en rango nominal, sin eventos activos.                                                                  |
| Alarma               | Al menos un sensor o botonera reporta condición de fuego confirmada.                                                                     |
| Alarma-Silenciada    | Sub-estado de Alarma: la notificación sonora fue silenciada, pero el sistema sigue en Alarma hasta reset.                                |
| Falla ("Trouble")    | Un circuito supervisado (entrada o salida) está fuera de rango nominal (circuito abierto o cortocircuito), sin que haya alarma de fuego. |
| Prueba/Mantenimiento | Modo operativo con autenticación, permite probar dispositivos sin disparar notificación general.                                         |

**EOL**: End-of-Line resistor (resistencia de fin de línea).
**WDT**: Watchdog Timer.
**RTC**: Real-Time Clock.
**MCU**: Microcontrolador.

---

## 1. Supervisión de circuitos de entrada (sensores y botoneras)

- **FR-SEN-001** — El sistema deberá monitorear cada línea de sensor de humo
  mediante lectura analógica de corriente, usando una resistencia de fin de
  línea (EOL) para mantener una corriente de reposo característica.
  *Racional:* distinguir "sin fuego" de "sensor desconectado" (ambos serían
  indistinguibles con una entrada digital simple). *Prioridad:* Must.

- **FR-SEN-002** — El sistema deberá distinguir al menos cuatro estados
  eléctricos por línea de sensor: circuito abierto (falla), corriente de
  reposo (normal), corriente de disparo (alarma).
  *Prioridad:* Must.

- **FR-SEN-003** — El sistema deberá aplicar el mismo principio de
  supervisión (EOL + sensado analógico de corriente) a las botoneras
  manuales ("break the glass"), en lugar de una entrada digital binaria con
  pull-up. *Prioridad:* Must.

- **FR-SEN-004** — Ante la detección de un circuito de entrada en estado de
  falla (abierto o cortocircuito), el sistema deberá generar un evento de
  tipo "Falla" identificando la zona/sensor afectado, sin generar una
  condición de Alarma. *Prioridad:* Must.

---

## 2. Supervisión de circuitos de salida (sirena, luces, rociado)

(TBD, no hay capacidad electrónica para verificar el estado de un actuador)

- **FR-OUT-001** — El sistema deberá supervisar cada línea de salida
  (sirena, luces, rociado) mediante resistencia de fin de línea y sensado
  analógico de corriente, de forma equivalente a las entradas.
  *Racional:* detectar cableado cortado en un actuador en reposo, antes de
  necesitarlo. *Prioridad:* Must.

- **FR-OUT-002** — El sistema deberá distinguir, por línea de salida, entre
  reposo normal, activación, circuito abierto y cortocircuito.
  *Prioridad:* Must.

---

## 3. Confiabilidad del controlador central

- **FR-CTRL-001** — El sistema deberá incorporar un watchdog timer (WDT)
  externo, implementado en un silicio y con un oscilador independientes del
  MCU principal. *Racional:* un WDT interno comparte silicio, clock y
  alimentación con el MCU que debe vigilar, por lo que un fallo de modo
  común (brownout, glitch de reloj, bug de firmware) puede inutilizarlo
  simultáneamente con el MCU. *Prioridad:* Must.

- **FR-CTRL-002** (Roadmap) — El sistema podrá incorporar un segundo
  controlador redundante que monitoree las mismas líneas críticas en
  paralelo, con mecanismo de arbitraje/failover ante discrepancia.
  *Prioridad:* Could (fuera de alcance V1).

---

## 4. Comportamiento seguro ante fallo (fail-safe)

- **FR-SAFE-001** — Ante la pérdida de respuesta del controlador principal
  (detectada por el WDT externo), el sistema deberá forzar las salidas de
  notificación (sirena, luces) a estado activado.
  *Racional:* entre una falsa alarma y no notificar un incendio real, el
  costo de la falsa alarma es menor. *Prioridad:* Must.

- **FR-SAFE-002** — Ante la misma condición de pérdida de respuesta del
  controlador principal, el sistema NO deberá activar automáticamente
  salidas de alto costo/irreversibles (p. ej. rociado de agua).
  *Racional:* el costo económico y el daño irreversible de una activación
  errónea de agua supera el beneficio, dado que ya se garantizó la
  notificación por FR-SAFE-001. *Prioridad:* Must.

---

## 5. Verificación cruzada para acciones irreversibles

- **FR-VER-001** — El sistema deberá requerir confirmación de al menos dos
  sensores distintos dentro de una misma zona antes de activar una salida
  de alto costo/irreversible (rociado de agua), cuando la zona cuente con
  más de un sensor. *Racional:* reduce falsos positivos en la acción más
  costosa del sistema. *Prioridad:* Must.

- **FR-VER-002** — En zonas con un único sensor por diseño (p. ej.
  habitaciones individuales), la confirmación de ese sensor será suficiente
  y la acción de rociado, si corresponde, deberá aplicarse a nivel de zona
  completa. *Prioridad:* Must.

- **FR-VER-003** — La activación de notificación (sirena/luces) no deberá
  requerir verificación cruzada: un único sensor o botonera en condición de
  alarma es suficiente. *Prioridad:* Must.

---

## 6. Alimentación eléctrica

- **FR-PWR-001** — El sistema deberá contar con una fuente de alimentación
  primaria (red) y una fuente secundaria de respaldo a batería, con
  transferencia automática ante pérdida de la primaria.
  *Prioridad:* Must.

- **FR-PWR-002** — El sistema deberá monitorear en forma continua la
  tensión y corriente de carga de la batería de respaldo.
  *Prioridad:* Must.

- **FR-PWR-003** — El sistema deberá ejecutar periódicamente un test de
  descarga de la batería para validar su capacidad real bajo carga, y no
  solo su tensión en reposo. *Racional:* la tensión en reposo no garantiza
  capacidad suficiente en el momento de un corte real. *Prioridad:* Must.

- **FR-PWR-004** — El sistema deberá generar un evento de Falla si la
  batería, su circuito de carga o la fuente primaria están fuera de rango
  nominal. *Prioridad:* Must.

---

## 7. Registro de eventos y trazabilidad

- **FR-LOG-001** — El sistema deberá registrar cada evento (alarma, falla,
  cambio de estado, acción de usuario) con timestamp (fecha y hora), tipo
  de evento, zona y sensor/dispositivo asociado. *Prioridad:* Must.

- **FR-LOG-002** — El registro de eventos deberá persistir en
  almacenamiento no volátil extraíble (tarjeta SD), en un formato legible
  desde una PC. *Prioridad:* Must.

- **FR-LOG-003** — El sistema deberá contar con conectividad de red para el
  envío remoto del registro de eventos, como redundancia ante pérdida o
  destrucción física del panel. *Prioridad:* Should.

- **FR-LOG-004** — El sistema deberá contar con un RTC con alimentación de
  respaldo propia, de forma que el timestamp de los eventos se mantenga
  correcto incluso tras un corte total de alimentación.
  *Prioridad:* Must.

---

## 8. Interfaz de usuario y control de acceso

- **FR-UI-001** — El sistema deberá permitir la activación manual de alarma
  (botón de fuego) sin requerir autenticación. *Racional:* la prioridad de
  vida humana exige que activar la alarma sea de acceso irrestricto.
  *Prioridad:* Must.

- **FR-UI-002** — El sistema deberá requerir autenticación (contraseña o
  código) para: silenciar una alarma activa, resetear el sistema, y entrar
  a modo Prueba/Mantenimiento. *Prioridad:* Must.

- **FR-UI-003** — El sistema deberá permitir la consulta de información
  general de estado (display) sin requerir autenticación.
  *Prioridad:* Must.

- **FR-UI-004** — El display deberá indicar en todo momento el estado
  vigente del sistema (Normal, Alarma, Alarma-Silenciada, Falla,
  Prueba/Mantenimiento), incluso durante el sub-estado Alarma-Silenciada.
  *Prioridad:* Must.

- **FR-UI-005** — El modo Prueba/Mantenimiento deberá permitir accionar y
  verificar dispositivos individualmente sin generar una notificación
  general de alarma. *Prioridad:* Must.

- **FR-UI-006** — El modo Prueba/Mantenimiento deberá soportar un sub-modo
  de "walk test": al activar un sensor o botonera, el sistema deberá dar
  una indicación local breve (no disparar notificación general) y
  registrar en el log qué dispositivo respondió. *Racional:* permite a un
  único técnico verificar todos los dispositivos del edificio sin
  necesidad de evacuar. *Prioridad:* Should.

- **FR-UI-007** — El sistema deberá permitir forzar una notificación
  general de evacuación desde el panel sin requerir autenticación,
  independientemente del estado de los sensores automáticos. *Racional:*
  mismo principio que FR-UI-001 — activar una notificación de emergencia
  debe ser de acceso irrestricto; cubre el caso en que el fuego se detecta
  visualmente antes de que lo haga un sensor. *Prioridad:* Must.

---

## 9. Detección inteligente

- **FR-DET-001** — El sistema deberá soportar sensores con más de un
  criterio de detección (p. ej. humo + temperatura o tasa de aumento de
  temperatura), correlacionando ambas lecturas antes de escalar a
  condición de Alarma. *Racional:* reduce falsos positivos por polvo,
  vapor u otras fuentes no relacionadas a fuego real. *Prioridad:* Should.

- **FR-DET-002** — El sistema deberá monitorear la deriva de sensibilidad
  de cada sensor de humo a lo largo del tiempo (p. ej. por acumulación de
  suciedad en la cámara óptica) y generar un evento de Falla si la
  sensibilidad sale del rango certificado. *Racional:* un sensor sucio
  puede volverse insensible sin que se note hasta que ya es tarde.
  *Prioridad:* Could (depende de si el sensor elegido expone esta info).

---

## 10. Tiempos de respuesta

- **FR-TIME-001** — El sistema deberá activar las salidas de notificación
  (sirena, luces) dentro de un máximo de 1 segundo desde que un sensor o
  botonera cruza el umbral de alarma, en el camino de un solo sensor sin
  verificación cruzada. *Racional:* EN 54-2/NFPA 72 usan ~10 segundos como
  techo de referencia para sistemas grandes con buses de muchos
  dispositivos; en un sistema de este tamaño, con un MCU dedicado, 1
  segundo es holgadamente alcanzable y deja margen de sobra. *Prioridad:*
  Must.

- **FR-TIME-002** — El camino de verificación cruzada (FR-VER-001) no
  deberá tener un límite fijo de latencia, ya que depende de que un
  segundo sensor físico cruce su propio umbral; el sistema deberá evaluar
  la condición del segundo sensor de forma continua, sin introducir
  demoras artificiales de software. *Prioridad:* Must.

---

## 11. Exclusión y bypass de subsistemas y zonas

- **FR-EXC-001** — El sistema deberá permitir excluir (bypass)
  individualmente una zona, sensor, salida o subsistema (p. ej.
  comunicador, extinción automática) sin necesidad de desconectar
  físicamente el cableado. *Prioridad:* Must.

- **FR-EXC-002** — Mientras exista al menos una exclusión activa, el
  sistema deberá mostrar una indicación persistente y visible en el
  display, distinta de los estados Normal/Alarma/Falla. *Racional:* evita
  que una exclusión de mantenimiento quede olvidada. *Prioridad:* Must.

- **FR-EXC-003** — Activar o desactivar una exclusión deberá requerir la
  misma autenticación que silenciar/resetear (FR-UI-002), y deberá
  registrarse en el log de eventos (FR-LOG-001) con identificación del
  usuario y timestamp. *Prioridad:* Must.

- **FR-EXC-004** — Una zona o sensor excluido no deberá poder disparar
  Alarma ni contribuir a la verificación cruzada (FR-VER-001) mientras la
  exclusión esté activa, pero sí deberá seguir siendo supervisado
  eléctricamente y generar un evento de Falla si su circuito se abre o
  cortocircuita. *Racional:* excluir la respuesta automática no debería
  significar dejar de vigilar el cableado. *Prioridad:* Should.

---

## 12. Arquitectura de bus y aislación de fallos (Roadmap)

- **FR-ARCH-001** (Roadmap) — El cableado de bus/lazo de dispositivos podrá
  implementarse en topología Clase A (loop que sale y vuelve al panel), de
  forma que una rotura en un único punto no aísle ningún dispositivo.
  *Prioridad:* Should (evaluar según topología final).

- **FR-ARCH-002** (Roadmap) — El sistema podrá incorporar módulos
  aisladores autónomos por segmento de bus, que desconecten localmente el
  segmento en cortocircuito al superar un umbral de corriente, sin depender
  de una decisión del controlador central. *Racional:* un cortocircuito
  colapsa la tensión de toda la línea compartida y puede degradar la
  comunicación con el controlador central en el mismo instante en que se
  necesitaría su intervención. *Prioridad:* Could (fuera de alcance V1,
  requiere hardware dedicado por punto).

---

## 13. Roadmap / fuera de alcance por esta versión

Ítems identificados durante el análisis, deliberadamente diferidos:

- FR-CTRL-002 — Redundancia de controlador con arbitraje/failover.
- FR-ARCH-001 / FR-ARCH-002 — Topología Clase A y módulos aisladores de bus.
- Autochequeo (POST) al arranque y diagnóstico periódico.
- Comunicación con central de monitoreo externa / contactos secos hacia
  bomberos.
- Seguridad de la conexión de red usada para logging remoto (FR-LOG-003).
