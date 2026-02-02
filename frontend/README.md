# FastAPI Project - Frontend

Frontend built with [Vite](https://vitejs.dev/), [React](https://reactjs.org/), [TypeScript](https://www.typescriptlang.org/), [TanStack Query](https://tanstack.com/query), [TanStack Router](https://tanstack.com/router), and [Tailwind CSS](https://tailwindcss.com/).

## Requirements

- [Bun](https://bun.sh/) (recommended) or [Node.js](https://nodejs.org/)
- Backend running (either in Docker or locally)

## Development Workflow (Recommended)

For the best frontend development experience, **stop the Docker frontend container** and run Bun locally:

```bash
# 1. Stop the frontend container (from project root)
docker compose stop frontend

# 2. Go to frontend directory
cd frontend

# 3. Install dependencies (first time only)
bun install

# 4. Start development server
bun run dev
```

The frontend will be available at http://localhost:5173/

**Benefits of local development:**
- ⚡ Instant hot-reload
- 🔥 Better performance
- 🐛 Better debugging experience
- 🎯 Direct access to source maps

The frontend will automatically connect to the backend running in Docker at `http://localhost:8000`.

## Running in Docker

If you prefer to run everything in Docker:

```bash
# From project root
docker compose up frontend -d
```

Frontend will be available at http://localhost:5173/

**Note:** The Docker setup builds for production, so hot-reload is not as fast as local development.

## Available Scripts

```bash
# Development server with hot-reload
bun run dev

# Type checking
bun run type-check

# Linting and auto-fix
bun run lint

# Build for production
bun run build

# Preview production build
bun run preview

# Generate API client from OpenAPI schema
bun run generate-client

# Run E2E tests with Playwright
bun run test

# Run tests with UI
bun run test:ui
```

## Generate API Client

The frontend uses an auto-generated TypeScript client based on the backend's OpenAPI schema. **Never edit files in `src/client/` manually** - they are auto-generated.

### Automatic generation (recommended):

```bash
# From project root, with backend running
bash ./scripts/generate-client.sh
```

### Manual generation:

```bash
# 1. Make sure backend is running in Docker
docker compose up backend -d

# 2. Go to frontend directory
cd frontend

# 3. Generate client
bun run generate-client
```

**When to regenerate:**
- After adding/modifying backend API endpoints
- After changing request/response schemas
- After updating Pydantic models

Always commit the generated client files to git.

## How the API Client Works

The frontend uses a **type-safe auto-generated API client** created from the backend's OpenAPI specification. This ensures that frontend and backend are always in sync.

### Architecture:

```
Backend (FastAPI)
    ↓ exposes
OpenAPI Schema (JSON)
    ↓ generates
TypeScript Client (src/client/)
    ↓ used by
React Components + TanStack Query
```

### Generated Files Structure:

```
src/client/
├── index.ts           # Main exports
├── types.gen.ts       # TypeScript types from Pydantic schemas
├── schemas.gen.ts     # Zod schemas for validation
├── sdk.gen.ts         # API service methods
└── core/              # HTTP client internals
    ├── OpenAPI.ts
    ├── request.ts
    └── ...
```

### Using the API Client:

#### 1. Import Services

Each API router in the backend generates a corresponding service:

```typescript
import { UsersService, ItemsService, LoginService } from "@/client"
```

#### 2. Available Services:

Based on your backend structure:
- `LoginService` - Authentication endpoints
- `UsersService` - User management (CRUD)
- `UtilsService` - Utility endpoints (health check, etc.)

#### 3. Making API Calls with TanStack Query:

**Fetch data (Query):**

```typescript
import { useQuery } from "@tanstack/react-query"
import { UsersService } from "@/client"

function UsersList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["users"], // Cache key
    queryFn: () => UsersService.readUsers(), // API call
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data?.data.map((user) => (
        <li key={user.id}>{user.email}</li>
      ))}
    </ul>
  )
}
```

**Create/Update data (Mutation):**

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { UsersService, type UserCreate } from "@/client"

function CreateUserForm() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    // API call to create user
    mutationFn: (data: UserCreate) => 
      UsersService.createUser({ requestBody: data }),
    
    // On success: invalidate cache and refetch
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
      showToast("User created successfully")
    },
    
    // On error: show error message
    onError: (error) => {
      showToast(`Error: ${error.message}`)
    },
  })

  const handleSubmit = (formData: UserCreate) => {
    mutation.mutate(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  )
}
```

**Update with optimistic UI:**

```typescript
const updateMutation = useMutation({
  mutationFn: (data: { id: string; body: UserUpdate }) =>
    UsersService.updateUser({ 
      userId: data.id, 
      requestBody: data.body 
    }),
  
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["users"] })
  },
})
```

**Delete:**

```typescript
const deleteMutation = useMutation({
  mutationFn: (userId: string) => 
    UsersService.deleteUser({ userId }),
  
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["users"] })
  },
})
```

#### 4. TypeScript Types:

All Pydantic models from the backend are available as TypeScript types:

```typescript
import type { 
  UserPublic,      // Response type
  UserCreate,      // Create request
  UserUpdate,      // Update request
  UsersPublic,     // Paginated list response
} from "@/client"

// Use in component props
interface UserCardProps {
  user: UserPublic
}

// Use in forms
const [formData, setFormData] = useState<UserCreate>({
  email: "",
  password: "",
  full_name: "",
})
```

#### 5. Error Handling:

```typescript
import { ApiError } from "@/client"

