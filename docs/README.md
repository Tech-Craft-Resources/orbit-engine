# Documentación del Proyecto OrbitEngine
## Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Equipo:** 3 Integrantes  
**Período:** Noviembre 2025 - Abril 2026

---

## 📋 Índice de Documentos

### 1. [Propuesta de Proyecto](./propuesta.md)
Documento inicial con el planteamiento del problema, objetivos e hipótesis del proyecto de grado.

### 2. [Alcance del Proyecto y MVP](./01-alcance-mvp.md)
Define el alcance completo del proyecto, la definición del MVP (Minimum Viable Product), módulos incluidos y excluidos, y métricas de éxito.

**Contenido destacado:**
- ✅ Definición clara del MVP
- ✅ Priorización de funcionalidades (Prioridad 1, 2, 3)
- ✅ Módulos adicionales post-MVP
- ✅ Métricas técnicas y de producto
- ✅ Riesgos y mitigación

### 3. [Historias de Usuario y Requisitos](./02-requisitos.md)
Especificación detallada de historias de usuario, requisitos funcionales y no funcionales del sistema.

**Contenido destacado:**
- 👥 Personas (usuarios tipo)
- 📖 27 Historias de Usuario detalladas con criterios de aceptación
- ⚙️ Requisitos funcionales por módulo
- 🔒 Requisitos no funcionales (rendimiento, seguridad, usabilidad)
- ✅ Reglas de negocio y validaciones

### 4. [Cronograma de Desarrollo](./03-cronograma.md)
Planificación temporal completa desde noviembre 2024 hasta abril 2025.

**Contenido destacado:**
- 📅 6 fases de desarrollo
- 🏃 12 sprints de 2 semanas cada uno
- 📊 Distribución de historias de usuario por sprint
- 🎯 Hitos principales (milestones)
- 👥 Roles y responsabilidades del equipo
- ⚠️ Gestión de riesgos y buffers

### 5. [Stack Tecnológico](./04-stack-tecnologico.md)
Propuesta completa del stack tecnológico con justificaciones.

**Contenido destacado:**
- 💻 **Frontend:** React 18 + TypeScript, Vite, Tailwind CSS, shadcn/ui
- ⚙️ **Backend:** Python 3.11 + FastAPI, SQLAlchemy, Pydantic
- 🗄️ **Base de Datos:** PostgreSQL + Redis
- 🤖 **IA/ML:** scikit-learn, Prophet, pandas
- ☁️ **Cloud:** AWS (EC2/ECS, RDS, S3, CloudFront)
- 🔄 **DevOps:** Docker, GitHub Actions, Celery
- 📊 Comparativas y justificaciones de decisiones
- 💰 Estimación de costos AWS (~$40/mes)

### 6. [Diseño de Base de Datos](./05-base-de-datos.md)
Modelo de datos completo con todas las tablas, relaciones e índices.

**Contenido destacado:**
- 📐 Diagrama Entidad-Relación
- 📊 11 tablas principales detalladas
- 🔐 Estrategia de multi-tenancy
- ⚡ Índices y optimizaciones
- 🔄 Triggers importantes
- 💾 Estrategia de backups
- 📈 Consideraciones de escalabilidad
- 📝 Queries comunes optimizadas

### 7. [Arquitectura Técnica](./06-arquitectura-tecnica.md)
Diseño arquitectónico completo del sistema con diagramas y patrones.

**Contenido destacado:**
- 🏗️ Arquitectura de alto nivel (diagrama de componentes)
- 🔧 Arquitectura del backend (capas, estructura de directorios)
- 🎨 Arquitectura del frontend (estructura, gestión de estado)
- 🔐 Seguridad y autenticación (flujo JWT, RBAC)
- 🤖 Sistema de IA/ML (pipelines de entrenamiento y predicción)
- 🚀 Estrategia de despliegue (Docker, CI/CD)
- 🔄 Flujos principales del sistema
- 📐 Patrones arquitectónicos (Repository, Service Layer, DI)
- 📈 Consideraciones de escalabilidad

---

## 🎯 Resumen Ejecutivo del Proyecto

### ¿Qué es OrbitEngine?

