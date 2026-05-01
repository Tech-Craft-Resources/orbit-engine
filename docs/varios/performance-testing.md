# Guía de Pruebas de Rendimiento — OrbitEngine

## 1. Google PageSpeed Insights

Mide el rendimiento del frontend con los Core Web Vitals de Google. Da un puntaje de 0–100.

### Paso a paso

1. Despliega la app (debe tener una URL pública — no funciona en localhost).
2. Ve a **pagespeed.web.dev**.
3. Pega la URL del frontend (ej. `https://orbitengine.tu-dominio.com`).
4. Haz clic en **Analizar**.
5. Espera ~30 segundos. Verás dos pestañas: **Móvil** y **Escritorio** — revisa ambas.

### Qué mirar en el reporte

| Métrica | Qué mide | Meta |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Tiempo hasta que el elemento principal es visible | < 2.5 s |
| **FID** / **INP** | Tiempo de respuesta al primer clic | < 200 ms |
| **CLS** (Cumulative Layout Shift) | Qué tanto "salta" el contenido al cargar | < 0.1 |
| **FCP** (First Contentful Paint) | Tiempo hasta ver algo en pantalla | < 1.8 s |
| **TTFB** (Time to First Byte) | Tiempo de respuesta del servidor | < 800 ms |

### Para el informe

- Toma captura del puntaje de escritorio.
- En la sección "Diagnóstico" aparecen las recomendaciones priorizadas — menciona las 2–3 más importantes.
- Un puntaje ≥ 70 es considerado "bueno" para una app web con autenticación.

---

## 2. Lighthouse (en Chrome — funciona en localhost)

Lighthouse está integrado en Chrome DevTools. Ventaja: no necesitas URL pública, funciona en `localhost`.

### Paso a paso

1. Abre Chrome y navega a tu app (ej. `http://localhost:5173`).
2. Inicia sesión para que Lighthouse vea las rutas protegidas.
3. Navega a la página que quieres analizar (ej. el Dashboard).
4. Abre DevTools: `F12` o `Ctrl+Shift+I`.
5. Ve a la pestaña **Lighthouse** (puede estar oculta bajo `>>`).
6. En "Categories" selecciona: ✅ Performance, ✅ Accessibility, ✅ Best Practices.
7. En "Device" elige **Desktop**.
8. Haz clic en **Analyze page load**.
9. Espera ~1 minuto. Se genera un reporte completo.

### Páginas recomendadas a analizar

- `/dashboard` — página principal con KPIs y gráficas (la más pesada).
- `/products` — lista con paginación.
- `/sales/new` — formulario con múltiples campos.

### Para el informe

- Exporta el reporte: botón **Download report** → elige PDF o HTML.
- Anota el puntaje de Performance para cada página analizada.

---

## 3. WebPageTest (webpagetest.org)

La herramienta más detallada. Muestra exactamente qué recursos tardan más en cargar (waterfall).

### Paso a paso

1. Ve a **webpagetest.org** (requiere URL pública).
2. En el campo URL pega la dirección del frontend.
3. Configura las opciones:
   - **Test Location:** elige el más cercano a Colombia (ej. "São Paulo, Brazil" o "Dulles, VA").
   - **Browser:** Chrome.
   - **Connection:** Cable (para simular usuario típico) o 3G (para simular peor caso).
4. Haz clic en **Start Test**. Tarda 2–3 minutos.
5. El reporte muestra:
   - **Waterfall:** cada archivo que carga el navegador, en orden y con su duración.
   - **Web Vitals:** LCP, CLS, TBT.
   - **Filmstrip view:** capturas de pantalla de cómo se ve la página mientras carga.

### Qué buscar

- Archivos JS/CSS que tardan más de 1 s en descargar.
- Solicitudes al backend (API) con TTFB alto.
- Recursos sin caché (encabezado `Cache-Control` ausente).

### Para el informe

- Descarga el reporte PDF desde el botón **Export**.
- El "Speed Index" y el "Load Time" son buenas métricas para citar.

---

## 4. Curl en loop (tiempos de respuesta de la API)

`curl` es una herramienta de terminal que hace peticiones HTTP. "En loop" significa ejecutarla varias veces seguidas y anotar los tiempos.

### Qué hace exactamente

```bash
curl -o /dev/null -s -w "%{time_total}\n" https://tu-dominio.com/api/v1/products/
```

- `-o /dev/null` — descarta el body de la respuesta (no nos interesa el contenido).
- `-s` — silencia la barra de progreso.
- `-w "%{time_total}\n"` — imprime solo el tiempo total en segundos.

### Cómo usarlo en loop (10 mediciones)

```bash
# En bash/Git Bash (Windows)
for i in {1..10}; do
  curl -o /dev/null -s -w "%{time_total}\n" https://tu-dominio.com/api/v1/products/
done
```

Salida típica:
```
0.312
0.287
0.301
0.298
...
```

Promedia esos números para el informe. **Meta: < 0.500 segundos promedio.**

### Para endpoints protegidos (con token)

```bash
TOKEN="eyJhbGci..."   # pega tu token JWT aquí

for i in {1..10}; do
  curl -o /dev/null -s \
    -H "Authorization: Bearer $TOKEN" \
    -w "%{time_total}\n" \
    https://tu-dominio.com/api/v1/dashboard/stats
done
```

Para obtener el token: inicia sesión en la app, abre DevTools → Network → cualquier petición a `/api/v1/` → copia el header `Authorization`.

### Endpoints clave a medir

```bash
# Listar productos
curl ... /api/v1/products/

# Listar ventas
curl ... /api/v1/sales/

# Dashboard stats (el más pesado)
curl ... /api/v1/dashboard/stats
```
