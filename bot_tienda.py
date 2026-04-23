import difflib
import json
import os

cliente_actual = {}

# 📁 RUTA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE_DIR, "clientes.json")


# =========================
# JSON
# =========================
def cargar_clientes():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return []
    return []


def guardar_clientes(lista):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(lista, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print("⚠️ Error al guardar:", e)


clientes = cargar_clientes()


def guardar_o_actualizar():
    global clientes, cliente_actual

    if "nombre" not in cliente_actual:
        return

    for c in clientes:
        if c["nombre"] == cliente_actual["nombre"]:
            c.update(cliente_actual)
            guardar_clientes(clientes)
            return

    clientes.append(cliente_actual.copy())
    guardar_clientes(clientes)


# =========================
# IA SIMPLE
# =========================
def detectar_palabra(mensaje, lista):
    for palabra in mensaje.split():
        if difflib.get_close_matches(palabra, lista, n=1, cutoff=0.7):
            return True
    return False


def detectar_talla(mensaje):
    palabras = mensaje.split()
    tallas = ["xs", "s", "m", "l", "xl", "xxl"]

    for palabra in palabras:
        if palabra in tallas:
            return palabra.upper()
    return None


def detectar_nombre_frase(mensaje):
    palabras = mensaje.split()
    claves = ["soy", "nombre", "llamo"]

    for i, p in enumerate(palabras):
        if p in claves and i + 1 < len(palabras):
            nombre = palabras[i + 1]
            if nombre.isalpha() and len(nombre) >= 3:
                return nombre
    return None


# =========================
# BOT
# =========================
def responder(mensaje):
    global cliente_actual

    mensaje = mensaje.lower().strip()

    # 🚫 SI YA ESTÁ EN COMPRA
    if cliente_actual.get("flujo") == "compra":
        return "🛒 Ya estamos en proceso de compra 😄 Escríbenos por DM para finalizar 😉"

    # 👋 SALUDO
    if "hola" in mensaje:
        if "nombre" in cliente_actual:
            return f"Hola {cliente_actual['nombre']} 😄 ¿Buscas polerones, parkas o ropa de bebé?"
        return "Hola! 😊 ¿Cuál es tu nombre?"

    # 👤 NOMBRE CON FRASE (soy mati)
    nombre = detectar_nombre_frase(mensaje)
    if nombre and "nombre" not in cliente_actual:
        cliente_actual["nombre"] = nombre
        guardar_o_actualizar()
        return f"Mucho gusto {nombre} 😊 ¿Qué estás buscando?"

    # 👤 NOMBRE SOLO (mati)  🔥 IMPORTANTE: va AQUÍ
    if "nombre" not in cliente_actual:
        palabras_invalidas = [
            "hola", "si", "sí", "no", "dale", "ok",
            "poleron", "polerones", "parka", "parkas",
            "bebe", "bebé", "guagua", "comprar"
        ]

        palabras = mensaje.split()

        if len(palabras) == 1:
            posible_nombre = palabras[0]

            if (
                posible_nombre.isalpha() and
                posible_nombre not in palabras_invalidas and
                len(posible_nombre) >= 3
            ):
                cliente_actual["nombre"] = posible_nombre
                guardar_o_actualizar()
                return f"Mucho gusto {posible_nombre} 😊 ¿Qué estás buscando?"

    # 🛒 COMPRA
    if "comprar" in mensaje:
        if "interes" in cliente_actual:
            cliente_actual["flujo"] = "compra"
            guardar_o_actualizar()

            return (
                f"🛒 Buenísima {cliente_actual.get('nombre','')}! 🙌\n\n"
                f"Producto: {cliente_actual.get('interes','')}\n"
                f"Talla: {cliente_actual.get('talla','No definida')}\n"
                f"Estilo: {cliente_actual.get('estilo','No definido')}\n\n"
                "📩 Escríbenos por DM 👇\n"
                "https://www.instagram.com/regatea.latienda/"
            )
        return "👀 ¿Qué producto te gustaría comprar?"

    # 👍 SI
    if any(p in mensaje for p in ["si", "sí", "dale", "ok", "obvio"]):
        flujo = cliente_actual.get("flujo")

        if flujo == "preguntando_talla":
            return "👌 Perfecto, dime tu talla (S, M, L, XL)"

        elif flujo == "preguntando_estilo":
            return "🔥 Buenísimo ¿te gusta más deportivo o urbano?"

        elif "interes" in cliente_actual:
            return (
                "🔥 Mira aquí 👇\n\n"
                "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
                "📘 Facebook: https://www.facebook.com/Regatea.latienda\n\n"
                "💬 Escríbenos por DM 😉"
            )

    # 👎 NO
    if any(p in mensaje for p in ["no", "nop", "no gracias"]):
        cliente_actual["flujo"] = None
        return "😊 Dale! Si necesitas algo, dime qué buscas"

    # 👕 TALLA
    talla = detectar_talla(mensaje)
    if talla:
        cliente_actual["talla"] = talla
        cliente_actual["flujo"] = "preguntando_estilo"
        guardar_o_actualizar()
        return f"🔥 Perfecto, talla {talla} 👌 ¿prefieres estilo deportivo o urbano?"

    # 🎯 ESTILO
    if "deportivo" in mensaje or "urbano" in mensaje:
        cliente_actual["estilo"] = mensaje
        cliente_actual["flujo"] = "cerrando"
        guardar_o_actualizar()

        return (
            f"😏 Buena elección {cliente_actual.get('nombre','')}\n\n"
            "Te dejo los modelos aquí 👇\n\n"
            "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
            "📘 Facebook: https://www.facebook.com/Regatea.latienda\n\n"
            "💬 Háblanos por DM 😉"
        )

    # 🛍️ PRODUCTOS
    if detectar_palabra(mensaje, ["poleron", "polerones", "hoodie"]):
        cliente_actual["interes"] = "polerones"
        cliente_actual["flujo"] = "preguntando_talla"
        guardar_o_actualizar()
        return "🔥 Tenemos polerones desde $15.000 ¿Quieres ver opciones?"

    if detectar_palabra(mensaje, ["parka", "parkas", "chaqueta"]):
        cliente_actual["interes"] = "parkas"
        cliente_actual["flujo"] = "preguntando_talla"
        guardar_o_actualizar()
        return "🧥 Parkas desde $25.000 ¿Quieres ver opciones?"

    if detectar_palabra(mensaje, ["bebe", "bebé", "guagua"]):
        cliente_actual["interes"] = "ropa bebé"
        cliente_actual["flujo"] = "preguntando_talla"
        guardar_o_actualizar()
        return "👶 Ropa de bebé desde $5.000 ¿Quieres ver opciones?"

    # 🙌 GRACIAS / DESPEDIDA
    if any(p in mensaje for p in ["gracias", "eso nomas", "eso no más", "eso seria", "eso sería"]):
        cliente_actual["flujo"] = None
        return (
            f"😊 ¡De nada {cliente_actual.get('nombre','')}!\n\n"
            "Si necesitas algo más, aquí estoy 🙌\n"
            "💬 Escríbenos cuando quieras 😉"
        )

    # 🌐 REDES
    if any(p in mensaje for p in ["catalogo", "productos", "ver"]):
        return (
            "🔥 Mira todo aquí 👇\n\n"
            "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
            "📘 Facebook: https://www.facebook.com/Regatea.latienda\n"
            "🎵 TikTok: https://www.tiktok.com/@regatea.latienda\n\n"
            "💬 Escríbenos por DM 😉"
        )

    return "🤔 No entendí… ¿Buscas polerones, parkas o ropa de bebé?"


# =========================
# LOOP
# =========================
print("📁 Guardando en:", ARCHIVO)

while True:
    mensaje = input("Cliente: ")
    respuesta = responder(mensaje)
    print("Bot:", respuesta)
    print(cliente_actual)
