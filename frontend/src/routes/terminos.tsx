import { createFileRoute } from "@tanstack/react-router"

import { LandingFooter } from "@/components/Landing/LandingFooter"
import { LandingNav } from "@/components/Landing/LandingNav"

export const Route = createFileRoute("/terminos" as never)({
  component: TermsPagina,
  head: () => ({
    meta: [{ title: "Términos y condiciones - OrbitEngine" }],
  }),
})

function TermsPagina() {
  return (
    <div className="relative min-h-svh overflow-x-hidden bg-background text-foreground landing-bg">
      <LandingNav />
      <main className="mx-auto max-w-4xl px-6 pb-16 pt-24">
        <h1 className="text-3xl font-bold tracking-tight">
          Términos y condiciones de uso
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Fecha de vigencia: 06 de abril de 2026
        </p>
        <div className="prose prose-neutral mt-8 max-w-none dark:prose-invert">
          <h2>1. Aceptación</h2>
          <p>
            Estos Términos regulan el acceso y uso de OrbitEngine. Al
            registrarte, acceder o usar la plataforma, aceptas estas
            condiciones.
          </p>
          <h2>2. Definiciones</h2>
          <ul>
            <li>OrbitEngine: proveedor del servicio de suscripción.</li>
            <li>
              Cliente: persona natural o jurídica que contrata el servicio.
            </li>
            <li>
              Usuario: persona autorizada por el cliente para usar la
              plataforma.
            </li>
            <li>Plan Pro: plan comercial de suscripcion.</li>
            <li>Prueba gratuita: 1 mes con acceso completo al Plan Pro.</li>
          </ul>
          <h2>3. Elegibilidad y cuentas</h2>
          <p>
            El cliente debe contar con capacidad legal y es responsable de la
            veracidad de la información, la administración de usuarios, y la
            confidencialidad de credenciales.
          </p>
          <h2>4. Uso permitido y prohibido</h2>
          <p>
            El servicio se usa para fines empresariales legítimos. Está
            prohibido usar la plataforma para actividades ilegales, vulnerar
            seguridad, interferir con el servicio o acceder sin autorización.
          </p>
          <h2>5. Suscripción y facturación</h2>
          <p>
            OrbitEngine opera bajo suscripción al Plan Pro. Cargos, períodos y
            condiciones se informan al contratar. El incumplimiento de pago
            puede generar restricción o suspensión del servicio.
          </p>
          <h2>6. Prueba gratuita de 1 mes</h2>
          <p>
            Aplica para nuevas cuentas elegibles. Si no cancelas antes de
            finalizar la prueba, la cuenta puede pasar al plan de pago según
            condiciones aceptadas al activarla.
          </p>
          <h2>7. Renovación y cancelación</h2>
          <p>
            La suscripción se renueva automáticamente salvo cancelación previa.
            La cancelación evita renovaciones futuras y no afecta cobros ya
            causados.
          </p>
          <h2>8. Propiedad intelectual</h2>
          <p>
            OrbitEngine, su marca, diseño y funcionalidades están protegidos. El
            uso del servicio no transfiere titularidad al cliente.
          </p>
          <h2>9. Confidencialidad</h2>
          <p>
            Cada parte se compromete a tratar como confidencial la información
            no pública recibida durante la relación comercial, salvo excepciones
            legales.
          </p>
          <h2>10. Disponibilidad y cambios</h2>
          <p>
            Hacemos esfuerzos razonables para mantener continuidad del servicio,
            sin garantizar disponibilidad ininterrumpida. Podemos realizar
            mantenimientos y mejoras cuando sea necesario.
          </p>
          <h2>11. Limitación de responsabilidad</h2>
          <p>
            En la medida permitida por la ley, OrbitEngine no será responsable
            por perjuicios indirectos y su responsabilidad total se limita a
            valores pagados en un período razonable previo.
          </p>
          <h2>12. Indemnidad</h2>
          <p>
            El cliente mantendrá indemne a OrbitEngine frente a reclamaciones
            derivadas de uso indebido, incumplimiento de términos o vulneración
            de derechos de terceros.
          </p>
          <h2>13. Terminación y suspensión</h2>
          <p>
            OrbitEngine puede suspender o terminar accesos por incumplimiento
            material, falta de pago o riesgos razonables de seguridad, fraude o
            uso ilicito.
          </p>
          <h2>14. Ley aplicable y jurisdicción</h2>
          <p>
            Estos Términos se rigen por las leyes de la República de Colombia.
            Las controversias se someten a la jurisdicción competente en
            Colombia.
          </p>
          <h2>15. Contacto</h2>
          <p>
            Para consultas legales, contractuales o de soporte:
            support@orbitengine.com.
          </p>
        </div>
      </main>
      <LandingFooter />
    </div>
  )
}
