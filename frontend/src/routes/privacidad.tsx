import { createFileRoute } from "@tanstack/react-router"

import {
  LegalLink,
  LegalPageLayout,
  LegalSection,
} from "@/components/legal/LegalPageLayout"

export const Route = createFileRoute("/privacidad" as never)({
  component: PrivacyPagina,
  head: () => ({
    meta: [{ title: "Política de privacidad - OrbitEngine" }],
  }),
})

const privacySections = [
  { id: "introduccion", title: "1. Introducción" },
  { id: "responsable", title: "2. Responsable del tratamiento" },
  { id: "datos", title: "3. Datos que recopilamos" },
  { id: "finalidades", title: "4. Finalidades del tratamiento" },
  { id: "base-legal", title: "5. Base legal y consentimiento" },
  { id: "terceros", title: "6. Comparticion con terceros" },
  { id: "transferencias", title: "7. Transferencias internacionales" },
  { id: "conservacion", title: "8. Conservación de datos" },
  { id: "derechos", title: "9. Derechos del titular" },
  { id: "seguridad", title: "10. Seguridad de la información" },
  { id: "cookies", title: "11. Cookies" },
  { id: "menores", title: "12. Menores de edad" },
  { id: "cambios", title: "13. Cambios a esta política" },
  { id: "contacto", title: "14. Contacto" },
]

function PrivacyPagina() {
  return (
    <LegalPageLayout
      title="Política de privacidad"
      lastUpdated="06 de abril de 2026"
      sections={privacySections}
    >
      <LegalSection id="introduccion" title="1. Introducción">
        <p>
          En OrbitEngine respetamos la privacidad de nuestros usuarios y
          tratamos los datos personales con responsabilidad, transparencia y
          seguridad. Esta Política explica cómo recopilamos, usamos,
          compartimos, almacenamos y protegemos la información personal
          relacionada con el uso de nuestros servicios.
        </p>
      </LegalSection>

      <LegalSection id="responsable" title="2. Responsable del tratamiento">
        <p>
          El responsable del tratamiento de los datos personales es OrbitEngine.
          Para consultas, solicitudes o reclamos, escríbenos a{" "}
          <LegalLink href="mailto:support@orbitengine.com">
            support@orbitengine.com
          </LegalLink>
          .
        </p>
      </LegalSection>

      <LegalSection id="datos" title="3. Datos que recopilamos">
        <ul className="space-y-2 pl-5 marker:text-muted-foreground list-disc">
          <li>
            Datos de identificación y contacto: nombre, correo, teléfono, cargo
            y empresa.
          </li>
          <li>
            Datos de cuenta: credenciales, rol de usuario y configuraciones.
          </li>
          <li>
            Datos operativos: inventario, ventas, movimientos operativos y
            reportes.
          </li>
          <li>
            Datos de facturación y suscripción: plan, pagos e historial de
            suscripción.
          </li>
          <li>
            Datos de uso y soporte: actividad, incidencias y comunicaciones con
            soporte.
          </li>
        </ul>
      </LegalSection>

      <LegalSection id="finalidades" title="4. Finalidades del tratamiento">
        <ul className="space-y-2 pl-5 marker:text-muted-foreground list-disc">
          <li>Crear, administrar y mantener cuentas de usuario.</li>
          <li>Prestar el servicio contratado y habilitar funcionalidades.</li>
          <li>
            Gestionar inventario, ventas, reportes y exportaciones dentro de la
            plataforma.
          </li>
          <li>Brindar soporte, atención al cliente y gestión de incidentes.</li>
          <li>Cumplir obligaciones legales, regulatorias y contractuales.</li>
        </ul>
      </LegalSection>

      <LegalSection id="base-legal" title="5. Base legal y consentimiento">
        <p>
          Tratamos datos personales con base en la autorización del titular
          cuando aplique, la ejecución contractual, el cumplimiento legal y el
          interés legítimo de operar y mejorar el servicio, respetando los
          derechos del titular conforme a la normativa colombiana.
        </p>
      </LegalSection>

      <LegalSection id="terceros" title="6. Comparticion con terceros">
        <p>
          Podemos compartir datos con proveedores de infraestructura,
          mensajería, soporte y pagos, bajo instrucciones de OrbitEngine y
          obligaciones de confidencialidad y seguridad.
        </p>
      </LegalSection>

      <LegalSection
        id="transferencias"
        title="7. Transferencias internacionales"
      >
        <p>
          Algunos datos pueden almacenarse o tratarse fuera de Colombia por
          proveedores que soportan la operación. Adoptamos medidas razonables
          para mantener niveles adecuados de seguridad y confidencialidad.
        </p>
      </LegalSection>

      <LegalSection id="conservacion" title="8. Conservación de datos">
        <p>
          Conservamos la información durante el tiempo necesario para cumplir
          finalidades, obligaciones legales y requerimientos de auditoría.
          Luego, eliminamos o anonimizamos los datos de forma segura.
        </p>
      </LegalSection>

      <LegalSection id="derechos" title="9. Derechos del titular">
        <p>
          Puedes conocer, actualizar, rectificar y solicitar supresión de tus
          datos, entre otros derechos. Para ejercerlos, escríbenos a{" "}
          <LegalLink href="mailto:support@orbitengine.com">
            support@orbitengine.com
          </LegalLink>{" "}
          con tus datos y descripción de la solicitud.
        </p>
      </LegalSection>

      <LegalSection id="seguridad" title="10. Seguridad de la información">
        <p>
          Implementamos medidas administrativas, técnicas y organizacionales
          razonables para proteger la información contra accesos no autorizados,
          pérdida, alteración o divulgación no permitida.
        </p>
      </LegalSection>

      <LegalSection id="cookies" title="11. Cookies">
        <p>
          Usamos cookies para sesiones, preferencias, rendimiento y mejora de
          experiencia. Puedes gestionarlas desde tu navegador.
        </p>
      </LegalSection>

      <LegalSection id="menores" title="12. Menores de edad">
        <p>
          Nuestros servicios están dirigidos a empresas y usuarios mayores de
          edad. Si detectas tratamiento de datos de menores sin autorización
          válida, contáctanos para su gestión.
        </p>
      </LegalSection>

      <LegalSection id="cambios" title="13. Cambios a esta política">
        <p>
          Podemos actualizar esta Política por cambios normativos, operativos o
          del servicio. Publicaremos la versión vigente con su fecha de
          actualización.
        </p>
      </LegalSection>

      <LegalSection id="contacto" title="14. Contacto">
        <p>
          Para consultas sobre privacidad y datos personales:{" "}
          <LegalLink href="mailto:support@orbitengine.com">
            support@orbitengine.com
          </LegalLink>
          .
        </p>
      </LegalSection>
    </LegalPageLayout>
  )
}
