cliente_actual = {}

def responder(mensaje):
    global cliente_actual
    mensaje = mensaje.lower()

    # SALUDO
    if "hola" in mensaje:
        return "Hola! 😊 ¿Cuál es tu nombre?"

    # NOMBRE
    elif "mi nombre es" in mensaje:
        nombre = mensaje.replace("mi nombre es", "").strip()
        cliente_actual["nombre"] = nombre
        return f"Mucho gusto {nombre} 😊 ¿Qué producto buscas?"

    elif mensaje.startswith("soy "):
        nombre = mensaje.replace("soy ", "").strip()
        cliente_actual["nombre"] = nombre
        return f"Mucho gusto {nombre} 😊 ¿Qué producto buscas?"

    # POLERONES
    elif any(palabra in mensaje for palabra in ["poleron", "polerón", "hoodie"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "poleron"

            if any(p in mensaje for p in ["ver", "catalogo", "catálogo"]):
                return (
                    "🔥 Mira nuestros polerones aquí 👇\n\n"
                    "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
                    "📘 Facebook: https://www.facebook.com/Regatea.latienda\n\n"
                    "Tenemos desde $15.000 😏"
                )

            return "Tenemos polerones desde $15.000 🔥 ¿Quieres ver el catálogo?"

        else:
            return "Primero dime tu nombre 😊"

    # PARKAS
    elif any(palabra in mensaje for palabra in ["parka", "chaqueta"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "parka"

            if any(p in mensaje for p in ["ver", "catalogo", "catálogo"]):
                return (
                    "🧥 Mira nuestras parkas aquí 👇\n\n"
                    "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
                    "📘 Facebook: https://www.facebook.com/Regatea.latienda\n\n"
                    "Desde $25.000 🔥"
                )

            return "Las parkas están desde $25.000 🧥 ¿Quieres ver modelos?"

        else:
            return "Primero dime tu nombre 😊"

    # BEBÉ
    elif any(palabra in mensaje for palabra in ["bebe", "bebé", "guagua"]):
        if "nombre" in cliente_actual:
            cliente_actual["interes"] = "ropa de bebé"

            if any(p in mensaje for p in ["ver", "catalogo", "catálogo"]):
                return (
                    "👶 Mira ropa de bebé aquí 👇\n\n"
                    "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
                    "📘 Facebook: https://www.facebook.com/Regatea.latienda\n\n"
                    "Desde $5.000 💖"
                )

            return "Ropa de bebé desde $5.000 👶 ¿Quieres ver opciones?"

        else:
            return "Primero dime tu nombre 😊"

    # PRECIO
    elif "precio" in mensaje or "cuanto cuesta" in mensaje:
        return "Los precios varían según la prenda 👀 ¿Qué producto buscas?"

    # HORARIO
    elif "horario" in mensaje or "hora" in mensaje:
        return "Atendemos de 10:00 a 20:00 🕒"

    # REDES (GENERAL)
    elif any(palabra in mensaje for palabra in ["catalogo", "catálogo", "productos", "ver", "instagram", "ig", "facebook", "tiktok"]):
        return (
            "🔥 Puedes ver todos nuestros productos aquí 👇\n\n"
            "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
            "📘 Facebook: https://www.facebook.com/Regatea.latienda\n"
            "🎵 TikTok: https://www.tiktok.com/@regatea.latienda\n\n"
            "💬 Háblanos por DM y te ayudamos 😉"
        )

    # DEFAULT
    else:
        return "No entendí bien 🤔 ¿Buscas polerones, parkas o ropa de bebé?"


# PROGRAMA PRINCIPAL
while True:
    mensaje = input("Cliente: ")
    respuesta = responder(mensaje)
    print("Bot:", respuesta)
    print(cliente_actual)
