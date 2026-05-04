# OrbitEngine – Frontend

Aplicación web construida con **React 19**, **TypeScript 5** y **Vite 7**. Usa TanStack Router para routing file-based, TanStack Query para estado del servidor, React Hook Form + Zod para formularios y shadcn/ui como sistema de componentes.

---

## Requisitos

- [Bun](https://bun.sh/)
- Backend corriendo (Docker o local)

---

## Desarrollo Local (recomendado)

Para mejor experiencia (hot-reload instantáneo), detén el contenedor de frontend y corre Bun directamente:

```bash
# Detener el contenedor de frontend
docker compose stop frontend

cd frontend

# Instalar dependencias (solo la primera vez)
bun install

# Servidor de desarrollo
bun run dev
```

El frontend estará en http://localhost:5173 y se conectará automáticamente al backend en Docker.

---

## Scripts Disponibles

```bash
bun run dev             # Servidor de desarrollo con hot-reload
bun run build           # Build de producción (tsc + vite build)
bun run lint            # Lint y auto-fix con Biome
bun run preview         # Preview del build de producción
bun run generate-client # Regenerar cliente API desde OpenAPI
bun run test            # Tests E2E con Playwright
bun run test:ui         # Tests E2E en modo interactivo
```

---

## Estructura de Código

```
frontend/src/
├── client/                     # Cliente API auto-generado (NO EDITAR)
│   ├── types.gen.ts            # Tipos TypeScript desde schemas Pydantic
│   ├── sdk.gen.ts              # Métodos de servicio por dominio
│   └── core/                  # Internals del cliente HTTP
│
├── components/
│   ├── Admin/                  # Gestión de usuarios (AddUser, EditUser, DeleteUser…)
│   ├── Common/                 # Compartidos: DataTable, AuthLayout, RoleGuard, Footer…
│   ├── Customers/              # Módulo clientes (CRUD, historial de compras)
│   ├── Dashboard/              # Exportaciones e indicadores
│   ├── Inventory/              # Módulo inventario (productos, categorías, movimientos)
│   ├── Landing/                # Página pública (Hero, Features, Benefits, Stats, CTA)
│   ├── Pending/                # Usuarios pendientes de aprobación
│   ├── Sales/                  # Módulo ventas (registro, detalle, cancelación)
│   ├── Sidebar/                # Navegación lateral (AppSidebar, Main, User)
│   ├── UserSettings/           # Ajustes (perfil, contraseña, organización, cuenta)
│   └── ui/                     # shadcn/ui (NO EDITAR)
│
├── hooks/
│   ├── useAuth.ts              # Autenticación, usuario actual, organización, roles
│   ├── useCustomToast.ts       # Toasts de éxito/error con Sonner
│   ├── useCopyToClipboard.ts   # Copiar al portapapeles
│   └── useMobile.ts            # Detección de viewport mobile
│
├── routes/                     # Páginas (TanStack Router file-based)
│   ├── __root.tsx              # Layout raíz
│   ├── index.tsx               # Landing page (/)
│   ├── login.tsx               # /login
│   ├── signup.tsx              # /signup
│   ├── signup-org.tsx          # /signup-org (registro de organización)
│   ├── recover-password.tsx    # /recover-password
│   ├── reset-password.tsx      # /reset-password
│   ├── terminos.tsx            # /terminos
│   ├── privacidad.tsx          # /privacidad
│   ├── dashboard.tsx           # Layout del dashboard
│   └── dashboard/
│       ├── index.tsx           # /dashboard (panel principal)
│       ├── inventory.tsx       # /dashboard/inventory
│       ├── sales.tsx           # /dashboard/sales
│       ├── sales.index.tsx     # /dashboard/sales (index)
│       ├── sales.$saleId.tsx   # /dashboard/sales/:saleId (detalle)
│       ├── customers.tsx       # /dashboard/customers
│       ├── admin.tsx           # /dashboard/admin (solo admin)
│       └── settings.tsx        # /dashboard/settings (solo admin)
│
├── lib/
│   └── utils.ts                # cn(), getInitials() y utilidades
├── routeTree.gen.ts            # Auto-generado por TanStack Router (NO EDITAR)
├── main.tsx                    # Entry point
└── index.css                   # Estilos globales y variables CSS
```

---

## Cliente API Auto-generado

El directorio `src/client/` es generado automáticamente desde el schema OpenAPI del backend. **Nunca edites estos archivos manualmente.**

### Regenerar el cliente

```bash
# El backend debe estar corriendo
cd frontend
bun run generate-client
```

Regenera cuando:
- Agregues o modifiques endpoints del backend
- Cambies schemas de request/response
- Actualices modelos Pydantic

Siempre commitea los archivos generados.

### Uso del cliente con TanStack Query

**Query (lectura):**

```typescript
import { useQuery } from "@tanstack/react-query"
import { ProductsService } from "@/client"

const { data, isLoading } = useQuery({
  queryKey: ["products"],
  queryFn: () => ProductsService.readProducts(),
})
```

**Mutation (escritura):**

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { ProductsService, type ProductCreate } from "@/client"

const queryClient = useQueryClient()

const mutation = useMutation({
  mutationFn: (data: ProductCreate) =>
    ProductsService.createProduct({ requestBody: data }),
  onSuccess: () => showSuccessToast("Producto creado"),
  onError: handleError.bind(showErrorToast),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ["products"] }),
})
```

---

## Routing

Rutas gestionadas con **TanStack Router** en modo file-based. El árbol de rutas se regenera automáticamente en `src/routeTree.gen.ts` al guardar archivos en `src/routes/`.

La protección de rutas se hace mediante el `RoleGuard` y el hook `useAuth`:

```typescript
const { user, organization, hasRole } = useAuth()
if (!hasRole(["admin"])) return <Navigate to="/dashboard" />
```

---

## Formularios

Todos los formularios usan **React Hook Form + Zod**:

```typescript
const formSchema = z.object({
  name: z.string().min(1, "El nombre es obligatorio"),
  price: z.number().positive("El precio debe ser positivo"),
})

