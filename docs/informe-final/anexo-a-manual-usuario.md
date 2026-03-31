# Anexo A — Manual de Usuario

**OrbitEngine** — Plataforma SaaS para la Gestión de Procesos Internos en Pymes  
Versión: 1.0 | Abril 2026  
Universidad Sergio Arboleda — Semillero de Software como Innovación

---

## A.1 Introducción

Este manual describe el uso de OrbitEngine para los usuarios finales de la plataforma. OrbitEngine es una aplicación web multi-tenant que permite a pequeñas y medianas empresas gestionar en un solo lugar sus operaciones de **inventario**, **ventas** y **clientes**, con un panel de indicadores clave de desempeño (KPIs) accesible en tiempo real.

El sistema opera completamente desde el navegador web, sin necesidad de instalar software adicional. Cada empresa (organización) tiene su propio espacio de trabajo completamente aislado de las demás.

---

## A.2 Acceso a la Plataforma

### A.2.1 Página de inicio

Al ingresar a la URL de OrbitEngine, el usuario accede a la **página de presentación** (landing page) que muestra las características de la plataforma. Desde esta página se puede navegar a las opciones de inicio de sesión o registro.

### A.2.2 Registro de organización

Para crear una nueva empresa en la plataforma:

1. Hacer clic en **"Comenzar gratis"** o en el enlace de registro en la barra de navegación.
2. En la pantalla `/signup-org`, completar el formulario con:
   - **Nombre de la organización** — nombre visible de la empresa.
   - **Slug** — identificador único en minúsculas (ej. `mi-empresa`). Solo letras, números y guiones; entre 3 y 50 caracteres.
   - **Descripción** *(opcional)* — breve descripción del negocio.
   - **Nombre**, **apellido** y **correo electrónico** del administrador.
   - **Contraseña** de al menos 8 caracteres.
3. Hacer clic en **"Crear organización"**.
4. El sistema crea la organización y la cuenta administrador automáticamente y redirige al panel de control.

### A.2.3 Invitación de usuarios

Los usuarios adicionales **no se registran por su cuenta**: son creados por el administrador desde el módulo **Admin**. Una vez creada la cuenta, el usuario recibe las credenciales y puede ingresar con ellas.

### A.2.4 Inicio de sesión

1. Ir a la pantalla `/login`.
2. Ingresar el **correo electrónico** y la **contraseña**.
3. Hacer clic en **"Ingresar"**.
4. Si las credenciales son correctas, el sistema redirige al **panel de control** (`/dashboard`).

### A.2.5 Recuperación de contraseña

Si olvidó su contraseña:

1. En la pantalla de inicio de sesión, hacer clic en **"¿Olvidaste tu contraseña?"**.
2. Ingresar el correo electrónico asociado a la cuenta.
3. Revisar la bandeja de entrada y hacer clic en el enlace recibido.
4. En la pantalla `/reset-password`, ingresar y confirmar la nueva contraseña.
5. Hacer clic en **"Restablecer contraseña"**.

### A.2.6 Cierre de sesión

Para cerrar sesión, hacer clic en el **ícono de usuario** en la barra lateral izquierda y seleccionar **"Cerrar sesión"**. La sesión expira automáticamente después de 8 días de inactividad.

---

## A.3 Navegación General

Una vez dentro del sistema, la interfaz se divide en:

- **Barra lateral izquierda** — menú principal de navegación con acceso a todos los módulos.
- **Área de contenido principal** — donde se muestra y gestiona la información de cada módulo.
- **Panel de usuario** (parte inferior de la barra lateral) — acceso a configuración personal y cierre de sesión.

Los módulos disponibles son:

| Módulo | Ruta | Acceso |
|--------|------|--------|
| Dashboard | `/dashboard` | Todos los usuarios |
| Inventario | `/dashboard/inventory` | Todos los usuarios |
| Ventas | `/dashboard/sales` | Todos los usuarios |
| Clientes | `/dashboard/customers` | Todos los usuarios |
| Administración | `/dashboard/admin` | Solo Administradores |
| Configuración | `/dashboard/settings` | Todos los usuarios |

