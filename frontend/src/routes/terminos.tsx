import { createFileRoute } from "@tanstack/react-router"

import {
  LegalLink,
  LegalPageLayout,
  LegalSection,
} from "@/components/legal/LegalPageLayout"

export const Route = createFileRoute("/terminos" as never)({
  component: TermsPagina,
  head: () => ({
    meta: [{ title: "Términos y condiciones - OrbitEngine" }],
  }),
})

const termsSections = [
  { id: "aceptacion", title: "1. Aceptación" },
  { id: "definiciones", title: "2. Definiciones" },
  { id: "cuentas", title: "3. Elegibilidad y cuentas" },
  { id: "uso", title: "4. Uso permitido y prohibido" },
  { id: "suscripcion", title: "5. Suscripción y facturación" },
  { id: "prueba", title: "6. Prueba gratuita de 1 mes" },
  { id: "renovacion", title: "7. Renovación y cancelación" },
  { id: "propiedad", title: "8. Propiedad intelectual" },
  { id: "confidencialidad", title: "9. Confidencialidad" },
  { id: "disponibilidad", title: "10. Disponibilidad y cambios" },
  { id: "responsabilidad", title: "11. Limitación de responsabilidad" },
  { id: "indemnidad", title: "12. Indemnidad" },
  { id: "terminacion", title: "13. Terminación y suspensión" },
  { id: "jurisdiccion", title: "14. Ley aplicable y jurisdicción" },
  { id: "contacto", title: "15. Contacto" },
]

function TermsPagina() {
  return (
    <LegalPageLayout
      title="Términos y condiciones de uso"
      lastUpdated="06 de abril de 2026"
      sections={termsSections}
    >
      <LegalSection id="aceptacion" title="1. Aceptación">
        <p>
          Estos Términos regulan el acceso y uso de OrbitEngine. Al registrarte,
          acceder o usar la plataforma, aceptas estas condiciones.
        </p>
      </LegalSection>

      <LegalSection id="definiciones" title="2. Definiciones">
        <ul className="space-y-2 pl-5 marker:text-muted-foreground list-disc">
          <li>OrbitEngine: proveedor del servicio de suscripción.</li>
          <li>Cliente: persona natural o jurídica que contrata el servicio.</li>
          <li>
            Usuario: persona autorizada por el cliente para usar la plataforma.
          </li>
          <li>Plan Pro: plan comercial de suscripcion.</li>
          <li>Prueba gratuita: 1 mes con acceso completo al Plan Pro.</li>
        </ul>
      </LegalSection>

      <LegalSection id="cuentas" title="3. Elegibilidad y cuentas">
        <p>
          El cliente debe contar con capacidad legal y es responsable de la
          veracidad de la información, la administración de usuarios, y la
          confidencialidad de credenciales.
        </p>
      </LegalSection>

      <LegalSection id="uso" title="4. Uso permitido y prohibido">
        <p>
          El servicio se usa para fines empresariales legítimos. Está prohibido
          usar la plataforma para actividades ilegales, vulnerar seguridad,
          interferir con el servicio o acceder sin autorización.
        </p>
      </LegalSection>

      <LegalSection id="suscripcion" title="5. Suscripción y facturación">
        <p>
          OrbitEngine opera bajo suscripción al Plan Pro. Cargos, períodos y
          condiciones se informan al contratar. El incumplimiento de pago puede
          generar restricción o suspensión del servicio.
        </p>
      </LegalSection>

      <LegalSection id="prueba" title="6. Prueba gratuita de 1 mes">
        <p>
          Aplica para nuevas cuentas elegibles. Si no cancelas antes de
          finalizar la prueba, la cuenta puede pasar al plan de pago según
          condiciones aceptadas al activarla.
        </p>
      </LegalSection>

      <LegalSection id="renovacion" title="7. Renovación y cancelación">
        <p>
          La suscripción se renueva automáticamente salvo cancelación previa. La
          cancelación evita renovaciones futuras y no afecta cobros ya causados.
        </p>
      </LegalSection>

      <LegalSection id="propiedad" title="8. Propiedad intelectual">
        <p>
          OrbitEngine, su marca, diseño y funcionalidades están protegidos. El
          uso del servicio no transfiere titularidad al cliente.
        </p>
      </LegalSection>

      <LegalSection id="confidencialidad" title="9. Confidencialidad">
        <p>
          Cada parte se compromete a tratar como confidencial la información no
          pública recibida durante la relación comercial, salvo excepciones
          legales.
        </p>
      </LegalSection>

      <LegalSection id="disponibilidad" title="10. Disponibilidad y cambios">
        <p>
          Hacemos esfuerzos razonables para mantener continuidad del servicio,
          sin garantizar disponibilidad ininterrumpida. Podemos realizar
          mantenimientos y mejoras cuando sea necesario.
        </p>
      </LegalSection>

      <LegalSection
        id="responsabilidad"
        title="11. Limitación de responsabilidad"
      >
        <p>
          En la medida permitida por la ley, OrbitEngine no será responsable por
          perjuicios indirectos y su responsabilidad total se limita a valores
          pagados en un período razonable previo.
        </p>
      </LegalSection>

      <LegalSection id="indemnidad" title="12. Indemnidad">
        <p>
          El cliente mantendrá indemne a OrbitEngine frente a reclamaciones
          derivadas de uso indebido, incumplimiento de términos o vulneración de
          derechos de terceros.
        </p>
      </LegalSection>

      <LegalSection id="terminacion" title="13. Terminación y suspensión">
        <p>
          OrbitEngine puede suspender o terminar accesos por incumplimiento
          material, falta de pago o riesgos razonables de seguridad, fraude o
          uso ilicito.
        </p>
      </LegalSection>

      <LegalSection id="jurisdiccion" title="14. Ley aplicable y jurisdicción">
        <p>
          Estos Términos se rigen por las leyes de la República de Colombia. Las
          controversias se someten a la jurisdicción competente en Colombia.
        </p>
      </LegalSection>

      <LegalSection id="contacto" title="15. Contacto">
        <h3 className="text-sm font-semibold text-foreground sm:text-base">
          Correo de soporte
        </h3>
        <p>
          Para consultas legales, contractuales o de soporte:{" "}
          <LegalLink href="mailto:support@orbitengine.com">
            support@orbitengine.com
          </LegalLink>
          .
        </p>
      </LegalSection>
    </LegalPageLayout>
  )
}
