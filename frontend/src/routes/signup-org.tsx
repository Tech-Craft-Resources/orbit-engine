import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import {
  createFileRoute,
  Link as RouterLink,
  redirect,
  useNavigate,
} from "@tanstack/react-router"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { OrganizationsService } from "@/client"
import { AuthLayout } from "@/components/Common/AuthLayout"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import { PasswordInput } from "@/components/ui/password-input"
import { Separator } from "@/components/ui/separator"
import { isLoggedIn } from "@/hooks/useAuth"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

const formSchema = z
  .object({
    organization_name: z
      .string()
      .min(2, { message: "Organization name must be at least 2 characters" }),
    organization_slug: z
      .string()
      .min(3, { message: "Slug must be at least 3 characters" })
      .max(50, { message: "Slug must be at most 50 characters" })
      .regex(slugRegex, {
        message:
          "Slug must contain only lowercase letters, numbers, and hyphens",
      }),
    organization_description: z.string().optional(),
    admin_email: z.string().email({ message: "Please enter a valid email" }),
    admin_first_name: z.string().min(1, { message: "First name is required" }),
    admin_last_name: z.string().min(1, { message: "Last name is required" }),
    admin_phone: z.string().optional(),
    admin_password: z
      .string()
      .min(8, { message: "Password must be at least 8 characters" }),
    confirm_password: z
      .string()
      .min(1, { message: "Password confirmation is required" }),
  })
  .refine((data) => data.admin_password === data.confirm_password, {
    message: "Passwords don't match",
    path: ["confirm_password"],
  })

type FormData = z.infer<typeof formSchema>

export const Route = createFileRoute("/signup-org")({
  component: SignUpOrg,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" })
    }
  },
  head: () => ({
    meta: [{ title: "Create Organization - OrbitEngine" }],
  }),
})

function SignUpOrg() {
  const navigate = useNavigate()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      organization_name: "",
      organization_slug: "",
      organization_description: "",
      admin_email: "",
      admin_first_name: "",
      admin_last_name: "",
      admin_phone: "",
      admin_password: "",
      confirm_password: "",
    },
  })

  const signupMutation = useMutation({
    mutationFn: (data: FormData) =>
      OrganizationsService.signupOrganization({
        requestBody: {
          organization_name: data.organization_name,
          organization_slug: data.organization_slug,
          organization_description: data.organization_description || null,
          admin_email: data.admin_email,
          admin_password: data.admin_password,
          admin_first_name: data.admin_first_name,
          admin_last_name: data.admin_last_name,
          admin_phone: data.admin_phone || null,
        },
      }),
    onSuccess: (response) => {
      localStorage.setItem("access_token", response.access_token)
      showSuccessToast("Organization created successfully!")
      navigate({ to: "/dashboard" })
    },
    onError: handleError.bind(showErrorToast),
  })

  const onSubmit = (data: FormData) => {
    if (signupMutation.isPending) return
    signupMutation.mutate(data)
  }

  /** Auto-generate slug from organization name */
  const handleNameChange = (
    value: string,
    onChange: (value: string) => void,
  ) => {
    onChange(value)
    const currentSlug = form.getValues("organization_slug")
    // Only auto-generate if slug is empty or was previously auto-generated
    const previousName = form.getValues("organization_name")
    const autoSlug = previousName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
    if (!currentSlug || currentSlug === autoSlug) {
      const newSlug = value
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "")
      form.setValue("organization_slug", newSlug, { shouldValidate: true })
    }
  }

  return (
    <AuthLayout>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-6"
        >
          <div className="flex flex-col items-center gap-2 text-center">
            <h1 className="text-2xl font-bold">Create your organization</h1>
            <p className="text-sm text-muted-foreground">
              Set up your organization and admin account
            </p>
          </div>

          <div className="grid gap-4">
            {/* Organization section */}
            <p className="text-sm font-medium text-muted-foreground">
              Organization details
            </p>

            <FormField
              control={form.control}
              name="organization_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Organization Name</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="org-name-input"
                      placeholder="My Company"
                      {...field}
                      onChange={(e) =>
                        handleNameChange(e.target.value, field.onChange)
                      }
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="organization_slug"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Slug</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="org-slug-input"
                      placeholder="my-company"
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    Unique identifier for your organization
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="organization_description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>
                    Description{" "}
                    <span className="text-muted-foreground">(optional)</span>
                  </FormLabel>
                  <FormControl>
                    <Input
                      data-testid="org-description-input"
                      placeholder="Brief description of your organization"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Separator />

            {/* Admin user section */}
            <p className="text-sm font-medium text-muted-foreground">
              Admin account
            </p>

            <div className="grid grid-cols-2 gap-3">
              <FormField
                control={form.control}
                name="admin_first_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                      <Input
                        data-testid="first-name-input"
                        placeholder="John"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="admin_last_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                      <Input
                        data-testid="last-name-input"
                        placeholder="Doe"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name="admin_email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="email-input"
                      placeholder="admin@example.com"
                      type="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="admin_phone"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>
                    Phone{" "}
                    <span className="text-muted-foreground">(optional)</span>
                  </FormLabel>
                  <FormControl>
                    <Input
                      data-testid="phone-input"
                      placeholder="+1 (555) 000-0000"
                      type="tel"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="admin_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="password-input"
                      placeholder="Password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirm_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="confirm-password-input"
                      placeholder="Confirm Password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <LoadingButton
              type="submit"
              className="w-full"
              loading={signupMutation.isPending}
            >
              Create Organization
            </LoadingButton>
          </div>

          <div className="text-center text-sm">
            Already have an account?{" "}
            <RouterLink to="/login" className="underline underline-offset-4">
              Log in
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

export default SignUpOrg