try {
  const result = await UsersService.createUser({ requestBody: data })
} catch (error) {
  if (error instanceof ApiError) {
    console.error("API Error:", error.status, error.body)
    // error.status: HTTP status code (400, 404, 500, etc.)
    // error.body: Error response from backend
  }
}
```

Or with TanStack Query:

```typescript
const { error } = useQuery({
  queryKey: ["users"],
  queryFn: () => UsersService.readUsers(),
  onError: (error) => {
    if (error instanceof ApiError) {
      // Handle specific status codes
      if (error.status === 401) {
        // Redirect to login
      }
    }
  },
})
```

#### 6. Authentication:

The client automatically includes authentication tokens from cookies/localStorage:

```typescript
// Login sets the token
const { data } = await LoginService.loginAccessToken({
  formData: { username, password }
})

// Subsequent requests automatically include the token
const users = await UsersService.readUsers() // Token included automatically
```

The token is stored and managed by the `useAuth` hook in `src/hooks/useAuth.ts`.

#### 7. Query Keys Convention:

Use consistent query keys for cache management:

```typescript
// List queries
["users"]
["items"]
["items", { skip: 0, limit: 50 }] // with params

// Detail queries
["users", userId]
["items", itemId]

// Nested/related queries
["users", userId, "items"]
```

#### 8. Common Patterns:

**Paginated Lists:**

```typescript
const { data } = useQuery({
  queryKey: ["items", { skip, limit }],
  queryFn: () => ItemsService.readItems({ skip, limit }),
})

// data.data: array of items
// data.count: total count
```

**Dependent Queries:**

```typescript
// Only fetch user's items after user is loaded
const { data: user } = useQuery({
  queryKey: ["users", userId],
  queryFn: () => UsersService.readUser({ userId }),
})

const { data: items } = useQuery({
  queryKey: ["users", userId, "items"],
  queryFn: () => ItemsService.readItems({ ownerId: userId }),
  enabled: !!user, // Only run if user exists
})
```

### Best Practices:

1. ✅ **Always use TanStack Query** for API calls (not raw fetch/axios)
2. ✅ **Invalidate queries** after mutations to refresh data
3. ✅ **Use TypeScript types** from the client for type safety
4. ✅ **Regenerate client** after backend changes
5. ✅ **Commit generated client** files to git
6. ❌ **Never edit** files in `src/client/` manually
7. ❌ **Never use** different HTTP clients (fetch, axios) alongside the generated client

### Troubleshooting:

**Type errors after backend changes:**
```bash
# Regenerate the client
bun run generate-client
```

**404 errors on API calls:**
- Check backend is running: http://localhost:8000/docs
- Verify `VITE_API_URL` in `.env`
- Check backend logs: `docker compose logs -f backend`

**CORS errors:**
- Ensure `BACKEND_CORS_ORIGINS` in `.env` includes `http://localhost:5173`
- Restart backend after changing CORS settings

## Code Structure

```
frontend/src/
├── client/          # 🚫 Auto-generated API client (DO NOT EDIT)
├── components/
│   ├── Admin/       # Admin-specific components
│   ├── Common/      # Shared components
│   ├── Pending/     # Pending users management
│   ├── Sidebar/     # Sidebar navigation
│   ├── ui/          # 🚫 shadcn/ui components (DO NOT EDIT)
│   └── UserSettings/ # User settings components
├── hooks/           # Custom React hooks
│   ├── useAuth.ts
│   ├── useCopyToClipboard.ts
│   ├── useCustomToast.ts
│   └── useMobile.ts
├── routes/          # TanStack Router pages (file-based routing)
│   ├── _layout/     # Layout routes
│   ├── __root.tsx   # Root layout
│   ├── login.tsx
│   └── ...
├── lib/
│   └── utils.ts     # Utility functions
├── index.css        # Global styles
├── main.tsx         # App entry point
└── routeTree.gen.ts # 🚫 Auto-generated routes (DO NOT EDIT)
```

## End-to-End Testing with Playwright

The project includes E2E tests using Playwright.

### Setup:

```bash
# Install Playwright browsers (first time only)
bunx playwright install
```

### Run tests:

```bash
# Make sure backend is running
docker compose up -d --wait backend

# Run all tests
bun run test

# Run tests with UI (interactive mode)
bun run test:ui

# Run specific test file
bunx playwright test tests/login.spec.ts

# Run tests matching a pattern
bunx playwright test --grep "create item"
```

### Clean up after tests:

```bash
# Stop containers and remove test data
docker compose down -v
```

### Test files:

- `tests/*.spec.ts` - Test specifications
- `tests/utils/` - Test utilities and helpers
- `tests/config.ts` - Test configuration
- `playwright.config.ts` - Playwright configuration

For more information, see the [Playwright documentation](https://playwright.dev/docs/intro).

## Using a Remote API

To use a remote backend instead of localhost, set the `VITE_API_URL` environment variable:

```env
# frontend/.env
VITE_API_URL=https://api.example.com
```

Or set it when running:

```bash
VITE_API_URL=https://api.example.com bun run dev
```

## shadcn/ui Components

The project uses [shadcn/ui](https://ui.shadcn.com/) components in `src/components/ui/`.

**Important:** These components are managed by shadcn and should not be edited directly. If you need to customize them:

1. Create a wrapper component in `src/components/Common/`
2. Import and extend the ui component there
3. Use your wrapper throughout the app

To add new shadcn components:

```bash
bunx shadcn@latest add [component-name]
```

## Environment Variables

```env
# .env or .env.local
VITE_API_URL=http://localhost:8000
```

Environment variables must be prefixed with `VITE_` to be exposed to the app.

## Styling

The project uses:
- **Tailwind CSS** for utility-first styling
- **CSS variables** for theming (light/dark mode)
- **shadcn/ui** design system

Theme configuration is in `src/components/theme-provider.tsx`.
