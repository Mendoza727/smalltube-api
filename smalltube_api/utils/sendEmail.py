import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, link, to_email):
    server = None
    from_email = "juancamilomendozavillegas14@gmail.com"
    password = "bmod tzhs xnmp hbyo"

    # creamos el mensaje para enviarlo
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject


    # adjuntamos el body
    msg.attach(MIMEText(f'''
    <!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Verifica tu correo electrónico</title>
  </head>
  <body
    style="
      margin: 0;
      padding: 0;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      background-color: #f7f9fc;
      color: #333333;
    "
  >
    <table
      border="0"
      cellpadding="0"
      cellspacing="0"
      width="100%"
      style="min-width: 100%; background-color: #f7f9fc"
    >
      <tr>
        <td align="center" valign="top" style="padding: 40px 10px">
          <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="
              max-width: 600px;
              background-color: #ffffff;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            "
          >
            <!-- Header -->
            <tr>
              <td
                align="center"
                valign="top"
                style="
                  padding: 40px 20px;
                  background-color: #4f46e5;
                  background-image: linear-gradient(
                    135deg,
                    #4f46e5 0%,
                    #7c3aed 100%
                  );
                "
              >
                <h1
                  style="
                    color: #ffffff;
                    font-size: 28px;
                    margin: 0;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                  "
                >
                  Verifica tu correo electrónico
                </h1>
              </td>
            </tr>
            <!-- Content -->
            <tr>
              <td align="left" valign="top" style="padding: 40px 30px">
                <p style="margin: 0 0 20px; font-size: 16px; line-height: 1.5">
                  Hola,
                </p>
                <p style="margin: 0 0 20px; font-size: 16px; line-height: 1.5">
                  Gracias por unirte a nuestro servicio de videos. Para completar tu
                  registro y comenzar a disfrutar de todas las funciones, por
                  favor verifica tu dirección de correo electrónico:
                </p>
                <table
                  border="0"
                  cellpadding="0"
                  cellspacing="0"
                  width="100%"
                  style="min-width: 100%; padding: 20px 0"
                >
                  <tr>
                    <td align="center">
                      <a
                        href="{link}"
                        target="_blank"
                        style="
                          display: inline-block;
                          padding: 14px 30px;
                          background-color: #4f46e5;
                          color: #ffffff;
                          text-decoration: none;
                          font-weight: bold;
                          font-size: 16px;
                          border-radius: 50px;
                          transition: background-color 0.3s ease;
                        "
                        >Verificar mi email</a
                      >
                    </td>
                  </tr>
                </table>
                <p
                  style="
                    margin: 0 0 20px;
                    font-size: 14px;
                    line-height: 1.5;
                    color: #666666;
                  "
                >
                  Si el botón no funciona, copia y pega este enlace en tu
                  navegador:
                </p>
                <p
                  style="
                    margin: 0 0 20px;
                    font-size: 14px;
                    line-height: 1.5;
                    word-break: break-all;
                  "
                >
                  <a href="{link}" style="color: #4f46e5; text-decoration: none"
                    >{link}</a
                  >
                </p>
                <p style="margin: 0 0 20px; font-size: 16px; line-height: 1.5">
                  Si no has solicitado esta verificación, puedes ignorar este
                  mensaje.
                </p>
                <p style="margin: 0; font-size: 16px; line-height: 1.5">
                  ¡Gracias por elegirnos!<br />El equipo de smalltube
                </p>
              </td>
            </tr>
            <!-- Footer -->
            <tr>
              <td
                align="center"
                valign="top"
                style="
                  padding: 30px;
                  background-color: #f0f4f8;
                  border-top: 1px solid #e5e7eb;
                "
              >
                <p
                  style="
                    margin: 0 0 10px;
                    font-size: 12px;
                    line-height: 1.5;
                    color: #6b7280;
                  "
                >
                  Este es un correo electrónico automático, por favor no
                  respondas a este mensaje.
                </p>
                <p
                  style="
                    margin: 0;
                    font-size: 12px;
                    line-height: 1.5;
                    color: #6b7280;
                  "
                >
                  &copy; 2024 smalltube. Todos los derechos
                  reservados.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
''', 'html'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()  # Identify yourself to the server
        server.starttls()  # Secure the connection with TLS
        server.login(from_email, password=password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print("Correo HTML enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        # Ensure server.quit() is called only if the connection exists
        if server:
            try:
                server.quit()
            except Exception as quit_error:
                print(f"Error al cerrar la conexión: {quit_error}")

