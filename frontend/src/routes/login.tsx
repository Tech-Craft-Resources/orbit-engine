import { zodResolver } from "@hookform/resolvers/zod"
import { createFileRoute, Link as RouterLink } from "@tanstack/react-router"
import { CircleAlert } from "lucide-react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import type { Body_login_login_access_token as AccessToken } from "@/client"
import { AuthLayout } from "@/components/Common/AuthLayout"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import { PasswordInput } from "@/components/ui/password-input"
import useAuth from "@/hooks/useAuth"
import { redirectIfAuthenticated } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

const formSchema = z.object({
  username: z.email(),
  password: z
    .string()
    .min(1, { message: "Password is required" })
    .min(8, { message: "Password must be at least 8 characters" }),
}) satisfies z.ZodType<AccessToken>

type FormData = z.infer<typeof formSchema>

const searchSchema = z.object({
  reason: z.enum(["auth-required", "session-invalid"]).optional(),
})

export const Route = createFileRoute("/login")({
  component: Login,
  validateSearch: searchSchema,
  beforeLoad: async () => {
    await redirectIfAuthenticated(queryClient)
  },
  head: () => ({
    meta: [
      {
        title: "Log In - OrbitEngine",
      },
    ],
  }),
})

function Login() {
  const { loginMutation } = useAuth()
  const { reason } = Route.useSearch()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  })

  const onSubmit = (data: FormData) => {
    if (loginMutation.isPending) return
    loginMutation.mutate(data)
  }

  return (
    <AuthLayout>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-6"
        >
          <div className="flex flex-col items-center gap-2 text-center">
            <h1 className="text-2xl font-bold">Login to your account</h1>
          </div>

          {reason === "session-invalid" ? (
            <Alert variant="destructive">
              <CircleAlert />
              <AlertTitle>Session no longer valid</AlertTitle>
              <AlertDescription>
                Your account session expired or is no longer available. Please
                log in again to continue.
              </AlertDescription>
            </Alert>
          ) : null}

          <div className="grid gap-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="email-input"
                      placeholder="user@example.com"
                      type="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <div className="flex items-center">
                    <FormLabel>Password</FormLabel>
                    <RouterLink
                      to="/recover-password"
                      className="ml-auto text-sm underline-offset-4 hover:underline"
                    >
                      Forgot your password?
                    </RouterLink>
                  </div>
                  <FormControl>
                    <PasswordInput
                      data-testid="password-input"
                      placeholder="Password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />

            <LoadingButton type="submit" loading={loginMutation.isPending}>
              Log In
            </LoadingButton>
          </div>

          <div className="text-center text-sm">
            Don't have an account yet?{" "}
            <RouterLink
              to="/signup-org"
              className="underline underline-offset-4"
            >
              Create an organization
            </RouterLink>
          </div>

          <div className="text-center text-sm text-muted-foreground">
            <RouterLink to="/" className="underline underline-offset-4">
              Back to main page
            </RouterLink>
          </div>
        </form>
      </Form>
    </AuthLayout>
  )
}
