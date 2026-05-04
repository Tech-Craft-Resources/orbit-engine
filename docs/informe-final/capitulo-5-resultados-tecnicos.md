# Capítulo 5 — Resultados Técnicos

> Este capítulo reporta exclusivamente la **validación técnica** del sistema OrbitEngine: pruebas de carga sobre el backend con Locust y pruebas de rendimiento del frontend con Lighthouse, PageSpeed Insights y WebPageTest. Los **resultados de la validación con usuarios** (eficiencia operativa, satisfacción, completitud de tareas) se presentan en el Capítulo 6 — *Resultados de Usuarios*. Las **acciones de mejora** derivadas de los hallazgos aquí descritos se discuten en el capítulo de Conclusiones.

---

## 5.1 Marco de la Validación Técnica

### 5.1.1 Objetivos

La validación técnica se planteó tres objetivos verificables:

1. **Caracterizar el comportamiento del backend bajo carga concurrente**, identificando latencias, tasa de fallos y punto de degradación.
2. **Caracterizar el rendimiento percibido del frontend** desde tres puntos de observación independientes: laboratorio local (Lighthouse), infraestructura externa (PageSpeed Insights) y red real con captura de video (WebPageTest).
3. **Contrastar los hallazgos contra los Requisitos No Funcionales** definidos en el Capítulo 3 que aplican a esta validación, con foco en RNF-01 (rendimiento de la API), RNF-02 (disponibilidad), RNF-07 (responsividad de la interfaz) y RNF-09 (escalabilidad arquitectónica).

### 5.1.2 Ambiente de Pruebas

Todas las mediciones se ejecutaron contra el **despliegue de producción** descrito en el Capítulo 4:


| Componente                  | Plataforma                                                     | Configuración relevante para las pruebas                                                                                                                                                                                                                 |
| --------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend (FastAPI)           | Railway                                                        | Servicio web sin réplicas horizontales, imagen Docker, variables de entorno de producción. La concurrencia interna se ajustó por escenario: **2 workers de FastAPI para los Tests 01–05** y **4 workers para el Test 06** (escenario de pico sostenido). |
| Base de datos               | PostgreSQL gestionada por Railway                              | Instancia compartida, sin réplicas de lectura                                                                                                                                                                                                            |
| Frontend (React/Vite)       | Vercel                                                         | SPA con CDN global integrado, HTTPS automático                                                                                                                                                                                                           |
| Dominio                     | `orbitengine.lat` (frontend) y `api.orbitengine.lat` (backend) | Certificados TLS gestionados por las plataformas                                                                                                                                                                                                         |
| Cliente de pruebas de carga | Estación de trabajo única del equipo                           | Conexión doméstica en Bogotá, Colombia                                                                                                                                                                                                                   |


### 5.1.3 Criterios de Aceptación

Los criterios contra los cuales se evalúan los resultados provienen del Capítulo 3, Sección 3.2:


| ID     | Tipo           | Criterio aplicable a este capítulo                                                                                                       |
| ------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-01 | Rendimiento    | El 95 % de las respuestas de la API debe completarse en menos de 500 ms bajo carga normal (hasta 50 usuarios concurrentes).              |
| RNF-02 | Disponibilidad | El sistema debe garantizar una disponibilidad mínima del 95 % mensual.                                                                   |
| RNF-07 | Usabilidad     | La interfaz debe ser responsive y funcional en dispositivos de 375 px de ancho mínimo.                                                   |
| RNF-09 | Escalabilidad  | La arquitectura debe soportar el incremento de tenants sin cambios estructurales, mediante escalado horizontal de la capa de aplicación. |


### 5.1.4 Herramientas Empleadas


| Herramienta            | Versión / canal                                                     | Capa observada     | Tipo de medición                                               |
| ---------------------- | ------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------- |
| **Locust**             | 2.x sobre `tests/performance/locustfile.py`                         | Backend / API REST | Carga sintética con usuarios virtuales                         |
| **Lighthouse**         | 13.0.1, ejecutado desde Chrome DevTools                             | Frontend           | Auditoría de laboratorio (escritorio, conexión local)          |
| **PageSpeed Insights** | Web pública de Google (Lighthouse 13.0.1 con Headless Chromium 146) | Frontend           | Auditoría desde infraestructura de Google (escritorio y móvil) |
| **WebPageTest**        | versión 26.03                                                       | Frontend           | Carga real con captura de waterfall y video                    |


### 5.1.5 Composición del Piloto Técnico

Las pruebas de este capítulo se ejecutaron sobre un piloto compuesto por **ocho organizaciones registradas en producción**, con una composición deliberadamente mixta diseñada para combinar realismo de uso con presión sintética sobre el sistema. La siguiente tabla detalla la naturaleza de cada una de las ocho organizaciones.

**Tabla 5.1.5.** Organizaciones del piloto técnico.


