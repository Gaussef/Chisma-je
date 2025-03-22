import requests
import time

MAILTM_API = "https://api.mail.tm"

def crear_cuenta():
    """Crea un correo temporal y devuelve sus credenciales y ID."""
    response = requests.get(f"{MAILTM_API}/domains")
    domain = response.json()["hydra:member"][0]["domain"]  # Obtiene un dominio disponible
    
    email = f"main{int(time.time())}@{domain}"  # Correo aleatorio
    password = "SuperPassword123"  # Contraseña arbitraria

    data = {"address": email, "password": password}
    response = requests.post(f"{MAILTM_API}/accounts", json=data)

    if response.status_code == 201:
        account_id = response.json()["id"]  # ID de la cuenta
        print(f"Correo temporal creado: {email}")
        return email, password, account_id
    else:
        print("Error al crear la cuenta.")
        return None, None, None

def obtener_token(email, password):
    """Autentica el usuario y obtiene el token de sesión."""
    response = requests.post(f"{MAILTM_API}/token", json={"address": email, "password": password})
    if response.status_code == 200:
        return response.json()["token"]
    return None

def obtener_mensajes(token):
    """Obtiene los mensajes de la bandeja de entrada."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{MAILTM_API}/messages", headers=headers)
    if response.status_code == 200:
        return response.json()["hydra:member"]
    return []

def leer_mensaje(token, mensaje_id):
    """Lee el contenido de un mensaje específico."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{MAILTM_API}/messages/{mensaje_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def eliminar_cuenta(token, account_id):
    """Elimina la cuenta temporal cuando se desocupe."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{MAILTM_API}/accounts/{account_id}", headers=headers)
    
    if response.status_code == 204:
        print("\n✅ Cuenta eliminada correctamente.")
    else:
        print("\n⚠️ No se pudo eliminar la cuenta.")

def main():
    email, password, account_id = crear_cuenta()
    if not email:
        return
    
    token = obtener_token(email, password)
    if not token:
        print("Error al obtener el token de autenticación.")
        return
    
    print("Esperando correos entrantes... (Presiona CTRL+C para salir)")
    mensajes_vistos = set()

    try:
        while True:
            mensajes = obtener_mensajes(token)

            for mensaje in mensajes:
                mensaje_id = mensaje["id"]
                if mensaje_id not in mensajes_vistos:
                    mensajes_vistos.add(mensaje_id)
                    contenido = leer_mensaje(token, mensaje_id)

                    if contenido:
                        print("\n=== NUEVO MENSAJE ===")
                        print(f"De: {contenido['from']['address']}")
                        print(f"Asunto: {contenido['subject']}")
                        print(f"Fecha: {contenido['createdAt']}")
                        print(f"Contenido:\n{contenido['text']}\n")

            time.sleep(10)  # Espera 10 segundos antes de verificar nuevamente

    except KeyboardInterrupt:
        print("\nSaliendo del programa...")
        eliminar_cuenta(token, account_id)

if __name__ == "__main__":
    main()