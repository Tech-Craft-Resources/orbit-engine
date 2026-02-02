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