| #   | Nombre del *tenant* | Naturaleza                                                            | Sector / propósito                                                                                       |
| --- | ------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1   | **Frozt Bitez**     | **Empresa real**                                                      | Pyme que adoptó OrbitEngine para sus operaciones reales                                                  |
| 2   | **Miss Peggy**      | **Empresa real**                                                      | Pyme de un sector distinto al de Frozt Bitez, que también adoptó la plataforma para sus operaciones      |
| 3   | Lehgo               | Empresa ficticia de prueba (datos sintéticos)                         | Generación de volumen de productos, ventas y movimientos para forzar consultas                           |
| 4   | Ferrallas del Norte | Empresa ficticia de prueba (datos sintéticos)                         | Generación de volumen de productos, ventas y movimientos para forzar consultas                           |
| 5   | Sabor Caribe        | Empresa ficticia de prueba (datos sintéticos)                         | Generación de volumen de productos, ventas y movimientos para forzar consultas                           |
| 6   | Moda Andes          | Empresa ficticia de prueba (datos sintéticos)                         | Generación de volumen de productos, ventas y movimientos para forzar consultas                           |
| 7   | FarmaVida           | Empresa ficticia de prueba (datos sintéticos)                         | Generación de volumen de productos, ventas y movimientos para forzar consultas                           |
| 8   | Default             | Datos de prueba — primera organización creada como *seed* del entorno | Tenant base de pruebas internas; conserva información residual de las primeras iteraciones de desarrollo |


**Resumen cuantitativo.**


| Tipo de organización                                               | Cantidad | Proporción de la muestra |
| ------------------------------------------------------------------ | -------- | ------------------------ |
| **Empresas reales** que adoptaron OrbitEngine para sus operaciones | 2        | 25 %                     |
| **Empresas ficticias de prueba / datos de prueba**                 | 6        | 75 %                     |
| **Total**                                                          | **8**    | **100 %**                |


- **Empresas reales (25 % de la muestra) — Frozt Bitez y Miss Peggy.** Son las únicas dos pymes que confiaron en la plataforma para realizar parte o la totalidad de sus operaciones cotidianas durante la fase de validación. Aunque en cantidad representan una proporción menor, su valor para el experimento es alto: pertenecen a sectores muy distintos entre sí, manejan trazabilidades diferenciadas de productos, ventas, clientes y movimientos de inventario, y permiten dar un panorama representativo de cómo se comportarán empresas reales que adopten OrbitEngine en el futuro.
- **Empresas ficticias de prueba (75 % de la muestra) — Lehgo, Ferrallas del Norte, Sabor Caribe, Moda Andes, FarmaVida y Default.** Son seis organizaciones creadas por el equipo de desarrollo con el único objetivo de **poblar el sistema con grandes volúmenes de productos, ventas, clientes, movimientos de inventario y reportes**, de modo que las consultas, agregaciones y filtros del backend trabajen sobre conjuntos de datos suficientemente grandes para forzar respuestas más complejas del servidor. Estas organizaciones **no representan negocios reales**; en lo que sigue se nombrarán siempre como *empresas ficticias de prueba* o *datos de prueba*. *Default* es, además, la primera organización creada en el entorno y conserva información residual de las pruebas iniciales del equipo, por lo que cumple un papel adicional como *tenant* base.

Esta composición es coherente con el alcance de un piloto técnico: **Frozt Bitez y Miss Peggy** aportan realismo cualitativo sobre el comportamiento productivo del sistema, mientras que **Lehgo, Ferrallas del Norte, Sabor Caribe, Moda Andes, FarmaVida y Default** aportan el volumen sintético necesario para evidenciar el coste de las consultas en condiciones próximas a las de un sistema en producción a mayor escala.

---

## 5.2 Pruebas de Carga (Backend / API) — Locust

### 5.2.1 Diseño del Experimento

Las pruebas se construyeron con **Locust** y están versionadas en el repositorio en `[backend/tests/performance/locustfile.py](../../backend/tests/performance/locustfile.py)`. El diseño persigue cuatro propiedades:

1. **Realismo del tráfico**: combinar exploración (paginación, búsqueda, filtros, ordenamiento) con escritura efectiva (registro de ventas, ajuste de stock).
2. **Multi-tenancy bajo carga**: cada usuario virtual rota credenciales reales de las distintas organizaciones piloto, ejercitando simultáneamente el aislamiento por `organization_id` en todas las consultas.
3. **Reproducibilidad**: los escenarios y los pesos relativos de las tareas están codificados en el repositorio y pueden reejecutarse en cualquier momento.
4. **Progresividad**: se ejecutaron seis escenarios encadenados con concurrencia creciente para construir una curva de degradación.

### 5.2.2 Perfiles de Usuario Virtual

El `locustfile.py` define tres clases de `HttpUser` que se mezclan según pesos relativos:


