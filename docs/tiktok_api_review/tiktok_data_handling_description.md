# Descripción de Manejo de Datos — TikTok Content Posting API
## IM Music Content Engine — para revisión de app de TikTok

**Aplicación**: IM Music Content Engine
**Cuenta objetivo**: @immusicsello
**API utilizada**: TikTok Content Posting API v2 (`video.publish`, `video.upload`)

## 1. Descripción del caso de uso

IM Music es un sello discográfico independiente. Esta aplicación es una
herramienta de uso interno que automatiza la publicación de contenido de
video ya producido y aprobado (shorts verticales de 30-70 segundos, formato
9:16) en la cuenta oficial de TikTok del sello, @immusicsello, siguiendo un
calendario editorial fijo (contenido educativo sobre la industria musical,
lanzamientos de artistas, y marketing musical).

Todo el contenido es producido, guionado y aprobado manualmente por el equipo
de IM Music antes de la publicación — no se genera ni publica contenido sin
revisión humana previa.

## 2. Flujo técnico de datos

1. **Autorización (OAuth 2.0)**: el usuario administrador de @immusicsello
   inicia sesión directamente en TikTok mediante la pantalla oficial de
   autorización de TikTok (`https://www.tiktok.com/v2/auth/authorize/`). La
   aplicación nunca ve ni almacena la contraseña del usuario.
2. **Intercambio de código por token**: TikTok redirige con un código de
   autorización de un solo uso, que la aplicación intercambia por un
   `access_token` y `refresh_token` mediante una llamada server-to-server
   directa a `https://open.tiktokapis.com/v2/oauth/token/`.
3. **Almacenamiento**: los tokens se guardan en un archivo local cifrado en
   tránsito, con acceso restringido al sistema de archivos del servidor de
   producción de IM Music. No se transmiten a ningún servicio de terceros.
4. **Uso**: los tokens se usan exclusivamente para llamar a los endpoints
   `POST /v2/post/publish/video/init/` y de subida de archivo (`PUT` al
   `upload_url` devuelto por TikTok), para publicar el video ya aprobado.
5. **Renovación**: cuando el `access_token` expira, se usa el
   `refresh_token` para obtener uno nuevo automáticamente, sin intervención
   manual ni nueva autorización del usuario.

## 3. Datos que NO se recopilan ni procesan

- No accedemos a la lista de videos existentes del usuario en TikTok.
- No accedemos a analítica de la cuenta, seguidores, ni comentarios.
- No accedemos a mensajes privados ni información de contactos.
- No se realiza ningún tipo de scraping o acceso no autorizado fuera de los
  endpoints oficiales documentados de la API.

## 4. Seguridad

- Todas las comunicaciones con la API de TikTok se realizan vía HTTPS/TLS.
- Los tokens de acceso nunca se registran en logs de texto plano ni se suben
  a control de versiones (excluidos explícitamente vía `.gitignore`).
- El acceso al archivo de tokens está limitado al equipo operativo del sello.

## 5. Retención y revocación

- El usuario puede revocar el acceso en cualquier momento desde TikTok
  (Ajustes → Seguridad y permisos → Aplicaciones conectadas).
- Al revocar el acceso, los tokens almacenados localmente quedan inválidos de
  inmediato y se eliminan del sistema dentro de 30 días.