---

## A.4 Dashboard — Panel de Indicadores

El dashboard muestra un resumen del estado del negocio en tiempo real para la organización activa.

**Indicadores disponibles:**

- **Ventas del día** — total en dinero de las ventas registradas hoy.
- **Ventas del mes** — total acumulado del mes en curso.
- **Ticket promedio** — valor promedio por venta en el período.
- **Productos con stock bajo** — conteo de productos que están por debajo del mínimo configurado.
- **Top productos** — listado de los productos más vendidos.
- **Ventas por día** — gráfica de barras con la evolución diaria de ventas.

El dashboard se actualiza automáticamente con cada consulta. No requiere acción adicional del usuario.

---

## A.5 Módulo de Inventario

El módulo de inventario permite gestionar los productos y categorías de la empresa, así como llevar el control detallado de los movimientos de stock.

### A.5.1 Categorías

Las categorías permiten organizar el inventario en grupos lógicos. Admiten **jerarquía** (una categoría puede tener subcategorías).

**Crear una categoría:**
1. En el módulo Inventario, ir a la pestaña **Categorías**.
2. Hacer clic en **"Agregar categoría"**.
3. Completar el **nombre** *(requerido)* y opcionalmente una **descripción** y una **categoría padre**.
4. Guardar.

**Editar o desactivar una categoría:**
- Hacer clic en el menú de acciones (⋮) de la fila y seleccionar **"Editar"** o **"Desactivar"**.

### A.5.2 Productos

**Crear un producto:**
1. En el módulo Inventario, ir a la pestaña **Productos**.
2. Hacer clic en **"Agregar producto"**.
3. Completar el formulario:
   - **Nombre** *(requerido)*
   - **SKU** — código único del producto *(requerido)*
   - **Categoría** *(opcional)*
   - **Precio de costo** y **precio de venta**
   - **Stock actual**, **stock mínimo** y **stock máximo** *(opcional)*
   - **Unidad de medida** (ej. `unit`, `kg`, `lt`)
   - **Código de barras** *(opcional)*
   - **Descripción** e **imagen** *(opcionales)*
4. Guardar.

**Editar un producto:**
- Hacer clic en el menú de acciones (⋮) → **"Editar"**. Todos los campos son modificables excepto el SKU si ya tiene movimientos.

**Desactivar un producto:**
- Hacer clic en el menú de acciones (⋮) → **"Desactivar"**. El producto deja de aparecer en los formularios de venta pero su historial se conserva.

**Alerta de stock bajo:**
- Los productos con `stock_quantity ≤ stock_min` aparecen resaltados en la tabla y se contabilizan en el indicador del dashboard.

### A.5.3 Ajuste de stock manual

Para corregir el inventario por diferencias de conteo, mermas u otros motivos:

1. En la tabla de productos, seleccionar el producto y hacer clic en **"Ajustar stock"**.
2. Ingresar la **cantidad** (positiva para agregar, negativa para restar).
3. Ingresar un **motivo** del ajuste *(requerido)*.
4. Confirmar.

El ajuste queda registrado en el historial de movimientos con el tipo `adjustment`.

### A.5.4 Historial de movimientos

El historial registra todos los cambios de stock de cada producto:

| Tipo de movimiento | Descripción |
|--------------------|-------------|
| `sale` | Salida generada por una venta |
| `adjustment` | Entrada o salida manual |
| `return` | Entrada por devolución o cancelación de venta |
| `purchase` | Entrada por compra |

Para ver el historial de un producto:
1. En la tabla de productos, hacer clic en el menú de acciones (⋮) → **"Ver historial de movimientos"**.
2. Se muestra la tabla con fecha, tipo, cantidad, stock anterior y stock resultante, y el usuario que realizó el movimiento.

