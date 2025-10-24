# Arquitectura Técnica del Sistema
## Pecesaurio - Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Versión:** 1.0  
**Fecha:** Octubre 2024

---

## Tabla de Contenidos

1. [Visión General de la Arquitectura](#1-visión-general-de-la-arquitectura)
2. [Arquitectura de Alto Nivel](#2-arquitectura-de-alto-nivel)
3. [Arquitectura del Backend](#3-arquitectura-del-backend)
4. [Arquitectura del Frontend](#4-arquitectura-del-frontend)
5. [Modelo de Datos y Persistencia](#5-modelo-de-datos-y-persistencia)
6. [Seguridad y Autenticación](#6-seguridad-y-autenticación)
7. [Sistema de IA/ML](#7-sistema-de-iaml)
8. [Estrategia de Despliegue](#8-estrategia-de-despliegue)
9. [Flujos Principales](#9-flujos-principales)
10. [Patrones y Principios Arquitectónicos](#10-patrones-y-principios-arquitectónicos)
11. [Consideraciones de Escalabilidad](#11-consideraciones-de-escalabilidad)

---

## 1. Visión General de la Arquitectura

### 1.1 Tipo de Arquitectura

**Arquitectura de N-Capas con Servicios REST**

- **Presentación:** React SPA
- **Lógica de Negocio:** FastAPI Backend
- **Datos:** PostgreSQL + Redis
- **IA/ML:** Módulo de Python independiente

### 1.2 Principios Arquitectónicos

1. **Separación de Responsabilidades:** Frontend, Backend, Base de Datos, ML separados
2. **Stateless:** Backend sin estado (escalable horizontalmente)
3. **API First:** Contrato bien definido entre frontend y backend
4. **Multi-tenancy:** Aislamiento de datos por empresa
5. **Seguridad por Diseño:** Autenticación y autorización en todas las capas
6. **Cloud Native:** Diseñado para ejecutarse en AWS

### 1.3 Decisiones Arquitectónicas Clave

| Decisión | Alternativa | Justificación |
|----------|-------------|---------------|
| SPA (React) | Server-side rendering | Mejor UX, interactividad |
| REST API | GraphQL | Simplicidad, menos curva de aprendizaje |
| PostgreSQL | NoSQL (MongoDB) | Datos relacionales, ACID |
| JWT | Session-based | Stateless, escalable |
| Monolito modular | Microservicios | Apropiado para el alcance |

---

## 2. Arquitectura de Alto Nivel

### 2.1 Diagrama de Componentes Principales

```
                          ┌─────────────────┐
                          │     USUARIOS    │
                          └────────┬────────┘
                                   │ HTTPS
                                   ▼
                    ┌──────────────────────────┐
                    │   Route 53 (DNS)         │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │  CloudFront (CDN)        │
                    └──────┬──────────┬────────┘
                           │          │
                  Static   │          │ API
                  Assets   │          │
                           ▼          ▼
                    ┌──────────┐  ┌──────────────────┐
                    │ S3       │  │ ALB              │
                    │ (React)  │  │ (Load Balancer)  │
                    └──────────┘  └────────┬─────────┘
                                           │
                    ┌──────────────────────┴──────────────────┐
                    │                                          │
                    ▼                                          ▼
         ┌────────────────────┐                   ┌────────────────────┐
         │  Backend App       │                   │  Celery Worker     │
         │  (FastAPI)         │                   │  (Tasks + ML)      │
         │  ECS/EC2           │                   │  ECS/EC2           │
         └────────┬───────────┘                   └──────────┬─────────┘
                  │                                          │
    ┌─────────────┼────────────────────┬────────────────────┤
    │             │                    │                    │
    ▼             ▼                    ▼                    ▼
┌────────┐  ┌──────────┐         ┌─────────┐         ┌──────────┐
│  RDS   │  │ Redis    │         │   S3    │         │CloudWatch│
│(Postgres)│ │(Cache)  │         │(Storage)│         │(Logging) │
└────────┘  └──────────┘         └─────────┘         └──────────┘
```

### 2.2 Flujo de Datos Simplificado

```
Usuario → CloudFront → React App (S3)
          ↓
          Usuario interactúa con UI
          ↓
          React hace llamada API (Axios)
          ↓
          ALB distribuye request
          ↓
          FastAPI Backend recibe request
          ↓
          Valida JWT y permisos
          ↓
          Ejecuta lógica de negocio
          ↓
          Consulta/Modifica PostgreSQL
          ↓
          (Opcional) Consulta cache Redis
          ↓
          Retorna respuesta JSON
          ↓
          React actualiza UI
```

---

## 3. Arquitectura del Backend

### 3.1 Estructura en Capas

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                            │
│  (Endpoints FastAPI - Validación de entrada)            │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 Service Layer                           │
│  (Lógica de negocio - Casos de uso)                     │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│               Data Access Layer                         │
│  (ORM SQLAlchemy - Queries)                             │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  Database                               │
│              (PostgreSQL)                               │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Estructura de Directorios Detallada

```
backend/
├── alembic/                    # Migraciones de BD
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/                    # API Endpoints
│   │   ├── deps.py            # Dependencies (get_db, get_current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py        # POST /login, /register
│   │       ├── users.py       # CRUD /users
│   │       ├── products.py    # CRUD /products
│   │       ├── sales.py       # CRUD /sales
│   │       ├── customers.py   # CRUD /customers
│   │       ├── reports.py     # GET /reports/*
│   │       └── predictions.py # GET /predictions/*
│   │
│   ├── core/                   # Configuración core
│   │   ├── config.py          # Settings (pydantic BaseSettings)
│   │   ├── security.py        # JWT, password hashing
│   │   └── database.py        # Database session
│   │
│   ├── models/                 # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── customer.py
│   │   ├── sale.py
│   │   ├── sale_item.py
│   │   ├── inventory_movement.py
│   │   ├── prediction.py
│   │   └── audit_log.py
│   │
│   ├── schemas/                # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── auth.py            # LoginRequest, TokenResponse
│   │   ├── user.py            # UserCreate, UserRead, UserUpdate
│   │   ├── product.py
│   │   ├── sale.py
│   │   ├── customer.py
│   │   └── common.py          # PaginationParams, etc.
│   │
│   ├── services/               # Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── inventory_service.py
│   │   ├── sales_service.py
│   │   ├── customer_service.py
│   │   ├── report_service.py
│   │   └── prediction_service.py
│   │
│   ├── ml/                     # Machine Learning
│   │   ├── __init__.py
│   │   ├── models/            # Modelos entrenados (pickle)
│   │   ├── data_processor.py  # Preparación de datos
│   │   ├── predictor.py       # Clase Predictor
│   │   ├── trainer.py         # Entrenamiento de modelos
│   │   └── evaluator.py       # Evaluación de modelos
│   │
│   ├── tasks/                  # Celery Tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── ml_tasks.py        # Entrenar modelos, generar predicciones
│   │   └── report_tasks.py    # Generar reportes pesados
│   │
│   ├── utils/                  # Utilidades
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   ├── validators.py
│   │   └── helpers.py
│   │
│   ├── middleware/             # Middlewares
│   │   ├── __init__.py
│   │   ├── tenant_middleware.py
│   │   └── logging_middleware.py
│   │
│   ├── tests/                  # Tests
│   │   ├── unit/
│   │   │   ├── test_services/
│   │   │   └── test_models/
│   │   └── integration/
│   │       └── test_api/
│   │
│   └── main.py                 # FastAPI App
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
└── README.md
```

### 3.3 Flujo de Request Típico

```python
# 1. Request llega al endpoint
@router.post("/products", response_model=ProductRead)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 2. Validación automática por Pydantic
    # 3. Verificación de permisos
    if not current_user.has_permission("products.create"):
        raise HTTPException(403)
    
    # 4. Llamada al servicio
    return await product_service.create_product(
        db, 
        product, 
        current_user.tenant_id
    )

# Service Layer
class ProductService:
    async def create_product(
        self, 
        db: Session, 
        product_data: ProductCreate,
        tenant_id: UUID
    ) -> Product:
        # 5. Lógica de negocio
        # Validar SKU único
        existing = db.query(Product).filter_by(
            tenant_id=tenant_id,
            sku=product_data.sku
        ).first()
        
        if existing:
            raise ProductAlreadyExistsError()
        
        # 6. Crear modelo
        product = Product(
            **product_data.dict(),
            tenant_id=tenant_id
        )
        
        # 7. Guardar en BD
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # 8. Logging/Auditoría
        await audit_log_service.log_action(
            "create", "product", product.id
        )
        
        return product
```

### 3.4 Gestión de Dependencias

```python
# app/api/deps.py

async def get_db() -> Generator:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

def require_role(required_role: str):
    """Dependency to check user role"""
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role.name != required_role:
            raise HTTPException(403, "Insufficient permissions")
        return current_user
    return role_checker
```

---

## 4. Arquitectura del Frontend

### 4.1 Estructura de Capas

```
┌─────────────────────────────────────────────────────────┐
│              Presentation Layer                         │
│  (Pages, Components, UI)                                │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              State Management                           │
│  (Zustand stores, React Query cache)                    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│               API Layer                                 │
│  (Axios client, API functions)                          │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
                  Backend API
```

### 4.2 Estructura de Directorios Detallada

```
frontend/
├── public/
│   ├── favicon.ico
│   └── robots.txt
│
├── src/
│   ├── api/                    # API Client
│   │   ├── client.ts          # Axios instance configured
│   │   ├── auth.api.ts
│   │   ├── products.api.ts
│   │   ├── sales.api.ts
│   │   ├── customers.api.ts
│   │   └── reports.api.ts
│   │
│   ├── components/             # Componentes reutilizables
│   │   ├── ui/                # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   ├── forms/
│   │   │   ├── ProductForm.tsx
│   │   │   ├── SaleForm.tsx
│   │   │   └── CustomerForm.tsx
│   │   ├── tables/
│   │   │   ├── DataTable.tsx
│   │   │   ├── ProductsTable.tsx
│   │   │   └── SalesTable.tsx
│   │   ├── charts/
│   │   │   ├── SalesChart.tsx
│   │   │   ├── PredictionChart.tsx
│   │   │   └── StockChart.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── Footer.tsx
│   │
│   ├── features/               # Features organizados por módulo
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useAuth.ts
│   │   │   └── store/
│   │   │       └── authStore.ts
│   │   │
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   │   ├── KPICard.tsx
│   │   │   │   └── RecentSales.tsx
│   │   │   └── hooks/
│   │   │       └── useDashboard.ts
│   │   │
│   │   ├── inventory/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   │   ├── useProducts.ts
│   │   │   │   └── useCategories.ts
│   │   │   └── pages/
│   │   │       ├── ProductsPage.tsx
│   │   │       └── ProductDetailPage.tsx
│   │   │
│   │   ├── sales/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── pages/
│   │   │
│   │   ├── customers/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── pages/
│   │   │
│   │   └── predictions/
│   │       ├── components/
│   │       ├── hooks/
│   │       └── pages/
│   │
│   ├── hooks/                  # Custom hooks globales
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   └── usePagination.ts
│   │
│   ├── layouts/                # Layout components
│   │   ├── MainLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── DashboardLayout.tsx
│   │
│   ├── lib/                    # Utilities y helpers
│   │   ├── utils.ts
│   │   ├── formatters.ts
│   │   └── constants.ts
│   │
│   ├── pages/                  # Page components (routing)
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ProductsPage.tsx
│   │   ├── SalesPage.tsx
│   │   └── NotFoundPage.tsx
│   │
│   ├── routes/                 # Router configuration
│   │   ├── index.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── routes.config.ts
│   │
│   ├── stores/                 # Zustand stores
│   │   ├── authStore.ts
│   │   ├── uiStore.ts
│   │   └── cartStore.ts
│   │
│   ├── types/                  # TypeScript types
│   │   ├── api.types.ts
│   │   ├── models.types.ts
│   │   └── common.types.ts
│   │
│   ├── App.tsx                 # App component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
│
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── README.md
```

### 4.3 Flujo de Estado

```typescript
// 1. Usuario interactúa con UI
<Button onClick={handleCreateProduct}>Crear Producto</Button>

// 2. Handler llama a React Query mutation
const createProductMutation = useMutation({
  mutationFn: (product: ProductCreate) => 
    productsApi.createProduct(product),
  onSuccess: () => {
    // 3. Invalidar cache y refetch
    queryClient.invalidateQueries(['products']);
    toast.success('Producto creado');
  },
  onError: (error) => {
    toast.error('Error al crear producto');
  }
});

// 4. API function hace llamada HTTP
export const productsApi = {
  createProduct: async (product: ProductCreate) => {
    const response = await apiClient.post<Product>(
      '/api/v1/products',
      product
    );
    return response.data;
  }
};

// 5. Axios interceptor añade JWT
apiClient.interceptors.request.use((config) => {
  const token = authStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 4.4 Gestión de Autenticación

```typescript
// stores/authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  
  login: async (email, password) => {
    const response = await authApi.login({ email, password });
    localStorage.setItem('token', response.token);
    set({
      user: response.user,
      token: response.token,
      isAuthenticated: true
    });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    set({
      user: null,
      token: null,
      isAuthenticated: false
    });
  },
  
  refreshUser: async () => {
    const user = await authApi.getCurrentUser();
    set({ user });
  }
}));
```

---

## 5. Modelo de Datos y Persistencia

### 5.1 Estrategia de Persistencia

```
┌───────────────────────────────────────────────────────┐
│              Application Layer                        │
└────────────────────┬──────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌─────────┐
│  PostgreSQL  │ │  Redis   │ │   S3    │
│  (Primary)   │ │  (Cache) │ │ (Files) │
└──────────────┘ └──────────┘ └─────────┘
```

**PostgreSQL:**
- Datos transaccionales
- Relaciones complejas
- ACID compliance

**Redis:**
- Session storage
- Cache de queries frecuentes
- Rate limiting
- Celery broker

**S3:**
- Imágenes de productos
- PDFs de facturas
- Reportes generados
- Backups

### 5.2 Patrón Repository (Opcional)

```python
# repositories/product_repository.py
class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, product_id: UUID, tenant_id: UUID) -> Product:
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id
        ).first()
    
    def get_all(
        self, 
        tenant_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        return self.db.query(Product).filter(
            Product.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()
    
    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
```

---

## 6. Seguridad y Autenticación

### 6.1 Flujo de Autenticación JWT

```
┌──────────┐                                ┌──────────┐
│  Client  │                                │  Server  │
└────┬─────┘                                └────┬─────┘
     │                                           │
     │  1. POST /auth/login                      │
     │   { email, password }                     │
     ├──────────────────────────────────────────►│
     │                                           │
     │                                  2. Validar credenciales
     │                                     Hash password
     │                                           │
     │  3. Response                              │
     │   { token: "JWT", user: {...} }           │
     │◄──────────────────────────────────────────┤
     │                                           │
4. Guardar token                                 │
   localStorage                                  │
     │                                           │
     │  5. GET /api/v1/products                  │
     │   Headers: Authorization: Bearer JWT      │
     ├──────────────────────────────────────────►│
     │                                           │
     │                                  6. Validar JWT
     │                                     Extraer user_id
     │                                     Verificar permisos
     │                                           │
     │  7. Response                              │
     │   { products: [...] }                     │
     │◄──────────────────────────────────────────┤
     │                                           │
```

### 6.2 Middleware de Seguridad

```python
# middleware/tenant_middleware.py

@app.middleware("http")
async def tenant_isolation_middleware(request: Request, call_next):
    """Ensure all requests are scoped to tenant"""
    
    # Skip for auth endpoints
    if request.url.path.startswith("/auth"):
        return await call_next(request)
    
    # Get current user from token
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = await get_user_from_token(token)
    
    if not user:
        return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    
    # Set tenant context
    request.state.tenant_id = user.tenant_id
    request.state.user = user
    
    response = await call_next(request)
    return response
```

### 6.3 Control de Acceso Basado en Roles (RBAC)

```python
# Decorador para verificar permisos
def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(401)
            
            # Verificar permiso
            if not has_permission(current_user, permission):
                raise HTTPException(403, "Insufficient permissions")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso
@router.delete("/products/{product_id}")
@require_permission("products.delete")
async def delete_product(
    product_id: UUID,
    current_user: User = Depends(get_current_user)
):
    ...
```

---

## 7. Sistema de IA/ML

### 7.1 Arquitectura del Módulo de IA

```
┌─────────────────────────────────────────────────────┐
│              Prediction Request                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│          Prediction Service                         │
│  (Orchestrates prediction workflow)                 │
└───────────┬───────────────────────┬─────────────────┘
            │                       │
            ▼                       ▼
┌──────────────────┐     ┌──────────────────────┐
│  Data Processor  │     │   Model Manager      │
│  (Fetch & Clean) │     │ (Load trained model) │
└────────┬─────────┘     └──────────┬───────────┘
         │                          │
         │                          │
         └──────────┬───────────────┘
                    ▼
        ┌────────────────────────┐
        │    Predictor           │
        │  (Generate forecast)   │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Save to Database      │
        │  Return predictions    │
        └────────────────────────┘
```

### 7.2 Pipeline de Entrenamiento

```python
# ml/trainer.py

class DemandForecastTrainer:
    def __init__(self):
        self.model = None
    
    async def train(self, tenant_id: UUID, product_id: UUID):
        """Train demand forecast model for a product"""
        
        # 1. Fetch historical data
        sales_data = await self._fetch_sales_history(
            tenant_id, 
            product_id
        )
        
        # 2. Preprocess data
        df = self._preprocess_data(sales_data)
        
        # 3. Feature engineering
        df = self._create_features(df)
        
        # 4. Train model (Prophet)
        from prophet import Prophet
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        model.fit(df)
        
        # 5. Evaluate model
        metrics = self._evaluate_model(model, df)
        
        # 6. Save model
        model_path = self._save_model(
            model, 
            tenant_id, 
            product_id
        )
        
        return {
            "model_path": model_path,
            "metrics": metrics
        }
    
    def _preprocess_data(self, sales_data):
        """Convert to Prophet format"""
        df = pd.DataFrame(sales_data)
        df = df.rename(columns={"date": "ds", "quantity": "y"})
        df["ds"] = pd.to_datetime(df["ds"])
        return df[["ds", "y"]]
```

### 7.3 Pipeline de Predicción

```python
# ml/predictor.py

class DemandPredictor:
    def __init__(self):
        self.models_cache = {}
    
    async def predict(
        self, 
        tenant_id: UUID, 
        product_id: UUID,
        periods: int = 30
    ):
        """Generate demand forecast"""
        
        # 1. Load model (with caching)
        model = self._load_model(tenant_id, product_id)
        
        if not model:
            # Train if not exists
            trainer = DemandForecastTrainer()
            await trainer.train(tenant_id, product_id)
            model = self._load_model(tenant_id, product_id)
        
        # 2. Generate future dates
        future = model.make_future_dataframe(periods=periods)
        
        # 3. Predict
        forecast = model.predict(future)
        
        # 4. Extract predictions
        predictions = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        predictions = predictions.tail(periods)
        
        # 5. Calculate confidence
        confidence = self._calculate_confidence(forecast)
        
        # 6. Format results
        results = []
        for _, row in predictions.iterrows():
            results.append({
                "date": row["ds"].date(),
                "predicted_quantity": max(0, row["yhat"]),
                "confidence_score": confidence,
                "lower_bound": max(0, row["yhat_lower"]),
                "upper_bound": row["yhat_upper"]
            })
        
        return results
```

### 7.4 Tarea Celery para Predicciones Periódicas

```python
# tasks/ml_tasks.py

@celery_app.task
def generate_daily_predictions():
    """
    Celery task to generate predictions for all active products
    Runs daily at midnight
    """
    
    # Get all tenants
    tenants = db.query(Tenant).filter(
        Tenant.subscription_status == 'active'
    ).all()
    
    for tenant in tenants:
        # Get products with sufficient history
        products = db.query(Product).filter(
            Product.tenant_id == tenant.id,
            Product.is_active == True
        ).all()
        
        for product in products:
            # Check if has enough data (30+ days)
            sales_count = db.query(func.count(Sale.id)).filter(
                Sale.tenant_id == tenant.id,
                # Join with sale_items for product
            ).scalar()
            
            if sales_count >= 10:
                # Generate predictions
                predictor = DemandPredictor()
                predictions = await predictor.predict(
                    tenant.id,
                    product.id,
                    periods=7  # Next 7 days
                )
                
                # Save to database
                for pred in predictions:
                    db.add(Prediction(
                        tenant_id=tenant.id,
                        product_id=product.id,
                        **pred
                    ))
                
                db.commit()
    
    return {"status": "completed"}
```

---

## 8. Estrategia de Despliegue

### 8.1 Ambientes

```
┌─────────────────────────────────────────────────────┐
│  Development (Local)                                │
│  - docker-compose                                   │
│  - Datos de prueba                                  │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Staging (AWS)                                      │
│  - Ambiente de pruebas                              │
│  - Deploy automático desde 'develop' branch         │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Production (AWS)                                   │
│  - Deploy manual desde 'main' branch                │
│  - Monitoreo activo                                 │
└─────────────────────────────────────────────────────┘
```

### 8.2 Docker Compose para Desarrollo Local

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: pecesaurio
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - postgres
      - redis

  celery-worker:
    build: ./backend
    command: celery -A app.tasks.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    env_file:
      - ./backend/.env
    depends_on:
      - postgres
      - redis

  celery-beat:
    build: ./backend
    command: celery -A app.tasks.celery_app beat --loglevel=info
    volumes:
      - ./backend:/app
    env_file:
      - ./backend/.env
    depends_on:
      - redis

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000

volumes:
  postgres_data:
```

### 8.3 Dockerfile Backend

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.4 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml

name: Deploy to AWS

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Test frontend
        run: |
          cd frontend
          npm ci
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build and push Docker image
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker build -t pecesaurio-backend ./backend
          docker tag pecesaurio-backend:latest $ECR_REGISTRY/pecesaurio-backend:latest
          docker push $ECR_REGISTRY/pecesaurio-backend:latest
      
      - name: Deploy frontend to S3
        run: |
          cd frontend
          npm ci
          npm run build
          aws s3 sync dist/ s3://pecesaurio-frontend --delete
          aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_ID --paths "/*"
      
      - name: Update ECS service
        run: |
          aws ecs update-service --cluster pecesaurio-cluster --service backend --force-new-deployment
```

---

## 9. Flujos Principales

### 9.1 Flujo: Crear una Venta

```
[Usuario] → [Frontend: SaleForm]
              ↓
         Selecciona productos
         Ingresa cantidades
         Selecciona cliente (opcional)
              ↓
         Click "Crear Venta"
              ↓
[Frontend: useMutation] → POST /api/v1/sales
              ↓
[Backend: sales.py endpoint]
              ↓
         Valida JWT
         Verifica permisos
              ↓
[SalesService.create_sale()]
              ↓
    1. Verificar stock disponible
    2. Calcular totales
    3. Crear registro Sale
    4. Crear registros SaleItem
    5. Trigger: Actualizar stock (automático)
    6. Trigger: Registrar inventory_movements
    7. Trigger: Actualizar stats de customer
    8. Commit transaction
    9. Generar número de factura
   10. Log de auditoría
              ↓
         Return Sale object
              ↓
[Frontend] ← Response
              ↓
    Invalidar cache de productos
    Invalidar cache de ventas
    Mostrar toast de éxito
    Navegar a detalle de venta
```

### 9.2 Flujo: Generar Predicción de Demanda

```
[Celery Beat] → Trigger diario a medianoche
              ↓
[Task: generate_daily_predictions]
              ↓
    Para cada tenant activo:
      Para cada producto con histórico:
              ↓
[DemandPredictor.predict()]
              ↓
    1. Cargar modelo entrenado (Prophet)
    2. Si no existe → entrenar modelo
    3. Generar predicciones (7-30 días)
    4. Calcular confidence score
    5. Guardar en tabla predictions
              ↓
[Frontend] Usuario accede a /predictions
              ↓
[Backend: GET /api/v1/predictions]
              ↓
    Query predictions de últimas 24h
    Join con products
    Return JSON
              ↓
[Frontend] Renderiza gráficos y tabla
```

---

## 10. Patrones y Principios Arquitectónicos

### 10.1 Principios SOLID

- **S - Single Responsibility:** Cada clase/módulo tiene una responsabilidad
- **O - Open/Closed:** Extendible sin modificar código existente
- **L - Liskov Substitution:** Subtipos deben ser sustituibles
- **I - Interface Segregation:** Interfaces específicas, no genéricas
- **D - Dependency Inversion:** Depender de abstracciones, no concreciones

### 10.2 Patrones Implementados

#### Repository Pattern
```python
class BaseRepository:
    def get_all(self): pass
    def get_by_id(self, id): pass
    def create(self, entity): pass
    def update(self, entity): pass
    def delete(self, id): pass
```

#### Service Layer Pattern
```python
# Lógica de negocio encapsulada en servicios
class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo
    
    def create_product(self, data):
        # Business logic here
        pass
```

#### Dependency Injection
```python
# FastAPI Depends
async def get_product_service(
    db: Session = Depends(get_db)
) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)
```

### 10.3 Principios Adicionales

#### DRY (Don't Repeat Yourself)
- Utilidades compartidas en `utils/`
- Componentes reutilizables en frontend

#### KISS (Keep It Simple, Stupid)
- Soluciones simples sobre complejas
- Evitar over-engineering

#### YAGNI (You Aren't Gonna Need It)
- No implementar features no requeridas
- Enfoque en MVP

---

## 11. Consideraciones de Escalabilidad

### 11.1 Escalamiento Horizontal vs Vertical

**Vertical (Corto plazo):**
- Aumentar CPU/RAM de instancias
- Más fácil de implementar

**Horizontal (Largo plazo):**
- Múltiples instancias de backend
- Load balancer distribuyendo carga
- Read replicas de BD

### 11.2 Optimizaciones de Performance

#### Cacheo Estratégico
```python
# Cache en Redis
@cache(expire=3600, key_prefix="products")
async def get_products_cached(tenant_id: UUID):
    return await get_products(tenant_id)
```

#### Queries Optimizadas
```python
# Eager loading para evitar N+1
products = db.query(Product).options(
    joinedload(Product.category),
    joinedload(Product.tenant)
).all()
```

#### Paginación
```python
# Siempre paginar listas
@router.get("/products")
async def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
```

#### CDN para Assets Estáticos
- CloudFront para frontend
- Imágenes servidas desde S3 + CloudFront

### 11.3 Monitoreo y Alertas

**Métricas Clave:**
- Latencia de endpoints (p50, p95, p99)
- Tasa de errores (5xx)
- Uso de CPU/RAM
- Conexiones de BD
- Tamaño de cola Celery

**Herramientas:**
- CloudWatch para infraestructura
- Sentry para errores de aplicación
- Logs estructurados con contexto

---

## Conclusión

Esta arquitectura proporciona:

✅ **Separación de responsabilidades** clara entre capas  
✅ **Escalabilidad** mediante diseño stateless y cacheo  
✅ **Seguridad** con autenticación JWT y multi-tenancy  
✅ **Mantenibilidad** con estructura modular y documentada  
✅ **Testabilidad** con dependency injection  
✅ **Observabilidad** con logging y monitoreo  

El diseño es apropiado para el MVP y puede evolucionar hacia microservicios si el crecimiento lo requiere.

---

**Elaborado por:** Equipo Pecesaurio  
**Fecha:** Octubre 2024  
**Versión:** 1.0