Una plataforma SaaS accesible y modular que permite a las pequeñas y medianas empresas (pymes) gestionar de manera centralizada sus procesos internos de **inventario, ventas, clientes y reportes**, incorporando **Inteligencia Artificial** para predicción de demanda y análisis predictivo.

### Problema que Resuelve

Las pymes enfrentan una brecha tecnológica considerable, gestionando sus procesos mediante métodos manuales (hojas de cálculo, mensajería), lo que produce:
- ❌ Duplicidad y pérdida de información
- ❌ Errores frecuentes en inventarios
- ❌ Escasa trazabilidad
- ❌ Sobrecarga administrativa

### Solución Propuesta

✅ Plataforma web intuitiva y responsive  
✅ Gestión centralizada de inventario, ventas y clientes  
✅ Dashboard con métricas en tiempo real  
✅ Predicción de demanda con IA  
✅ Recomendaciones inteligentes de reabastecimiento  
✅ Reportes exportables y análisis  

### MVP (Alcance Inicial)

**Módulos Críticos:**
1. ✅ Autenticación y gestión de usuarios con roles
2. ✅ Gestión de inventario (CRUD productos, alertas de stock)
3. ✅ Gestión de ventas (registro, historial, facturación)
4. ✅ Gestión de clientes (CRUD, historial de compras)
5. ✅ Dashboard y reportes básicos
6. ✅ Predicción de demanda con IA (simplificado)

### Stack Tecnológico

```
Frontend:  React + TypeScript + Tailwind CSS
Backend:   Python + FastAPI + PostgreSQL
Cloud:     AWS (EC2, RDS, S3, CloudFront)
IA/ML:     Prophet + scikit-learn
```

### Timeline

- **Inicio:** Noviembre 2025
- **Desarrollo:** 16 semanas (8 sprints)
- **Validación:** 4 semanas con pymes reales
- **Entrega:** Abril 2026

### Equipo

- **3 integrantes:** Backend Lead, Frontend Lead, DevOps & Full Stack
- **15-20 horas/semana** por integrante
- **Metodología:** Scrum adaptado (sprints de 2 semanas)

---

## 📊 Métricas de Éxito

### Técnicas
- ⚡ Tiempo de respuesta < 500ms
- 🧪 Cobertura de tests > 60%
- ⏰ Disponibilidad > 95%

### Producto
- 👥 2+ pymes usando el sistema
- 😊 Satisfacción de usuario > 4/5
- 🎯 Precisión de IA > 70%

### Académicas
- ✅ Validación empírica de hipótesis
- 📉 Reducción de tiempo en tareas administrativas > 30%
- 📊 Reducción de errores en inventario > 40%

---

## 🚀 Próximos Pasos

### Fase 1: Setup Inicial (Noviembre)
1. Configurar repositorios GitHub
2. Setup de infraestructura AWS
3. Crear estructura de proyecto (backend + frontend)
4. Configurar CI/CD básico
5. Sprint Planning - Sprint 1

### Sprint 1: Autenticación (Diciembre)
1. Implementar modelos de Usuario y Roles
2. Endpoints de login/register
3. Generación y validación de JWT
4. UI de login y registro
5. Tests de autenticación

---

## 📚 Cómo Usar Esta Documentación

1. **Empezar por:** [Propuesta](./propuesta.md) para entender el contexto
2. **Luego:** [Alcance y MVP](./01-alcance-mvp.md) para ver qué se va a construir
3. **Después:** [Requisitos](./02-requisitos.md) para detalles funcionales
4. **Para planificación:** [Cronograma](./03-cronograma.md)
5. **Para implementación:** [Stack Tecnológico](./04-stack-tecnologico.md), [Base de Datos](./05-base-de-datos.md), [Arquitectura](./06-arquitectura-tecnica.md)

---

## 🔄 Control de Versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | Nov 2025 | Versión inicial completa de documentación |

---

## 👥 Contacto

**Proyecto:** OrbitEngine  
**Universidad:** [Tu Universidad]  
**Asesor:** [Nombre del asesor]  
**Equipo:** [Nombres de los integrantes]

---

**Fecha de Elaboración:** Noviembre 2025  
**Última Actualización:** Noviembre 2025

