# Política de Privacidad — IM Music Content Engine

**Última actualización: 3 de julio de 2026**

## 1. Quiénes somos

IM Music ("nosotros", "la aplicación") es una herramienta interna de gestión de
contenido para el sello discográfico IM Music (@immusicsello), utilizada para
programar y publicar contenido de video en redes sociales, incluyendo TikTok.

## 2. Qué datos recopilamos

Cuando conectás tu cuenta de TikTok a esta aplicación mediante el flujo de
autorización oficial de TikTok (OAuth 2.0), recopilamos únicamente:

- **Identificador de usuario de TikTok (open_id)**: para identificar la cuenta
  autorizada dentro de nuestro sistema.
- **Token de acceso y token de actualización (access token / refresh token)**:
  para poder publicar contenido en tu nombre sin pedirte que inicies sesión
  cada vez.
- **Permisos de publicación (`video.publish`, `video.upload`)**: usados
  exclusivamente para subir y publicar videos en la cuenta autorizada.

No recopilamos contraseñas de TikTok en ningún momento — la autenticación pasa
exclusivamente por el flujo oficial de OAuth de TikTok, nunca por nuestra
aplicación.

## 3. Cómo usamos los datos

Los tokens de acceso se usan **únicamente** para:
- Subir y publicar videos de contenido de marca previamente aprobado por el
  equipo de IM Music en la cuenta de TikTok autorizada.
- Verificar el estado de publicaciones ya subidas.

No usamos estos datos para ningún otro propósito: no hacemos analítica de
terceros, no vendemos ni compartimos datos con anunciantes, y no accedemos a
ningún dato del usuario de TikTok más allá de lo estrictamente necesario para
publicar contenido.

## 4. Almacenamiento y seguridad

- Los tokens se almacenan localmente, cifrados en tránsito (HTTPS/TLS) en
  todas las comunicaciones con la API de TikTok.
- Los tokens NUNCA se suben a repositorios de código públicos ni se comparten
  con terceros.
- El acceso a los tokens está restringido al equipo operativo de IM Music.

## 5. Retención y eliminación de datos

- Los tokens se conservan mientras la cuenta permanezca conectada a la
  aplicación.
- El usuario puede revocar el acceso en cualquier momento desde la
  configuración de su cuenta de TikTok (Ajustes → Seguridad y permisos →
  Aplicaciones conectadas), lo cual invalida inmediatamente los tokens
  almacenados.
- A pedido del usuario, eliminamos cualquier dato almacenado dentro de 30 días.

## 6. Compartir datos con terceros

No compartimos, vendemos, ni alquilamos ningún dato obtenido a través de la
API de TikTok con terceros, bajo ninguna circunstancia.

## 7. Contacto

Para consultas sobre esta política de privacidad o para solicitar la
eliminación de tus datos, contactar a: **immusicsello@gmail.com**