const form = useForm<z.infer<typeof formSchema>>({
  resolver: zodResolver(formSchema),
})
```

---

## Componentes UI

El proyecto usa [shadcn/ui](https://ui.shadcn.com/) en `src/components/ui/`. No edites estos archivos directamente. Para personalizar, crea un wrapper en `src/components/Common/`.

Para añadir nuevos componentes de shadcn:

```bash
bunx shadcn@latest add [nombre-del-componente]
```

---

## Modo Oscuro/Claro

El tema se gestiona con `next-themes` a través de `ThemeProvider` en `src/components/theme-provider.tsx`. El usuario puede cambiarlo desde el sidebar con `SidebarAppearance`.

---

## Tests E2E con Playwright

```bash
# Instalar browsers (solo la primera vez)
bunx playwright install

# El backend debe estar corriendo
docker compose up -d --wait backend

# Ejecutar todos los tests
bun run test

# Modo interactivo con UI
bun run test:ui

# Archivo específico
bunx playwright test tests/login.spec.ts

# Tests que coincidan con un patrón
bunx playwright test --grep "login"
```

---

## Variables de Entorno

```env
# frontend/.env o frontend/.env.local
VITE_API_URL=http://localhost:8000
```

Las variables deben tener prefijo `VITE_` para ser expuestas a la aplicación.

---

## Troubleshooting

**Errores de tipos después de cambiar el backend:**
```bash
bun run generate-client
```

**El frontend no conecta al backend:**
- Verifica que el backend corra: http://localhost:8000/docs
- Revisa `VITE_API_URL` en `frontend/.env`
- Comprueba CORS: `BACKEND_CORS_ORIGINS` en `.env` debe incluir `http://localhost:5173`

**Rutas no encontradas:**
- TanStack Router regenera el árbol automáticamente; si no funciona, reinicia `bun run dev`