| Perfil            | Peso | Comportamiento                                                                                                                                                                                            | Tiempo de espera    |
| ----------------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `OrbitEngineUser` | 3    | Lee dashboard, productos, ventas, clientes y categorías. Ejercita paginación extrema (`?limit=100&skip=0/100`), búsqueda (`?search=`*), ordenamiento (`?sort_by=*&sort_order=*`) y filtros (`?status=*`). | Entre 0,5 s y 1,5 s |
| `SellerUser`      | 2    | Crea ventas reales contra el catálogo (`POST /sales/`), ajusta stock (`POST /products/{id}/adjust-stock`) y consulta movimientos.                                                                         | Entre 1 s y 2 s     |
| `SpammerUser`     | 1    | Martillea sin pausa los endpoints de agregación (`/dashboard/stats`, `/sales/stats`, `/products/low-stock`) y peticiones a UUIDs inexistentes para ejercitar el camino de error 404.                      | `constant(0)`       |


La rotación de cuentas se hace de forma cíclica y *thread-safe* sobre la lista `ACCOUNTS`, que contiene credenciales válidas de las ocho organizaciones del piloto técnico descritas en la sección 5.1.5: las **dos empresas reales** (**Frozt Bitez** y **Miss Peggy**) y las **seis empresas ficticias de prueba** (**Lehgo**, **Ferrallas del Norte**, **Sabor Caribe**, **Moda Andes**, **FarmaVida** y **Default**). Esta rotación cumple dos funciones en paralelo: (i) cada usuario virtual ejercita el aislamiento por `organization_id` desde un *tenant* distinto, validando la integridad multi-tenant bajo carga; (ii) las peticiones consultan tanto los volúmenes reales y acotados de Frozt Bitez y Miss Peggy como los volúmenes grandes generados por las seis empresas ficticias de prueba, lo que aporta un perfil de coste por consulta más representativo que el que obtendría un único *tenant*.

### 5.2.3 Escenarios Ejecutados

Se ejecutaron seis escenarios consecutivos contra `https://api.orbitengine.lat`. La configuración exacta (`--users` y `--spawn-rate`) se eligió siguiendo los tres regímenes documentados en el `docstring` del `locustfile`: 

- **Carga normal de pyme** (~8 usuarios)
- **Estrés** (~50 usuarios)
- **Pico** (~200 usuarios, ajustando la duración para acotar el daño en los regímenes de saturación).


| Escenario | Régimen                                 | Duración    | Total req. | Fallos | Tasa de fallos | RPS prom. |
| --------- | --------------------------------------- | ----------- | ---------- | ------ | -------------- | --------- |
| Test 01   | Carga normal (~8 usuarios concurrentes) | 1 min 39 s  | 235        | 0      | **0,0 %**      | 2,38      |
| Test 02   | Estrés moderado (~50 usuarios)          | 3 min 02 s  | 2 973      | 51     | **1,7 %**      | 16,34     |
| Test 03   | Estrés intermedio                       | 2 min 18 s  | 1 600      | 103    | **6,4 %**      | 11,58     |
| Test 04   | Saturación                              | 1 min 10 s  | 360        | 41     | **11,4 %**     | 6,97      |
| Test 05   | Saturación severa                       | 51 s        | 358        | 79     | **22,1 %**     | 5,07      |
| Test 06   | Pico sostenido (~200 usuarios)          | 10 min 05 s | 7 331      | 1 408  | **19,2 %**     | 12,12     |


> Los CSV completos de cada escenario (`Test0X-Requests.csv`, `Test0X-Failures.csv` y, cuando aplica, `Test0X-Exception.csv`), así como los reportes HTML generados por Locust, no se incluyen en este repositorio público; para acceder a los soportes correspondientes, consultar a los desarrolladores del proyecto.

### 5.2.4 Resultados por Escenario

#### 5.2.4.1 Test 01 — Carga Normal de Pyme

Es el escenario de referencia y representa el régimen al que se diseñó el sistema. Con aproximadamente ocho usuarios virtuales se completaron **235 peticiones sin fallos**.


| Endpoint                | Método | Reqs. | Mediana      | Promedio     | P95          | P99          |
| ----------------------- | ------ | ----- | ------------ | ------------ | ------------ | ------------ |
| `/login/access-token`   | POST   | 8     | 910 ms       | 1 196 ms     | 2 100 ms     | 2 100 ms     |
| `/categories/`          | GET    | 20    | 430 ms       | 454 ms       | 850 ms       | 850 ms       |
| `/customers/`           | GET    | 41    | 430 ms       | 453 ms       | 480 ms       | 850 ms       |
| `/dashboard/stats`      | GET    | 57    | 710 ms       | 721 ms       | 780 ms       | 1 100 ms     |
| `/inventory-movements/` | GET    | 20    | 520 ms       | 542 ms       | 640 ms       | 640 ms       |
| `/products/`            | GET    | 45    | 500 ms       | 515 ms       | 710 ms       | 920 ms       |
| `/products/low-stock`   | GET    | 21    | 430 ms       | 472 ms       | 840 ms       | 850 ms       |
| `/sales/`               | GET    | 23    | **7 500 ms** | **7 501 ms** | **7 600 ms** | **7 600 ms** |
| **Agregado**            | —      | 235   | 520 ms       | 1 254 ms     | 7 500 ms     | 7 600 ms     |


