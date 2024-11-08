📬 API de Envío de SMS y Email
Este proyecto es una API RESTful desarrollada en Flask para el envío de mensajes SMS y correos electrónicos. Desplegada en Railway, esta API es ideal para integrarse en aplicaciones o sistemas que requieren funcionalidades de notificaciones.

🚀 Características
Envío de SMS: Integra fácilmente el envío de mensajes de texto.
Envío de Emails: Permite el envío de correos electrónicos personalizados.
Endpoints seguros: La API está diseñada para ser fácil de usar y segura.
📋 Requisitos
Python 3.7+
Flask y otros paquetes listados en requirements.txt
Cuenta en Railway para el despliegue
🛠 Instalación
Clona el repositorio:

bash
Copiar código
git clone https://github.com/GustavoAuger/ApiSmsEmail.git
cd ApiSmsEmail
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configura tus credenciales:

Agrega las credenciales de servicios (como el proveedor de SMS y correo electrónico) en variables de entorno o en un archivo .env para su uso en la aplicación.

🖥 Uso
Para ejecutar el servidor localmente:

bash
Copiar código
python app.py
La API debería estar accesible en http://localhost:5000.

📡 Endpoints
1. Enviar SMS
URL: /send-sms

Método: POST

Parámetros JSON:

phone: Número de teléfono del destinatario.
message: Texto del mensaje a enviar.
Ejemplo de solicitud:

json
Copiar código
{
  "phone": "+1234567890",
  "message": "Hola, este es un mensaje de prueba."
}
2. Enviar Email
URL: /send-email

Método: POST

Parámetros JSON:

email: Dirección de correo del destinatario.
subject: Asunto del correo.
body: Cuerpo del mensaje.
Ejemplo de solicitud:

json
Copiar código
{
  "email": "ejemplo@correo.com",
  "subject": "Asunto del correo",
  "body": "Cuerpo del mensaje"
}
☁️ Despliegue en Railway
Para desplegar en Railway:

Crea un nuevo proyecto en Railway y conecta el repositorio de GitHub.
Configura las variables de entorno necesarias en Railway (por ejemplo, claves de API para los servicios de SMS y correo electrónico).
Railway detectará automáticamente la configuración de tu aplicación Flask y la desplegará.