---

## A.6 Módulo de Ventas

El módulo de ventas permite registrar transacciones comerciales, visualizar el historial y cancelar ventas cuando sea necesario.

### A.6.1 Registrar una venta

1. En el módulo Ventas, hacer clic en **"Nueva venta"**.
2. Completar el formulario:
   - **Cliente** *(opcional)* — buscar por nombre o documento.
   - **Método de pago**: Efectivo, Tarjeta, Transferencia u Otro.
   - **Descuento** y **IVA/impuesto** *(opcional, en valores monetarios)*.
   - **Notas** *(opcional)*.
3. En la sección de **ítems**, agregar los productos de la venta:
   - Buscar el producto por nombre o SKU.
   - Ingresar la **cantidad**.
   - El sistema calcula el precio unitario y el subtotal del ítem automáticamente.
4. El sistema calcula en tiempo real: subtotal, descuento, impuesto y **total**.
5. Hacer clic en **"Registrar venta"**.

Al guardar, el sistema:
- Genera un **número de factura** único.
- Descuenta las cantidades del stock de cada producto registrado.
- Registra los movimientos de inventario correspondientes (`sale`).
- Actualiza el total de compras del cliente, si se asoció uno.

### A.6.2 Ver detalle de una venta

En la tabla de ventas, hacer clic en el menú de acciones (⋮) → **"Ver detalle"**. Se muestra la información completa: número de factura, cliente, fecha, ítems, totales y método de pago.

### A.6.3 Cancelar una venta

Una venta puede cancelarse mientras tenga estado `completed`:

1. En la tabla de ventas, hacer clic en el menú de acciones (⋮) → **"Cancelar venta"**.
2. Ingresar el **motivo de cancelación** *(requerido)*.
3. Confirmar.

Al cancelar, el sistema:
- Cambia el estado de la venta a `cancelled`.
- **Revierte el stock** de cada producto afectado (movimiento tipo `return`).
- Registra la fecha y usuario de cancelación.

### A.6.4 Filtros y búsqueda

La tabla de ventas permite:
- Buscar por **número de factura**.
- Filtrar por **estado** (`completed`, `cancelled`) y **método de pago**.
- Ordenar por cualquier columna.

---

## A.7 Módulo de Clientes

El módulo permite gestionar el directorio de clientes de la organización y consultar su historial de compras.

### A.7.1 Registrar un cliente

1. En el módulo Clientes, hacer clic en **"Agregar cliente"**.
2. Completar el formulario:
   - **Tipo de documento**: CC, NIT, Pasaporte, Otro *(requerido)*.
   - **Número de documento** *(requerido, único por organización)*.
   - **Nombre** y **apellido** *(requeridos)*.
   - **Correo electrónico**, **teléfono**, **dirección**, **ciudad** y **país** *(opcionales)*.
   - **Notas internas** *(opcionales)*.
3. Guardar.

### A.7.2 Editar un cliente

- Hacer clic en el menú de acciones (⋮) → **"Editar"**. Se pueden modificar todos los campos excepto el número de documento.

### A.7.3 Desactivar un cliente

- Hacer clic en el menú de acciones (⋮) → **"Desactivar"**. El cliente se desactiva pero su historial de compras se conserva.

### A.7.4 Historial de compras del cliente

- Hacer clic en el menú de acciones (⋮) → **"Ver historial de compras"**.
- Se muestran todas las ventas asociadas al cliente con fecha, número de factura, total y estado.
- Se visualizan también los indicadores: **total acumulado de compras**, **número de compras** y **fecha de última compra**.

---

## A.8 Módulo de Administración

> Este módulo es exclusivo para usuarios con el rol **Administrador**.

El módulo de administración permite gestionar las cuentas de usuario de la organización.

### A.8.1 Ver usuarios

La tabla muestra todos los usuarios de la organización con su nombre, correo, rol y estado (activo/inactivo).