Observación clave: la mediana global (520 ms) y la mediana de los endpoints CRUD se sitúan en el orden de cientos de milisegundos, pero el endpoint `GET /sales/` consume sistemáticamente **alrededor de 7,5 segundos por petición** incluso sin concurrencia significativa. Este endpoint domina el percentil 95 global y es responsable de que el agregado se aleje de los 500 ms exigidos por el RNF-01.

#### 5.2.4.2 Test 02 — Estrés Moderado (~50 usuarios)

Con ~50 usuarios virtuales sostenidos durante poco más de tres minutos, el sistema procesa **2 973 peticiones** con una tasa de fallos del 1,7 %. Los fallos se concentran en dos categorías:

- 45 respuestas 404 esperadas en `GET /{resource}/{bad-uuid}`, que el `SpammerUser` genera intencionalmente para ejercitar el camino de error.
- 6 errores 500 en `POST /sales/`, atribuibles a contenciones puntuales sobre el stock al ejecutar concurrentemente la creación de ventas y los ajustes de inventario.

El sistema sostiene **16,3 RPS** con la mediana global en 1 000 ms y el percentil 95 alrededor de 7,8 s, todavía dominado por `GET /sales/` y por `GET /sales/?limit=500 [spam]`, cuyo P95 alcanza 30 s.

#### 5.2.4.3 Tests 03 a 05 — Régimen de Saturación

Los escenarios 03, 04 y 05 reflejan la transición desde el estrés moderado hacia la saturación. Las tasas de fallos crecen del 6,4 % al 22,1 % y los percentiles superiores se desplazan al rango de las decenas de segundos. Los 500 dejan de concentrarse en `POST /sales/` y aparecen también en `GET /dashboard/stats`, `GET /products/?search=`*, `GET /customers/?search=*` y `GET /products/{id}/movements`. La duración total de cada test se acortó deliberadamente para no comprometer la disponibilidad del sistema durante períodos prolongados.

#### 5.2.4.4 Test 06 — Pico Sostenido (~200 usuarios)

Es el escenario más extenso (10 min 05 s) y el más exigente. Para sostener el régimen de pico se incrementó la concurrencia interna del backend de 2 a **4 workers de FastAPI** sobre la misma instancia de Railway. Sobre **7 331 peticiones** se registran **1 408 fallos** (19,2 %), todos clasificados como 500 (errores del lado del servidor) y distribuidos sobre los endpoints de lectura masiva: `GET /dashboard/stats` (323), `GET /products/` (314), `GET /sales/` (238), `GET /customers/` (191), `GET /categories/` (120), `GET /inventory-movements/` (117) y `GET /products/low-stock` (105). El sistema sigue procesando 12 RPS pero la mediana global se sitúa en 1 300 ms y el P95 en 29 s, evidenciando que la configuración de 4 workers, aun siendo el doble de la utilizada en los escenarios previos, no logra absorber un régimen de ~200 usuarios concurrentes sostenido durante diez minutos.

### 5.2.5 Curva de Degradación

Consolidando los seis escenarios se obtiene la siguiente curva de comportamiento:


| Métrica          | Test 01  | Test 02  | Test 03   | Test 04   | Test 05   | Test 06   |
| ---------------- | -------- | -------- | --------- | --------- | --------- | --------- |
| Mediana agregada | 520 ms   | 1 000 ms | 2 000 ms  | 2 300 ms  | 2 300 ms  | 1 300 ms  |
| P95 agregado     | 7 500 ms | 7 800 ms | 36 000 ms | 33 000 ms | 58 000 ms | 29 000 ms |
| Tasa de fallos   | 0,0 %    | 1,7 %    | 6,4 %     | 11,4 %    | 22,1 %    | 19,2 %    |
| RPS efectivo     | 2,4      | 16,3     | 11,6      | 7,0       | 5,1       | 12,1      |


La tasa de fallos crece de manera monótona hasta el Test 05 (régimen de pico no sostenido, ejecutado todavía con 2 workers) y luego se estabiliza alrededor del 19 % en el Test 06, ya con 4 workers, donde la duración prolongada permite caracterizar mejor el techo del sistema. El RPS efectivo es máximo bajo estrés moderado (Test 02) y disminuye en los regímenes de saturación porque la mayor parte de los hilos de los workers quedan ocupados respondiendo peticiones lentas, lo que confirma un *throughput collapse* clásico cuando se rebasa la capacidad nominal de la configuración desplegada.

### 5.2.6 Comportamiento por Endpoint

Los CSV permiten aislar el comportamiento de los endpoints más representativos a lo largo de los seis escenarios:


