
API de Envío de SMS y Email
Este proyecto contiene una API RESTful construida en Flask para el envío de mensajes SMS y correos electrónicos. Está desplegado en Railway y puede ser utilizado para integrarse en otras aplicaciones o sistemas que requieran funcionalidad de notificaciones.

Características
Envío de mensajes SMS.
Envío de correos electrónicos.
Endpoints seguros y documentados.
Requisitos
Python 3.7+
Flask y otros paquetes en requirements.txt
Cuenta de Railway para el despliegue.
Instalación
Clona el repositorio:

bash
Copiar código
git clone https://github.com/GustavoAuger/ApiSmsEmail.git
cd ApiSmsEmail
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configura tus credenciales de servicios (como proveedor de SMS y correo electrónico) en variables de entorno o en un archivo de configuración .env.

Uso
Para ejecutar el servidor localmente:

bash
Copiar código
python app.py
La API debería estar accesible en http://localhost:5000.

Endpoints
1. Enviar SMS
Endpoint: /send-sms
Método: POST
Parámetros JSON:
phone: Número de teléfono destinatario.
message: Mensaje a enviar.
Ejemplo de uso:
json
Copiar código
{
  "phone": "+1234567890",
  "message": "Hola, este es un mensaje de prueba."
}
2. Enviar Email
Endpoint: /send-email
Método: POST
Parámetros JSON:
email: Dirección de correo electrónico destinatario.
subject: Asunto del correo.
body: Cuerpo del mensaje.
Ejemplo de uso:
json
Copiar código
{
  "email": "ejemplo@correo.com",
  "subject": "Asunto del correo",
  "body": "Cuerpo del mensaje"
}
Despliegue en Railway
Para desplegar en Railway:

Crea un nuevo proyecto en Railway y conecta el repositorio de GitHub.
Configura las variables de entorno necesarias en Railway (por ejemplo, claves de API de servicios de SMS y correo).
Railway detectará automáticamente tu aplicación Flask y la desplegará.
