cliente_actual = {}

def responder(mensaje):
    global cliente_actual
    mensaje = mensaje.lower()

    # SALUDO
    if "hola" in mensaje:
        return "Hola! 😊 ¿Cuál es tu nombre?"

    # NOMBRE (más flexible)
    elif "mi nombre es" in mensaje or "soy" in mensaje:
        nombre = mensaje.replace("mi nombre es", "").replace("soy", "").strip()
        cliente_actual["nombre"] = nombre
        return f"Mucho gusto {nombre} 😊 ¿Qué producto buscas?"

    # PRODUCTOS (más natural)
    elif any(palabra in mensaje for palabra in ["poleron", "polerón", "hoodie"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "poleron"
            return "Tenemos polerones desde $15.000 🔥"
        else:
            return "Primero dime tu nombre 😊"

    elif any(palabra in mensaje for palabra in ["parka", "chaqueta"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "parka"
            return "Las parkas están desde $25.000 🧥"
        else:
            return "Primero dime tu nombre 😊"

    elif any(palabra in mensaje for palabra in ["bebe", "bebé", "guagua"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "ropa de bebé"
            return "Ropa de bebé desde $5.000 👶"
        else:
            return "Primero dime tu nombre 😊"

    # PRECIO
    elif "precio" in mensaje or "cuanto cuesta" in mensaje:
        return "Los precios varían según la prenda 👀 ¿Qué producto buscas?"

    # HORARIO
    elif "horario" in mensaje or "hora" in mensaje:
        return "Atendemos de 10:00 a 20:00 🕒"

    # DEFAULT
    else:
        return "No entendí bien 🤔 ¿Buscas polerones, parkas o ropa de bebé?"


# 👇 FUERA de la función
while True:
    mensaje = input("Cliente: ")
    respuesta = responder(mensaje)
    print("Bot:", respuesta)
    print(cliente_actual)