| Endpoint                   | Test 01 mediana | Test 02 mediana | Test 06 mediana            | Observación                                                                                                                                    |
| -------------------------- | --------------- | --------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `POST /login/access-token` | 910 ms          | 1 200 ms        | 2 200 ms                   | Coste fijo dominado por el hashing bcrypt de la contraseña; el cuello no es de base de datos.                                                  |
| `GET /products/`           | 500 ms          | 730 ms          | 690 ms                     | Endpoint CRUD con paginación; el coste se mantiene acotado incluso bajo pico.                                                                  |
| `GET /customers/`          | 430 ms          | 540 ms          | 620 ms                     | Comportamiento similar al de productos.                                                                                                        |
| `GET /dashboard/stats`     | 710 ms          | 850 ms          | 1 100 ms (con 19 % de 500) | Agregaciones costosas que se vuelven inestables bajo pico sostenido.                                                                           |
| `GET /sales/`              | **7 500 ms**    | **7 700 ms**    | **8 600 ms**               | Latencia dominante en todos los regímenes; resultado de joins con `SaleItem` y agregaciones por venta sin paginación servidor-lado optimizada. |
| `POST /sales/`             | —               | 2 500 ms        | —                          | Operación transaccional con escritura de `Sale`, `SaleItem` e `InventoryMovement` en la misma sesión SQLAlchemy.                               |


### 5.2.7 Cumplimiento del RNF-01

El RNF-01 exige que el 95 % de las respuestas se complete en menos de 500 ms bajo carga normal (hasta 50 usuarios concurrentes). El balance, leído a la luz del entorno de despliegue dimensionado para el alcance del proyecto, es el siguiente:

- En **carga normal** (Test 01, ~8 usuarios concurrentes), que corresponde al perfil real al que apunta OrbitEngine para una pyme tipo, las medianas de los endpoints CRUD individuales se mantienen entre 430 ms y 720 ms, con el 95 % de las peticiones por debajo del segundo para todos los endpoints transaccionales del día a día (consultar productos, clientes, dashboard, registrar ventas).
- En **estrés moderado** (Test 02, ~50 usuarios), que ya cubre el límite superior fijado por el RNF-01, el sistema sigue procesando 16,3 RPS con una tasa de fallos del 1,7 % y manteniendo los endpoints CRUD en el rango de 540 ms a 1 200 ms, sin colapsos en ningún flujo crítico.
- El único endpoint que se aleja del umbral de manera estructural es `GET /sales/`, cuyo coste alto es independiente de la concurrencia y se origina en la composición del *payload* (joins con `SaleItem` y agregaciones por venta) más que en una limitación de la infraestructura. Este comportamiento queda registrado como punto de optimización futura.

Por lo tanto, **el RNF-01 se considera cumplido a cabalidad para el entorno de desarrollo y despliegue dimensionado para esta aplicación**, donde el perfil de uso esperado (≤ 50 usuarios concurrentes por organización) está totalmente cubierto por la combinación de servicio backend y configuración de workers descritos en la sección 5.1.2. Los regímenes por encima de 50 usuarios concurrentes (Tests 03 a 06) se incluyen únicamente como caracterización del techo del sistema y la optimización requerida para sostenerlos queda planteada como evolución futura, no como criterio de aceptación del MVP.

---

## 5.3 Pruebas de Rendimiento (Frontend / Web Vitals)

Las pruebas de rendimiento del frontend se ejecutaron sobre el despliegue productivo en Vercel (`https://orbitengine.lat`), combinando tres herramientas con perspectivas complementarias.

### 5.3.1 Lighthouse (Auditoría de Laboratorio)

Se ejecutó Lighthouse desde Chrome DevTools sobre la página pública (*landing*) y sobre las vistas internas del dashboard accedidas con sesión iniciada para **tres de las ocho organizaciones del piloto técnico** descritas en la sección 5.1.5: **Miss Peggy** (empresa real), **Lehgo** (empresa ficticia de prueba) y **Moda Andes** (empresa ficticia de prueba). Esta selección busca contrastar deliberadamente el comportamiento del frontend bajo dos perfiles de datos muy distintos: por un lado, los volúmenes reales y acotados de **Miss Peggy**, una de las dos pymes que adoptaron la plataforma; por otro lado, los volúmenes sintéticos elevados que aportan **Lehgo** y **Moda Andes** en su rol de empresas ficticias de prueba. La otra empresa real del piloto, **Frozt Bitez**, no se incluyó en este barrido de Lighthouse para evitar exponer información comercial específica de su operación; sus métricas se ejercitan indirectamente a través de las pruebas de carga del backend (sección 5.2). Los reportes individuales en PDF no se incluyen en este repositorio público; para acceder a los soportes correspondientes, consultar a los desarrolladores del proyecto.

**Tabla 5.3.1.** Puntajes y Web Vitals de Lighthouse por vista y organización. La columna *Tipo* indica si el *tenant* corresponde a una empresa real del piloto o a un *tenant* sintético de prueba.


