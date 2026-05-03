# Pruebas de Carga con Locust — OrbitEngine

## ¿Qué es Locust?

Locust es una herramienta de pruebas de carga de código abierto escrita en Python. Simula múltiples usuarios usando la aplicación al mismo tiempo y mide cómo responde el servidor: tiempos de respuesta, errores y peticiones por segundo.

A diferencia de PageSpeed Insights o Lighthouse (que prueban un solo usuario), Locust responde la pregunta: **¿qué pasa cuando 8 personas usan OrbitEngine al mismo tiempo?**

---

## Instalación

Desde la carpeta `backend/`:

```bash
cd backend
uv add --dev locust
```

Eso es todo. No requiere configuración adicional.

---

## Cómo ejecutarlo

**1. Lanzar Locust con interfaz web:**

```bash
cd backend
uv run locust -f tests/performance/locustfile.py --host=https://api.orbitengine.lat
```

**2. Abrir el panel de control** en el navegador:

```
http://localhost:8089
```

**3. Configurar la prueba** en el formulario que aparece:

| Campo | Valor recomendado | Qué significa |
|---|---|---|
| Number of users | `8` | Cuántos usuarios simultáneos se simulan |
| Spawn rate | `1` | Cuántos usuarios arrancan por segundo (gradual) |
| Host | `https://api.orbitengine.lat` | Ya viene pre-llenado |

**4. Hacer clic en Start.** El panel muestra en tiempo real:

- **RPS** — peticiones por segundo que recibe el servidor.
- **Response time (ms)** — tiempo promedio, p50, p90, p95 de cada endpoint.
- **Failures** — peticiones que fallaron (idealmente 0%).

**5. Dejar correr ~60 segundos** y luego hacer clic en **Stop**.

**6. Descargar el reporte:** botón **Download Data → Download Report (HTML)** — este archivo es el que va como evidencia en el Capítulo 5 del informe.

---

## Qué hace con las cuentas configuradas

El archivo `locustfile.py` tiene 8 cuentas reales de OrbitEngine, una por cada empresa piloto:

| Cuenta | Empresa |
|---|---|
| carito_16172@hotmail.com | Ferrallas |
| daniel.velasco01@usa.edu.co | Sabor Caribe |
| marior.16@hotmail.com | Moda Andes |
| info@froztbitez.com | Frozt Bitez |
| nicolas.rodriguez10@usa.edu.co | FarmaVida |
| nicolas.rodriguez2004@outlook.com | lehgo |
| niquimiqui@gmail.com | Miss Peggy |
| orbitengine3@gmail.com | default |

### Flujo por usuario virtual

Cuando la prueba arranca, cada usuario virtual ejecuta estos pasos en orden:

```
1. Toma la siguiente cuenta de la lista (rotación cíclica)
2. Hace POST /api/v1/login/access-token  →  obtiene un token JWT
3. Guarda el token para todas sus peticiones siguientes
4. Empieza a navegar por la API de forma aleatoria:
      - GET /dashboard/stats          (frecuencia alta — peso 3)
      - GET /products/                (frecuencia alta — peso 3)
      - GET /sales/                   (frecuencia media — peso 2)
      - GET /customers/               (frecuencia media — peso 2)
      - GET /products/low-stock       (frecuencia baja — peso 1)
      - GET /inventory-movements/     (frecuencia baja — peso 1)
      - GET /categories/              (frecuencia baja — peso 1)
5. Entre cada petición espera entre 1 y 3 segundos (simula un humano real)
```

### Por qué usar cuentas distintas

Cada cuenta pertenece a una organización diferente. Esto significa que cada usuario virtual consulta datos aislados (multi-tenancy real), lo que es más representativo que 8 sesiones del mismo usuario. Si el servidor tuviera algún problema de aislamiento entre organizaciones, esta prueba también lo revelaría.

---

## Modo de estrés máximo (romper el servidor)

Para buscar el límite real del sistema, usa más usuarios con spawn rápido:

```bash
cd backend
uv run locust -f tests/performance/locustfile.py \
    --host=https://api.orbitengine.lat \
    --headless \
    --users 50 \
    --spawn-rate 5 \
    --run-time 120s \
    --html reporte-estres.html
```

Con interfaz web puedes ir subiendo los usuarios en caliente (botón **Edit**) mientras la prueba corre para encontrar el punto de quiebre.

---

## Clases de usuario

El archivo tiene tres perfiles distintos que Locust mezcla automáticamente según su peso:

| Clase | Peso | `wait_time` | Qué hace |
|---|---|---|---|
| `OrbitEngineUser` | 3 | 0.5–1.5 s | Lector realista: paginación, búsquedas, filtros, ordenamiento |
| `SellerUser` | 2 | 1–2 s | Crea ventas reales con productos del catálogo y ajusta stock |
| `SpammerUser` | 1 | 0 s (sin pausa) | Martilla dashboard/stats y endpoints de agregación sin descanso |

---

## Modo sin interfaz (solo terminal)

Si quieres correrlo de forma automatizada sin abrir el navegador:

```bash
cd backend
uv run locust -f tests/performance/locustfile.py \
    --host=https://api.orbitengine.lat \
    --headless \
    --users 8 \
    --spawn-rate 1 \
    --run-time 60s \
    --html reporte-carga.html
```

Al finalizar genera `reporte-carga.html` directamente en la carpeta `backend/`.

---

## Métricas a anotar para el Capítulo 5

Al terminar la prueba, registra estos valores de la tabla de resultados:

| Métrica | Dónde verla | Meta |
|---|---|---|
| Tiempo de respuesta promedio | Columna "Average (ms)" | < 500 ms |
| Percentil 95 (p95) | Columna "95%ile (ms)" | < 1000 ms |
| Tasa de errores | Columna "Failure %" | 0 % |
| Peticiones por segundo | Panel superior "RPS" | — (informativo) |
