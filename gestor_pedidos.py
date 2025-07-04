
# Aplicación web para gestionar pedidos de clientes
import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(page_title="Gestor de Pedidos", layout="wide")
st.title("📋 Gestor de Pedidos de Clientes")

# Base de datos temporal en sesión
if "clientes" not in st.session_state:
    st.session_state.clientes = {}

# Crear nuevo cliente
with st.sidebar:
    st.header("➕ Agregar Cliente")
    nuevo_nombre = st.text_input("Nombre del cliente")
    if st.button("Agregar cliente") and nuevo_nombre:
        id_cliente = str(uuid.uuid4())
        st.session_state.clientes[id_cliente] = {
            "nombre": nuevo_nombre,
            "pedidos": []
        }
        st.success("Cliente agregado")

# Mostrar clientes existentes
st.subheader("👤 Lista de Clientes")
for id_cliente, data in st.session_state.clientes.items():
    with st.expander(f"{data['nombre']} ({len(data['pedidos'])} pedidos)"):
        st.markdown("### ➕ Nuevo Pedido")
        with st.form(f"form_{id_cliente}"):
            tipo = st.text_input("Tipo de playera", key=f"tipo_{id_cliente}")
            cantidad = st.number_input("Cantidad", min_value=1, key=f"cant_{id_cliente}")
            talla_color = st.text_input("Talla y color", key=f"talla_{id_cliente}")
            costo_playera = st.number_input("Costo por playera", min_value=0.0, key=f"costo_p_{id_cliente}")
            costo_bordado = st.number_input("Costo del bordado", min_value=0.0, key=f"costo_b_{id_cliente}")
            imagen = st.file_uploader("Imagen del logo", type=["png", "jpg", "jpeg"], key=f"img_{id_cliente}")
            fecha_pedido = st.date_input("Fecha del pedido", key=f"fecha_ped_{id_cliente}")
            fecha_entrega = st.date_input("Fecha de entrega", key=f"fecha_ent_{id_cliente}")
            progreso = st.selectbox("Estado del pedido", ["1️⃣ Anticipo", "2️⃣ Surtir playeras", "3️⃣ En bordado", "4️⃣ Listo para entrega"], key=f"prog_{id_cliente}")
            submit = st.form_submit_button("Guardar pedido")

        if submit:
            pedido = {
                "tipo": tipo,
                "cantidad": cantidad,
                "talla_color": talla_color,
                "costo_playera": costo_playera,
                "costo_bordado": costo_bordado,
                "imagen": imagen.name if imagen else None,
                "fecha_pedido": fecha_pedido.strftime("%Y-%m-%d"),
                "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
                "progreso": progreso,
                "id": str(uuid.uuid4())
            }
            st.session_state.clientes[id_cliente]["pedidos"].append(pedido)
            st.success("✅ Pedido guardado")

        if data['pedidos']:
            st.markdown("### 📦 Pedidos")
            for pedido in data['pedidos']:
                st.markdown(f"- **{pedido['tipo']}** | {pedido['cantidad']} piezas | {pedido['talla_color']} | {pedido['progreso']}")
                st.markdown(f"  🗓️ {pedido['fecha_pedido']} ➡️ {pedido['fecha_entrega']}")
                st.markdown(f"  💵 ${pedido['costo_playera']} playera + ${pedido['costo_bordado']} bordado")
                if pedido['imagen']:
                    st.markdown(f"  🖼️ Logo: {pedido['imagen']}")
                st.markdown("---")