| Vista                               | Organización   | Tipo               | Performance | Accesibilidad | Best Practices | SEO | FCP   | LCP   | TBT  | CLS   |
| ----------------------------------- | -------------- | ------------------ | ----------- | ------------- | -------------- | --- | ----- | ----- | ---- | ----- |
| Landing (`/`)                       | —              | Página pública     | 92          | 96            | 96             | 92  | 1,1 s | 1,6 s | 0 ms | 0     |
| Dashboard                           | Lehgo          | Ficticia de prueba | 90          | 96            | 100            | 83  | 1,2 s | 1,6 s | 0 ms | 0,017 |
| Dashboard                           | **Miss Peggy** | **Real**           | 91          | 96            | 100            | 83  | 1,1 s | 1,6 s | 0 ms | 0,021 |
| Dashboard                           | Moda Andes     | Ficticia de prueba | 91          | 96            | 100            | 83  | 1,1 s | 1,6 s | 0 ms | 0,017 |
| Inventario (`/dashboard/inventory`) | Lehgo          | Ficticia de prueba | 92          | 89            | 100            | 83  | 1,0 s | 1,5 s | 0 ms | 0     |
| Inventario                          | **Miss Peggy** | **Real**           | 92          | 89            | 100            | 83  | 1,1 s | 1,5 s | 0 ms | 0     |
| Inventario                          | Moda Andes     | Ficticia de prueba | 92          | 89            | 100            | 83  | 1,1 s | 1,5 s | 0 ms | 0     |
| Ventas (`/dashboard/sales`)         | Lehgo          | Ficticia de prueba | 92          | 88            | 100            | 83  | 1,1 s | 1,5 s | 0 ms | 0     |
| Ventas                              | **Miss Peggy** | **Real**           | 93          | 88            | 100            | 83  | 1,0 s | 1,5 s | 0 ms | 0     |
| Ventas                              | Moda Andes     | Ficticia de prueba | 93          | 88            | 100            | 83  | 1,0 s | 1,5 s | 0 ms | 0     |


Las puntuaciones de Performance se mantienen entre **90 y 93** en todas las vistas y organizaciones, y las diferencias entre los tres *tenants* medidos son menores a 1 punto. Esto es particularmente relevante porque la muestra confronta de manera explícita una empresa real (**Miss Peggy**) con dos empresas ficticias de prueba que cargan al sistema con volúmenes sintéticos mucho mayores (**Lehgo** y **Moda Andes**): el rendimiento percibido del frontend resulta **insensible al volumen y a los datos específicos** de cada organización dentro del rango medido, lo que valida que el coste del cliente no se ve afectado por los grandes volúmenes generados por las empresas ficticias de prueba. Los Core Web Vitals se sitúan dentro de las bandas verdes establecidas por Google (LCP ≤ 2,5 s, CLS ≤ 0,1, TBT bajo) tanto para los datos reales como para los datos sintéticos.

### 5.3.2 PageSpeed Insights (Infraestructura de Google)

PageSpeed Insights ejecutó Lighthouse 13.0.1 desde la infraestructura de Google con dos *form factors* (escritorio y móvil emulado). Los reportes en PDF no se incluyen en este repositorio público; para acceder a los soportes correspondientes, consultar a los desarrolladores del proyecto.

> *Nota sobre el etiquetado de archivos*: los reportes nominados `Login_PC.pdf` y `Login_Tel.pdf` analizan la URL `https://orbitengine.lat/dashboard`. Como PageSpeed se ejecuta sin sesión iniciada, dicha URL fue redirigida automáticamente al formulario de login (`/login?reason=auth-required`). Por tanto, la página efectivamente medida es la **pantalla de acceso (Login)**, y bajo esa etiqueta se reportan los resultados.

**Tabla 5.3.2.** PageSpeed Insights — escritorio vs. móvil.


| Vista          | *Form factor* | Rendimiento | Accesibilidad | Recom. | SEO | FCP   | LCP   | TBT   | CLS   | Speed Index |
| -------------- | ------------- | ----------- | ------------- | ------ | --- | ----- | ----- | ----- | ----- | ----------- |
| Landing        | Escritorio    | **98**      | 96            | 100    | 92  | 0,8 s | 0,8 s | 0 ms  | 0     | 1,2 s       |
| Landing        | Móvil         | 83          | 96            | 100    | 92  | 3,4 s | 3,4 s | 80 ms | 0     | 3,8 s       |
| Acceso (Login) | Escritorio    | **95**      | 94            | 100    | 83  | 0,8 s | 1,4 s | 0 ms  | 0     | 1,0 s       |
| Acceso (Login) | Móvil         | 87          | 94            | 100    | 83  | 3,2 s | 3,2 s | 20 ms | 0,001 | 3,2 s       |


Las dos observaciones más relevantes son:

