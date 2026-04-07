import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import {
  createFileRoute,
  Link as RouterLink,
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
import useCustomToast from "@/hooks/useCustomToast"
import { redirectIfAuthenticated } from "@/lib/auth-guards"
import { setAccessToken } from "@/lib/auth-session"
import { queryClient } from "@/lib/queryClient"
import { handleError } from "@/utils"

const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

const formSchema = z
  .object({
    organization_name: z.string().min(2, {
      message: "El nombre de la organización debe tener al menos 2 caracteres",
    }),
    organization_slug: z
      .string()
      .min(3, { message: "El slug debe tener al menos 3 caracteres" })
      .max(50, { message: "El slug debe tener máximo 50 caracteres" })
      .regex(slugRegex, {
        message: "El slug solo puede contener minúsculas, números y guiones",
      }),
    organization_description: z.string().optional(),
    admin_email: z
      .string()
      .email({ message: "Ingresa un correo electrónico válido" }),
    admin_first_name: z
      .string()
      .min(1, { message: "El nombre es obligatorio" }),
    admin_last_name: z
      .string()
      .min(1, { message: "El apellido es obligatorio" }),
    admin_phone: z.string().optional(),
    admin_password: z
      .string()
      .min(8, { message: "La contraseña debe tener al menos 8 caracteres" }),
    confirm_password: z
      .string()
      .min(1, { message: "Debes confirmar la contraseña" }),
  })
  .refine((data) => data.admin_password === data.confirm_password, {
    message: "Las contraseñas no coinciden",
    path: ["confirm_password"],
  })

type FormData = z.infer<typeof formSchema>

export const Route = createFileRoute("/signup-org")({
  component: SignUpOrg,
  beforeLoad: async () => {
    await redirectIfAuthenticated(queryClient)
  },
  head: () => ({
    meta: [{ title: "Crear organización - OrbitEngine" }],
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
      setAccessToken(response.access_token)
      showSuccessToast("Organización creada correctamente")
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
            <h1 className="text-2xl font-bold">Crea tu organización</h1>
            <p className="text-sm text-muted-foreground">
              Configura tu organización y la cuenta administradora
            </p>
          </div>

          <div className="grid gap-4">
            {/* Organization section */}
            <p className="text-sm font-medium text-muted-foreground">
              Datos de la organización
            </p>

            <FormField
              control={form.control}
              name="organization_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nombre de la organización</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="org-name-input"
                      placeholder="Mi empresa"
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
                    Identificador único de tu organización
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
                    Descripción{" "}
                    <span className="text-muted-foreground">(opcional)</span>
                  </FormLabel>
                  <FormControl>
                    <Input
                      data-testid="org-description-input"
                      placeholder="Descripción breve de tu organización"
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
              Cuenta administradora
            </p>

            <div className="grid grid-cols-2 gap-3">
              <FormField
                control={form.control}
                name="admin_first_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nombre</FormLabel>
                    <FormControl>
                      <Input
                        data-testid="first-name-input"
                        placeholder="Juan"
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
                    <FormLabel>Apellido</FormLabel>
                    <FormControl>
                      <Input
                        data-testid="last-name-input"
                        placeholder="Perez"
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
                  <FormLabel>Correo electronico</FormLabel>
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
                    Teléfono{" "}
                    <span className="text-muted-foreground">(opcional)</span>
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
                  <FormLabel>Contraseña</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="password-input"
                      placeholder="Contraseña"
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
                  <FormLabel>Confirmar contraseña</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="confirm-password-input"
                      placeholder="Confirmar contraseña"
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
              Crear organización
            </LoadingButton>
          </div>

          <div className="text-center text-sm">
            ¿Ya tienes una cuenta?{" "}
            <RouterLink to="/login" className="underline underline-offset-4">
              Iniciar sesión
            </RouterLink>
          </div>

          <div className="text-center text-sm text-muted-foreground">
            <RouterLink to="/" className="underline underline-offset-4">
              Volver a la página principal
            </RouterLink>
          </div>
        </form>
      </Form>
    </AuthLayout>
  )
}

export default SignUpOrg
