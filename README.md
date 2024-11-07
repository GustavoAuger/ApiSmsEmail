# 📬 API de Envío de SMS y Email

Este proyecto es una API RESTful desarrollada en Flask para el envío de mensajes SMS y correos electrónicos. Desplegada en Railway, esta API es ideal para integrarse en aplicaciones o sistemas que requieren funcionalidades de notificaciones automatizadas.

## 🚀 Características

- **Envío de SMS**: Integra el envío de mensajes de texto de manera sencilla.
- **Envío de Emails**: Permite el envío de correos electrónicos personalizados.
- **Endpoints Seguros**: La API está diseñada para ser fácil de usar y segura.

## 📋 Requisitos

- Python 3.7 o superior
- Flask y otros paquetes listados en `requirements.txt`
- Cuenta en Railway para el despliegue

## 🛠 Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/GustavoAuger/ApiSmsEmail.git
   cd ApiSmsEmail


2. **Crea un entorno virtual**:

python -m venv venv
source venv/bin/activate  # Para Linux/Mac
.\venv\Scripts\activate   # Para Windows


3. **Instala las dependencias**:

pip install -r requirements.txt

4. **Configura las credenciales**:

Las credenciales para los servicios de SMS, email y base de datos se deben configurar en un archivo .env. A continuación se listan las variables necesarias:

DB_USER=postgres.zwcokbhciyalafyflvkc
DB_PASSWORD=76eoFV1fuJ5XPfn3
DB_URL=https://zwcokbhciyalafyflvkc.supabase.co
DB_HOST=aws-0-us-east-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3Y29rYmhjaXlhbGFmeWZsdmtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk4OTMzODYsImV4cCI6MjA0NTQ2OTM4Nn0.QWNxXN5_rCDmPNaNpDDHpi5ws4su5XbM8s4ChlhrDGA

- para uso de sms necesitas cuenta en TWULIO y agregar tus propias credenciales.
TWILIO_ACCOUNT_SID= **
TWILIO_AUTH_TOKEN= **
TWILIO_PHONE_NUMBER= **



🖥 Uso
Para ejecutar el servidor localmente:
Copiar código
python app.py
La API debería estar accesible en http://localhost:5000 o en la nube: https://apismsemail-production.up.railway.ap

Puedes usar los siguientes 📡 Endpoints (Probar localmente, o usar Postman https://www.postman.com/)

1. Autenticación (/login):

Método: POST
https://apismsemail-production.up.railway.app/login
http://localhost:5000/login

Parámetros JSON:
{
  'email': correo, 
  'password': contrasena
}

2. Crear campañas email (/add_campaigns): 

Método: POST:
https://apismsemail-production.up.railway.app/add_campaigns
http://localhost:5000/add_campaigns

-canal 2: - envío por email -
-userid_ 1: - usuario de prueba - 
Parámetros JSON:
{
  "nombre_campana": descripcion,
  "canal":2, 
  "user_id":1,
  "template": template,
}

3. Mostrar campañas email (/list_campaigns_by_id): 

Método GET:
https://apismsemail-production.up.railway.app/list_campaigns_by_id
http://localhost:5000/list_campaigns_by_id

Parámetros JSON:
-canal 2: - envío por email -
-userid_ 1: - usuario de prueba - 

{
  'user_id': user_id, 
  'canal': canal
}
 
4. Obtner todos los datos de un usuario:

Método GET:
https://apismsemail-production.up.railway.app/list_users
http://localhost:5000/list_users


Parámetros JSON:
"usuario prueba": 1
{
  "user_id":1
}

5. Enviar Email (/send-email): 

METODO POST:
https://apismsemail-production.up.railway.app/send-email
http://localhost:5000/send-email

Parámetros JSON:
"campaña prueba": 4
{
  'id_campana': 4 
}   


6. Enviar SMS
URL: /send-sms (Por implementar/en desarrollo )

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



☁️ Despliegue en Railway
Para desplegar en Railway:

Crea un nuevo proyecto en Railway y conecta el repositorio de GitHub.
Configura las variables de entorno necesarias en Railway (por ejemplo, claves de API para los servicios de SMS y correo electrónico).
Railway detectará automáticamente la configuración de tu aplicación Flask y la desplegará.
Variables de Entorno para Railway
Asegúrate de que todas las variables de entorno necesarias para conectar la base de datos y los servicios de terceros (como Twilio para SMS) estén configuradas en el panel de Railway:
DB_USER, DB_PASSWORD, DB_URL, DB_HOST, DB_PORT, DB_NAME, DB_API_KEY
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

📂 Estructura del Proyecto

```plaintext

my_project/
├── app.py                  # Archivo principal de la aplicación Flask
├── app/                    # Carpeta de la aplicación
│   ├── __init__.py         # Inicializa la app y registra los blueprints
│   ├── user.py             # Rutas de usuario
│   ├── campaign.py         # Rutas de campañas
│   ├── report.py           # Rutas de reportes (funciones en desarrollo reporte y crud usuario)
│   ├── envio.py            # Rutas de envíos
│   └── models2.py          # Modelos de base de datos
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno para uso local
├── Procfile                # Para desplegar en Railway con gunicorn
└── venv                    # Carpeta del entorno virtual

```