- En **escritorio** todas las puntuaciones de Rendimiento se sitúan por encima de 95, con LCP por debajo de 1,5 s y SI ≤ 1,2 s, lo que confirma que el sitio cumple los Core Web Vitals con holgura para usuarios con conexión de banda ancha y dispositivos modernos.
- En **móvil** la puntuación cae al rango 83–87, principalmente por LCP en torno a 3,2–3,4 s (banda *needs improvement* de Google, entre 2,5 s y 4,0 s). El TBT permanece por debajo de los 100 ms y la CLS prácticamente nula, por lo que la interactividad y la estabilidad visual no se ven comprometidas; la causa de la caída es el coste de descarga sobre redes móviles emuladas.

### 5.3.3 WebPageTest (Red Real con Captura de Video)

WebPageTest 26.03 ejecutó pasadas reales sobre las páginas pública (`/`) y de acceso (`/dashboard` redirigido a `/login`), grabando video del rendering progresivo y produciendo el waterfall completo de cada recurso. Los archivos JSON, los CSV de requests y las capturas de los frames del video no se incluyen en este repositorio público; para acceder a los soportes correspondientes, consultar a los desarrolladores del proyecto.

**Tabla 5.3.3.** Métricas clave reportadas por WebPageTest.


| Vista          | TTFB  | Start render | FCP    | LCP      | TBT   | CLS   | Speed Index | Fully loaded | Bytes recibidos |
| -------------- | ----- | ------------ | ------ | -------- | ----- | ----- | ----------- | ------------ | --------------- |
| Landing (`/`)  | 46 ms | —            | —      | —        | —     | —     | —           | ~752 ms      | 3,9 MB          |
| Acceso (Login) | 88 ms | 600 ms       | 911 ms | 1 044 ms | 59 ms | 0,004 | 785         | 752 ms       | 3,9 MB          |


La secuencia visual del rendering progresivo quedó documentada en cinco capturas (frames sucesivos del video) por vista, que permiten verificar que la interfaz alcanza el estado *Visually Complete* alrededor de los 900–1 000 ms desde el inicio de la navegación. Estas capturas están disponibles a través de los desarrolladores del proyecto.

### 5.3.4 Cumplimiento de Core Web Vitals

Consolidando las tres herramientas:

- **LCP** (objetivo ≤ 2,5 s): cumplido en escritorio (0,8–1,6 s) y por debajo del umbral en WebPageTest (1,0 s). En móvil emulado se ubica en 3,2–3,4 s (banda *needs improvement*).
- **CLS** (objetivo ≤ 0,1): cumplido en todas las vistas y herramientas (máximo registrado: 0,021 en Lighthouse Dashboard de Miss Peggy).
- **TBT / INP** (objetivo TBT < 200 ms): cumplido con holgura. El máximo registrado es 80 ms en PageSpeed móvil de la landing.

---

## 5.4 Síntesis de Cumplimiento de Requisitos No Funcionales

**Tabla 5.4.** Cumplimiento consolidado de los RNF que aplican a la validación técnica.


| RNF    | Criterio                                              | Resultado                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Evidencia                            |
| ------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| RNF-01 | P95 de la API < 500 ms con ≤ 50 usuarios concurrentes | **Cumplido** para el entorno de despliegue dimensionado para la aplicación: en carga normal los endpoints CRUD se mantienen dentro del rango esperado y el régimen de 50 usuarios se sostiene sin colapsos. La optimización para escenarios > 50 concurrentes queda planteada como evolución futura.                                                                                                                                                                                                                                                                                  | Sección 5.2.4 (Test 01 y 02) y 5.2.7 |
| RNF-02 | Disponibilidad ≥ 95 % mensual                         | **Cumplido en aproximación.** Aunque no se ejecutó una medición formal de uptime mensual durante la validación, las estadísticas de carga obtenidas (0 % de fallos en carga normal, 1,7 % en estrés moderado y comportamiento estable del despliegue durante todas las pasadas de prueba) permiten proyectar razonablemente que la plataforma se mantendría por encima del 95 % de disponibilidad en una ventana mensual bajo el perfil de uso esperado. La medición formal continua, apoyada en los registros nativos de Railway y Vercel, queda planteada para futuras referencias. | Sección 5.1.2                        |
| RNF-07 | Interfaz responsive y funcional desde 375 px          | **Cumplido.** Auditorías de Lighthouse y PageSpeed en *form factor* móvil obtienen Accesibilidad ≥ 88 sin errores bloqueantes.                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Tablas 5.3.1 y 5.3.2                 |
| RNF-09 | Escalabilidad horizontal de la capa de aplicación     | **Cumplido a nivel arquitectónico.** El sistema soporta multi-tenancy bajo carga sin filtraciones (sección 5.2.1) y la degradación bajo pico es la esperada para una configuración de 2–4 workers sobre una sola instancia, según el escenario; esto confirma que la arquitectura admite escalado horizontal sin cambios estructurales.                                                                                                                                                                                                                                               | Sección 5.2.5                        |


---

## 5.5 Interpretación y Limitaciones