### A.8.2 Crear un usuario

1. Hacer clic en **"Agregar usuario"**.
2. Completar el formulario:
   - **Nombre** y **apellido**.
   - **Correo electrónico** — será el identificador de ingreso.
   - **Contraseña** temporal.
   - **Rol** — seleccionar entre los roles disponibles de la organización.
3. Guardar.

El nuevo usuario puede ingresar inmediatamente con las credenciales proporcionadas y cambiar su contraseña desde la configuración.

### A.8.3 Editar un usuario

- Hacer clic en el menú de acciones (⋮) → **"Editar"**. Se pueden cambiar nombre, apellido y rol.

### A.8.4 Eliminar un usuario

- Hacer clic en el menú de acciones (⋮) → **"Eliminar"**.
- Confirmar la acción en el diálogo de confirmación.

> **Advertencia:** Esta acción es permanente. El historial de ventas y movimientos del usuario permanece registrado.

---

## A.9 Configuración

El módulo de configuración permite al usuario gestionar su cuenta personal y, si es administrador, los datos de la organización.

### A.9.1 Información personal

En la pestaña **"Perfil"**:
- Ver y editar **nombre** y **apellido**.
- Ver el **correo electrónico** asociado (no editable desde aquí).

### A.9.2 Cambio de contraseña

En la pestaña **"Seguridad"**:
1. Ingresar la **contraseña actual**.
2. Ingresar la **nueva contraseña** y confirmarla.
3. Hacer clic en **"Actualizar contraseña"**.

### A.9.3 Configuración de la organización

> Disponible solo para usuarios con rol **Administrador**.

En la pestaña **"Organización"**:
- Editar el **nombre** de la organización.
- Editar el **slug** *(identificador único)*.
- Editar la **descripción** y la **URL del logo**.

### A.9.4 Apariencia

En la pestaña **"Apariencia"**:
- Cambiar entre **modo claro** y **modo oscuro**.

### A.9.5 Eliminación de cuenta

En la pestaña **"Cuenta"**:
- El usuario puede solicitar la **eliminación de su propia cuenta**.
- Se requiere confirmación escribiendo el correo electrónico.

> **Nota:** La eliminación de cuenta no elimina el historial de transacciones asociadas.

---

## A.10 Preguntas Frecuentes

**¿Puedo usar OrbitEngine desde el celular?**  
Sí. La interfaz está diseñada de manera responsiva y funciona en navegadores móviles modernos (Chrome, Safari). La experiencia óptima es en pantallas de escritorio o tabletas.

**¿Mis datos están separados de los de otras empresas?**  
Sí. Cada organización tiene un espacio de trabajo completamente aislado. No es posible ver ni acceder a datos de otras organizaciones.

**¿Qué pasa si cancelo una venta? ¿El stock vuelve?**  
Sí. Al cancelar una venta, el sistema revierte automáticamente el stock de todos los productos incluidos en ella.

**¿Puedo tener múltiples roles para usuarios?**  
Actualmente cada usuario tiene un único rol. Los roles definen los permisos de acceso a los módulos y acciones disponibles.

**¿Cómo sé cuándo un producto está por agotarse?**  
Los productos cuyo stock actual es igual o menor al **stock mínimo** configurado aparecen resaltados en la tabla de inventario y se contabilizan en el indicador "Productos con stock bajo" del dashboard.

**¿Se puede exportar la información a Excel o PDF?**  
La exportación de reportes es una funcionalidad planificada para versiones futuras. Actualmente los datos se visualizan dentro de la plataforma.

**¿Qué navegadores son compatibles?**  
OrbitEngine es compatible con las versiones recientes de Chrome, Firefox, Edge y Safari. No se garantiza compatibilidad con Internet Explorer.

---

*Documento generado como parte del proyecto de grado — Universidad Sergio Arboleda, Semillero de Software como Innovación, Abril 2026.*
