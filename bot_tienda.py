import difflib
import json
import os
import re

# =========================
# MEMORIA
# =========================
clientes_sesion = {}
cliente_actual = {}

# =========================
# RUTAS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE_DIR, "clientes.json")
PRODUCTOS_ARCHIVO = os.path.join(BASE_DIR, "productos.json")


def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()


def es_saludo(mensaje):
    return bool(re.search(r'\bho+la+\b', mensaje))


def obtener_cliente(nombre):
    global clientes_sesion
    if nombre not in clientes_sesion:
        clientes_sesion[nombre] = {"nombre": nombre}
    return clientes_sesion[nombre]


# =========================
# JSON CLIENTES
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
        print("⚠️ Error:", e)


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
# PRODUCTOS
# =========================
def cargar_productos():
    if os.path.exists(PRODUCTOS_ARCHIVO):
        try:
            with open(PRODUCTOS_ARCHIVO, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except:
            return {}
    return {}


productos = cargar_productos()


def obtener_info_producto(nombre):
    data = productos.get(nombre, {})
    precio = data.get("precio", "??")
    stock = data.get("stock", 0)

    if stock == 0:
        estado = "😢 sin stock"
    elif stock <= 3:
        estado = "⚠️ quedan MUY pocas"
    elif stock <= 5:
        estado = "👀 quedan pocas unidades"
    else:
        estado = "🙌 hay stock"

    return precio, estado


# =========================
# IA SIMPLE
# =========================
def detectar_palabra(mensaje, lista):
    for palabra in mensaje.split():
        if difflib.get_close_matches(palabra, lista, n=1, cutoff=0.7):
            return True
    return False


def detectar_talla(mensaje):
    tallas = ["xs", "s", "m", "l", "xl", "xxl"]
    for palabra in mensaje.split():
        if palabra in tallas:
            return palabra.upper()
    return None


def detectar_nombre_frase(mensaje):
    claves = ["soy", "nombre", "llamo"]
    palabras = mensaje.split()

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

    try:
        mensaje = normalizar(mensaje)

        # =========================
        # 🙌 DESPEDIDA
        # =========================
        if mensaje in ["gracias", "vale", "ok", "chao", "adios"]:
            nombre = cliente_actual.get("nombre", "")
            cliente_actual.clear()
            return f"😊 ¡De nada {nombre}! Cuando quieras, aquí estaré 🙌"

        # =========================
        # 👋 SALUDO INTELIGENTE
        # =========================
        if es_saludo(mensaje):
            if "nombre" in cliente_actual:
                return f"Hola {cliente_actual['nombre']} 😄 ¿Buscas polerones, parkas o ropa de bebé?"
            return "Hola! 😄 ¿Cuál es tu nombre?"

        # =========================
        # 🔥 DETECTAR PRODUCTO
        # =========================
        if detectar_palabra(mensaje, ["poleron", "polerones", "hoodie"]):
            mensaje = "polerones"
        elif detectar_palabra(mensaje, ["parka", "parkas", "chaqueta"]):
            mensaje = "parkas"
        elif detectar_palabra(mensaje, ["bebe", "bebé", "guagua"]):
            mensaje = "ropa bebé"

        # =========================
        # 💰 INTENCIÓN DE PRECIO
        # =========================
        if any(p in mensaje for p in ["precio", "plata", "cuanto", "cuesta"]):
            if "interes" in cliente_actual:
                return f"💰 Los {cliente_actual['interes']} van desde precios accesibles 👀 ¿Quieres ver opciones?"
            return "💰 Tenemos precios variados 😄 ¿Buscas polerones, parkas o ropa de bebé?"

        # =========================
        # 🔥 TALLA
        # =========================
        talla = detectar_talla(mensaje)
        if talla:
            cliente_actual["talla"] = talla
            cliente_actual["flujo"] = "preguntando_estilo"
            guardar_o_actualizar()
            return f"🔥 Perfecto, talla {talla} 👌 ¿deportivo o urbano?"

        # =========================
        # 👤 NOMBRE
        # =========================
        nombre = detectar_nombre_frase(mensaje)
        if nombre and "nombre" not in cliente_actual:
            cliente_actual = obtener_cliente(nombre)
            guardar_o_actualizar()
            return f"Mucho gusto {nombre} 😊 ¿Qué estás buscando?"

        if "nombre" not in cliente_actual:
            palabras_invalidas = ["hola", "si", "no", "ok", "dale"]
            palabras_producto = ["parka", "parkas", "poleron", "polerones", "bebe"]
            palabras_no_nombre = [
                "plata", "precio", "valor", "cuanto", "cuesta",
                "ver", "quiero", "busco", "necesito",
                "ropa", "stock", "modelo"
            ]
            tallas = ["xs", "s", "m", "l", "xl", "xxl"]

            palabras = mensaje.split()

            if len(palabras) == 1:
                posible = palabras[0]

                if (
                    posible.isalpha()
                    and posible not in palabras_invalidas
                    and posible not in tallas
                    and posible not in palabras_producto
                    and posible not in palabras_no_nombre
                    and not es_saludo(posible)
                    and len(posible) > 2
                ):
                    cliente_actual = obtener_cliente(posible)
                    guardar_o_actualizar()
                    return f"Mucho gusto {posible} 😊 ¿Qué estás buscando?"

        # =========================
        # PRODUCTOS
        # =========================
        def cambiar_interes(nuevo):
            anterior = cliente_actual.get("interes")

            cliente_actual["interes"] = nuevo
            guardar_o_actualizar()

            if "talla" in cliente_actual:
                cliente_actual["flujo"] = "preguntando_estilo"
                return f"😏 Ya tengo tu talla {cliente_actual['talla']} 👌 ¿deportivo o urbano?"

            cliente_actual["flujo"] = "preguntando_talla"

            if anterior and anterior != nuevo:
                return f"😄 Ahh buena, cambiamos a {nuevo} entonces 👌 ¿Qué talla buscas?"
            return None

        if "polerones" in mensaje:
            msg = cambiar_interes("polerones")
            if msg:
                return msg

            precio, estado = obtener_info_producto("polerones")
            talla = cliente_actual.get("talla", "")
            extra = f" en talla {talla}" if talla else ""
            urgencia = " 😳 se están yendo rápido" if "MUY pocas" in estado else ""

            return f"🔥 Tengo polerones{extra} desde ${precio} y {estado}{urgencia} ¿Quieres ver opciones?"

        if "parkas" in mensaje:
            msg = cambiar_interes("parkas")
            if msg:
                return msg

            precio, estado = obtener_info_producto("parkas")
            talla = cliente_actual.get("talla", "")
            extra = f" en talla {talla}" if talla else ""
            urgencia = " 😳 se están yendo rápido" if "MUY pocas" in estado else ""

            return f"🧥 Tengo parkas{extra} desde ${precio} y {estado}{urgencia} ¿Quieres ver opciones?"

        if "ropa bebé" in mensaje:
            msg = cambiar_interes("ropa bebé")
            if msg:
                return msg

            precio, estado = obtener_info_producto("ropa bebé")
            talla = cliente_actual.get("talla", "")
            extra = f" en talla {talla}" if talla else ""
            urgencia = " 😳 se están yendo rápido" if "MUY pocas" in estado else ""

            return f"👶 Tengo ropa de bebé{extra} desde ${precio} y {estado}{urgencia} ¿Quieres ver opciones?"

        # =========================
        # 👍 RESPUESTAS
        # =========================
        if any(p in mensaje for p in ["si", "dale"]):
            flujo = cliente_actual.get("flujo")

            if flujo == "preguntando_talla":
                return "👌 Perfecto, dime tu talla (S, M, L, XL)"

            elif flujo == "preguntando_estilo":
                return "🔥 ¿Prefieres deportivo o urbano?"

        # =========================
        # ESTILO
        # =========================
        if "deportivo" in mensaje or "urbano" in mensaje:

            estilo = "deportivo" if "deportivo" in mensaje else "urbano"

            cliente_actual["estilo"] = estilo
            cliente_actual["flujo"] = None
            guardar_o_actualizar()

            return (
                f"😏 Buena elección {cliente_actual.get('nombre','')}\n\n"
                "🔥 Te puedo mostrar modelos disponibles ahora mismo\n\n"
                "📸 Instagram: https://www.instagram.com/regatea.latienda/\n"
                "💬 O si prefieres, te los mando directo por WhatsApp 👇\n"
                "📲 +56935628595"
            )

        return "🤔 No entendí… ¿Buscas polerones, parkas o ropa de bebé?"

    except Exception as e:
        return f"⚠️ Error: {e}"


# =========================
# LOOP
# =========================
print("📁 Bot iniciado")

while True:
    mensaje = input("Cliente: ")
    respuesta = responder(mensaje)
    print("Bot:", respuesta)
    print(cliente_actual)