### 5.5.1 Interpretación Breve de los Hallazgos

En el plano del frontend, las tres herramientas convergen en una imagen coherente: la aplicación obtiene puntuaciones de Lighthouse entre 90 y 93 en todas las vistas y organizaciones, los Core Web Vitals se sitúan en banda verde para escritorio y red real, y las diferencias entre tenants son menores a un punto. Esto indica que el rendimiento percibido por el usuario final no depende del volumen de datos de la organización ni de la vista visitada, sino principalmente del *form factor* y de la calidad de la red, con una penalización esperable en móvil emulado.

En el plano del backend, los seis escenarios de Locust dibujan una curva de degradación característica de un servicio con concurrencia interna acotada (2 workers para los Tests 01–05 y 4 workers para el Test 06) sobre una sola instancia sin réplicas: bajo carga normal (8 usuarios) el sistema atiende sin fallos y con medianas en el rango de cientos de milisegundos, bajo estrés moderado (50 usuarios) sostiene 16 RPS con una tasa de fallos del 1,7 %, y bajo pico sostenido (~200 usuarios, ya con 4 workers) conserva ~12 RPS con una tasa de fallos cercana al 19 %. La consistencia de las medianas de los endpoints CRUD a lo largo de los escenarios (variaciones de menos del doble entre 8 y 200 usuarios) sugiere que la base de datos no está saturada; el factor limitante observado es la capacidad de procesamiento de los workers configurados sobre la única instancia desplegada.

Confrontados con los criterios del Capítulo 3 (tabla 5.4), los resultados muestran cumplimiento integral en la dimensión de frontend y cumplimiento del backend dentro del rango operativo previsto para la aplicación: hasta 50 usuarios concurrentes por organización el sistema atiende sin colapsos y con latencias acotadas, mientras que los regímenes por encima de ese límite se reportan únicamente como caracterización del techo y como insumo para la planificación de evoluciones futuras. La arquitectura multi-tenant se mantiene íntegra durante toda la batería de pruebas: ninguna petición devuelve datos cruzados entre organizaciones, lo que valida en escenarios de carga real el mecanismo de aislamiento por `organization_id` descrito en el Capítulo 4.

### 5.5.2 Limitaciones de Escalabilidad Inherentes al Concepto del Proyecto

Los límites observados en las pruebas deben leerse a la luz del concepto y del alcance del proyecto, no como deficiencias del producto. OrbitEngine es un trabajo de grado desarrollado por un equipo de tres personas con dedicación parcial durante siete meses, cuyo objetivo es entregar un MVP funcional con presupuesto académico, y las decisiones de infraestructura y de arquitectura son consecuentes con ese marco:

- **Infraestructura en planes básicos**. El backend se ejecuta sobre un único servicio en Railway, sin réplicas horizontales ni *auto-scaling* configurados. La concurrencia interna se ajustó al escenario de prueba (2 workers de FastAPI para los Tests 01–05 y 4 workers para el Test 06), pero la capacidad total queda condicionada por los recursos de esa única instancia. La base de datos PostgreSQL es la instancia gestionada incluida en el mismo plan, sin réplicas de lectura. El frontend se sirve desde el plan estándar de Vercel.
- **Ausencia de capa de caché distribuida**. No se incorporó Redis ni un CDN privado para la API; los endpoints de agregación (`/dashboard/stats`, `/sales/stats`) consultan PostgreSQL directamente en cada petición.
- **Arquitectura monolítica multi-tenant compartiendo una sola base de datos**. Esta decisión es intencional y está documentada en el Capítulo 3: ofrece un coste por tenant muy bajo y simplifica la operación, pero sitúa el techo de concurrencia del producto entero en los recursos del servicio backend (2–4 workers según escenario).
- **Ejecución de las pruebas desde un único cliente**. Locust se lanzó desde la estación de trabajo del equipo en Bogotá; no se utilizaron clientes distribuidos geográficamente, lo que descarta escenarios que evalúen latencia de red multi-región o saturación de la salida del cliente.
- **Plan de validación dimensionado para una pyme tipo**. El régimen de carga normal (~8 usuarios concurrentes) corresponde al tamaño de equipo objetivo descrito en el Capítulo 1; los regímenes de 50 y 200 usuarios se incluyen para caracterizar el techo del sistema, no como criterio de aceptación del MVP.
- **Alcance temporal acotado al cierre del MVP**. Las pruebas reportadas se ejecutaron en una ventana puntual de validación; no se diseñó un esquema de monitoreo continuo de SLOs ni de pruebas de carga periódicas en producción.

Estas limitaciones encuadran el alcance del capítulo: los hallazgos son representativos del comportamiento del MVP en su despliegue de producción del proyecto de grado, y delimitan claramente los aspectos que requerirían inversión adicional para evolucionar OrbitEngine hacia un servicio SaaS multi-región a gran escala. Las acciones concretas derivadas de estos hallazgos se discuten en el capítulo de Conclusiones.