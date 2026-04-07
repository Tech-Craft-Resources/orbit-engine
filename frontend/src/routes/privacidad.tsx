import { createFileRoute } from "@tanstack/react-router"

import { LandingFooter } from "@/components/Landing/LandingFooter"
import { LandingNav } from "@/components/Landing/LandingNav"

export const Route = createFileRoute("/privacidad" as never)({
  component: PrivacyPagina,
  head: () => ({
    meta: [{ title: "Política de privacidad - OrbitEngine" }],
  }),
})

function PrivacyPagina() {
  return (
    <div className="relative min-h-svh overflow-x-hidden bg-background text-foreground landing-bg">
      <LandingNav />
      <main className="mx-auto max-w-4xl px-6 pb-16 pt-24">
        <h1 className="text-3xl font-bold tracking-tight">
          Política de privacidad
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Fecha de vigencia: 06 de abril de 2026
        </p>
        <div className="prose prose-neutral mt-8 max-w-none dark:prose-invert">
          <h2>1. Introducción</h2>
          <p>
            En OrbitEngine respetamos la privacidad de nuestros usuarios y
            tratamos los datos personales con responsabilidad, transparencia y
            seguridad. Esta Política explica cómo recopilamos, usamos,
            compartimos, almacenamos y protegemos la información personal
            relacionada con el uso de nuestros servicios.
          </p>
          <h2>2. Responsable del tratamiento</h2>
          <p>
            El responsable del tratamiento de los datos personales es
            OrbitEngine. Para consultas, solicitudes o reclamos, escríbenos a
            support@orbitengine.com.
          </p>
          <h2>3. Datos que recopilamos</h2>
          <ul>
            <li>
              Datos de identificación y contacto: nombre, correo, teléfono,
              cargo y empresa.
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
              Datos de uso y soporte: actividad, incidencias y comunicaciones
              con soporte.
            </li>
          </ul>
          <h2>4. Finalidades del tratamiento</h2>
          <ul>
            <li>Crear, administrar y mantener cuentas de usuario.</li>
            <li>Prestar el servicio contratado y habilitar funcionalidades.</li>
            <li>
              Gestionar inventario, ventas, reportes y exportaciones dentro de
              la plataforma.
            </li>
            <li>
              Brindar soporte, atención al cliente y gestión de incidentes.
            </li>
            <li>Cumplir obligaciones legales, regulatorias y contractuales.</li>
          </ul>
          <h2>5. Base legal y consentimiento</h2>
          <p>
            Tratamos datos personales con base en la autorización del titular
            cuando aplique, la ejecución contractual, el cumplimiento legal y el
            interés legítimo de operar y mejorar el servicio, respetando los
            derechos del titular conforme a la normativa colombiana.
          </p>
          <h2>6. Comparticion con terceros</h2>
          <p>
            Podemos compartir datos con proveedores de infraestructura,
            mensajería, soporte y pagos, bajo instrucciones de OrbitEngine y
            obligaciones de confidencialidad y seguridad.
          </p>
          <h2>7. Transferencias internacionales</h2>
          <p>
            Algunos datos pueden almacenarse o tratarse fuera de Colombia por
            proveedores que soportan la operación. Adoptamos medidas razonables
            para mantener niveles adecuados de seguridad y confidencialidad.
          </p>
          <h2>8. Conservación de datos</h2>
          <p>
            Conservamos la información durante el tiempo necesario para cumplir
            finalidades, obligaciones legales y requerimientos de auditoría.
            Luego, eliminamos o anonimizamos los datos de forma segura.
          </p>
          <h2>9. Derechos del titular</h2>
          <p>
            Puedes conocer, actualizar, rectificar y solicitar supresión de tus
            datos, entre otros derechos. Para ejercerlos, escríbenos a
            support@orbitengine.com con tus datos y descripción de la solicitud.
          </p>
          <h2>10. Seguridad de la información</h2>
          <p>
            Implementamos medidas administrativas, técnicas y organizacionales
            razonables para proteger la información contra accesos no
            autorizados, pérdida, alteración o divulgación no permitida.
          </p>
          <h2>11. Cookies</h2>
          <p>
            Usamos cookies para sesiones, preferencias, rendimiento y mejora de
            experiencia. Puedes gestionarlas desde tu navegador.
          </p>
          <h2>12. Menores de edad</h2>
          <p>
            Nuestros servicios están dirigidos a empresas y usuarios mayores de
            edad. Si detectas tratamiento de datos de menores sin autorización
            válida, contáctanos para su gestión.
          </p>
          <h2>13. Cambios a esta política</h2>
          <p>
            Podemos actualizar esta Política por cambios normativos, operativos
            o del servicio. Publicaremos la versión vigente con su fecha de
            actualización.
          </p>
          <h2>14. Contacto</h2>
          <p>
            Para consultas sobre privacidad y datos personales:
            support@orbitengine.com.
          </p>
        </div>
      </main>
      <LandingFooter />
    </div>
  )
}
