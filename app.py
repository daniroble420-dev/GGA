import streamlit as st
import pandas as pd
import datetime
import calendar
from PIL import Image

# Configuración de la página usando la imagen real de la cartera como icono de pestaña
try:
    icon_img = Image.open("ChatGPT Image 10 ago 2026, 01_45_28 a.m..png")
except Exception:
    icon_img = "👛"

st.set_page_config(page_title="Gestor de Dinero Personal", page_icon=icon_img, layout="wide")

# --- CONTROL DE ACCESO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if 'mes_activo' not in st.session_state:
    st.session_state.mes_activo = None

if 'creando_mes' not in st.session_state:
    st.session_state.creando_mes = False

if not st.session_state.autenticado:
    col_izq, col_centro, col_der = st.columns([1, 1, 1])
    with col_centro:
        _, col_img, _ = st.columns([1, 1, 1])
        with col_img:
            try:
                img = Image.open("ChatGPT Image 10 ago 2026, 01_45_28 a.m..png")
                st.image(img, width=90)
            except Exception:
                st.warning("No se pudo cargar la imagen.")
        
        st.markdown("<h2 style='text-align: center; margin-top: 5px; margin-bottom: 10px;'>Bienvenido</h2>", unsafe_allow_html=True)
        
        pwd = st.text_input("Contraseña", placeholder="Contraseña", type="password", label_visibility="collapsed")
        
        if st.button("Entrar", use_container_width=True):
            if pwd == "1234":  
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# --- SI ESTÁ AUTENTICADO, CARGA EL RESTO ---

if 'datos_financieros' not in st.session_state:
    st.session_state.datos_financieros = {
        "Marzo 2026": {
            "salario": 1410.0,
            "dinero_extra": 662.05,
            "ahorro_fijo": 600.0,
            "dinero_gastos_fijo": 438.69,
            "presupuesto": {"Ocio": 70.0, "Fijo": 128.69, "Curro": 80.0, "Capricho": 70.0, "Otros": 388.0},
            "gastos": [],
            "gastos_calendario": [],
            "ahorro_cuenta": 1400.0
        }
    }

for _m_info in st.session_state.datos_financieros.values():
    if "gastos_calendario" not in _m_info:
        _m_info["gastos_calendario"] = []

# --- PÁGINA INTERMEDIA DE SELECCIÓN DE MES / CUADRADO CON "+" INTERACTIVO ---
if st.session_state.mes_activo is None:
    col_izq_m, col_cent_m, col_der_m = st.columns([1, 2, 1])
    with col_cent_m:
        st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Selecciona o Crea un Mes</h1>", unsafe_allow_html=True)
        
        for mes_disponible in list(st.session_state.datos_financieros.keys()):
            if st.button(f"📁 {mes_disponible}", use_container_width=True):
                st.session_state.mes_activo = mes_disponible
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón interactivo que actúa exactamente como el cuadrado visual solicitado
        if not st.session_state.creando_mes:
            if st.button("➕\n\nAñadir nuevo mes", use_container_width=True):
                st.session_state.creando_mes = True
                st.rerun()
        else:
            with st.form("form_crear_mes_previo"):
                st.markdown("<h3 style='text-align: center;'>Crear Nuevo Mes</h3>", unsafe_allow_html=True)
                nuevo_mes_input = st.text_input("Nombre del nuevo mes (ej. Octubre 2026)", placeholder="Octubre 2026")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    submitted = st.form_submit_button("Crear y Entrar", use_container_width=True)
                with col_b2:
                    cancelled = st.form_submit_button("Cancelar", use_container_width=True)
                
                if cancelled:
                    st.session_state.creando_mes = False
                    st.rerun()
                    
                if submitted:
                    if nuevo_mes_input and nuevo_mes_input not in st.session_state.datos_financieros:
                        st.session_state.datos_financieros[nuevo_mes_input] = {
                            "salario": 0.0, "dinero_extra": 0.0, "ahorro_fijo": 600.0, 
                            "dinero_gastos_fijo": 0.0,
                            "presupuesto": {"Ocio": 70.0, "Fijo": 120.0, "Curro": 80.0, "Capricho": 70.0, "Otros": 70.0},
                            "gastos": [], "gastos_calendario": [], "ahorro_cuenta": 1500.0
                        }
                        st.session_state.mes_activo = nuevo_mes_input
                        st.session_state.creando_mes = False
                        st.rerun()
                    elif nuevo_mes_input in st.session_state.datos_financieros:
                        st.session_state.mes_activo = nuevo_mes_input
                        st.session_state.creando_mes = False
                        st.rerun()
    st.stop()

# Título principal con la imagen real de la cartera al lado
col_t1, col_t2 = st.columns([0.08, 0.92])
with col_t1:
    try:
        title_img = Image.open("ChatGPT Image 10 ago 2026, 01_45_28 a.m..png")
        st.image(title_img, width=50)
    except Exception:
        st.write("👛")
with col_t2:
    st.title("Mi Gestor de Dinero Personal")

st.sidebar.header("Panel de Navegación")

if st.sidebar.button("⬅️ Cambiar de Mes"):
    st.session_state.mes_activo = None
    st.rerun()

meses_disponibles = list(st.session_state.datos_financieros.keys())
mes_seleccionado = st.sidebar.selectbox("Selecciona el Mes", meses_disponibles, index=meses_disponibles.index(st.session_state.mes_activo) if st.session_state.mes_activo in meses_disponibles else 0)
st.session_state.mes_activo = mes_seleccionado

nuevo_mes = st.sidebar.text_input("Añadir nuevo mes (ej. Abril 2026)")
if st.sidebar.button("Crear Mes"):
    if nuevo_mes and nuevo_mes not in st.session_state.datos_financieros:
        st.session_state.datos_financieros[nuevo_mes] = {
            "salario": 0.0, "dinero_extra": 0.0, "ahorro_fijo": 600.0, 
            "dinero_gastos_fijo": 0.0,
            "presupuesto": {"Ocio": 70.0, "Fijo": 120.0, "Curro": 80.0, "Capricho": 70.0, "Otros": 70.0},
            "gastos": [], "gastos_calendario": [], "ahorro_cuenta": 1500.0
        }
        st.rerun()

data = st.session_state.datos_financieros[mes_seleccionado]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configuración del Mes")
data["salario"] = st.sidebar.number_input("Salario (€)", value=data["salario"], step=10.0)
data["dinero_extra"] = st.sidebar.number_input("Dinero Extra (€)", value=data["dinero_extra"], step=10.0)
data["ahorro_fijo"] = st.sidebar.number_input("Ahorro Fijo en Cuenta (€)", value=data["ahorro_fijo"], step=10.0)
data["dinero_gastos_fijo"] = st.sidebar.number_input("Lo que dejo para gastos (€)", value=data["dinero_gastos_fijo"], step=10.0)

ingresos_totales = data["salario"] + data["dinero_extra"]
df_gastos = pd.DataFrame(data["gastos"]) if data["gastos"] else pd.DataFrame(columns=["fecha", "categoria", "descripcion", "monto"])
total_gastado = df_gastos["monto"].sum() if not df_gastos.empty else 0.0

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📝 Gasto", "📅 Calendario", "📈 Estadísticas", "🔒 Cierre"])

with tab1:
    st.header(f"Resumen: {mes_seleccionado}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Salario + Extra", f"{ingresos_totales:.2f} €")
    c2.metric("Ahorro Fijo", f"{data['ahorro_fijo']:.2f} €")
    c3.metric("Para Gastos", f"{data['dinero_gastos_fijo']:.2f} €")
    
    st.subheader("Control por Categorías (Modificar Estándar)")
    
    gastos_por_cat = df_gastos.groupby("categoria")["monto"].sum() if not df_gastos.empty else pd.Series(dtype=float)
    
    with st.form("form_editar_estandar"):
        nuevos_estandares = {}
        st.write("Modifica el presupuesto estándar de cada categoría:")
        for cat, estandar in data["presupuesto"].items():
            nuevos_estandares[cat] = st.number_input(f"Presupuesto para '{cat}' (€)", min_value=0.0, value=float(estandar), step=5.0)
            
        if st.form_submit_button("Actualizar Presupuesto Estándar"):
            data["presupuesto"] = nuevos_estandares
            st.success("¡Presupuestos estándar actualizados correctamente!")
            st.rerun()

    st.markdown("---")
    resumen_data = []
    for cat, estandar in data["presupuesto"].items():
        gastado_cat = gastos_por_cat.get(cat, 0.0)
        restante_cat = estandar - gastado_cat
        resumen_data.append({
            "Categoría": cat, 
            "Estándar (€)": round(estandar, 2), 
            "Gastado (€)": round(gastado_cat, 2),
            "Queda por gastar (€)": round(restante_cat, 2)
        })
    
    df_resumen = pd.DataFrame(resumen_data).set_index("Categoría")
    
    df_resumen_styled = df_resumen.style.format("{:.2f}").set_properties(**{'text-align': 'center'}).set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]
    )
    st.dataframe(df_resumen_styled, use_container_width=True)

with tab2:
    st.header("Registrar Gasto y Gestión de Categorías")
    
    with st.expander("🛠️ Administrar Categorías (Añadir / Cambiar nombre)"):
        with st.form("form_gestionar_categorias"):
            st.write("Añadir nueva categoría:")
            nueva_cat_nombre = st.text_input("Nombre de la nueva categoría")
            nueva_cat_presupuesto = st.number_input("Presupuesto inicial (€)", min_value=0.0, value=50.0)
            
            st.markdown("---")
            st.write("Renombrar categoría existente:")
            cat_a_renombrar = st.selectbox("Selecciona categoría a modificar", ["-- Ninguna --"] + list(data["presupuesto"].keys()))
            nuevo_nombre_cat = st.text_input("Nuevo nombre para la categoría")
            
            if st.form_submit_button("Guardar Cambios en Categorías"):
                if nueva_cat_nombre and nueva_cat_nombre not in data["presupuesto"]:
                    data["presupuesto"][nueva_cat_nombre] = nueva_cat_presupuesto
                    st.success(f"Categoría '{nueva_cat_nombre}' añadida.")
                if cat_a_renombrar != "-- Ninguna --" and nuevo_nombre_cat and nuevo_nombre_cat not in data["presupuesto"]:
                    data["presupuesto"][nuevo_nombre_cat] = data["presupuesto"].pop(cat_a_renombrar)
                    for g in data["gastos"]:
                        if g["categoria"] == cat_a_renombrar:
                            g["categoria"] = nuevo_nombre_cat
                    for g in data["gastos_calendario"]:
                        if g["categoria"] == cat_a_renombrar:
                            g["categoria"] = nuevo_nombre_cat
                    st.success(f"Categoría renombrada a '{nuevo_nombre_cat}'.")
                st.rerun()

    st.markdown("---")
    with st.form("form_gasto_rapido"):
        col1, col2 = st.columns(2)
        cat = col1.selectbox("Categoría", list(data["presupuesto"].keys()))
        monto = col2.number_input("Importe", min_value=0.0)
        desc = st.text_input("Descripción")
        if st.form_submit_button("Guardar"):
            data["gastos"].append({"fecha": str(datetime.date.today()), "categoria": cat, "descripcion": desc, "monto": monto})
            st.rerun()

    st.markdown("---")
    st.subheader("Historial de Gastos")
    st.dataframe(df_gastos, use_container_width=True)

with tab3:
    st.header("Calendario de Gastos")
    fecha_sel = st.date_input("Seleccionar fecha")
    with st.form("form_cal"):
        cat_cal = st.selectbox("Categoría", list(data["presupuesto"].keys()))
        monto_cal = st.number_input("Monto", min_value=0.0)
        desc_cal = st.text_input("Descripción")
        if st.form_submit_button("Añadir Gasto en este día"):
            data["gastos_calendario"].append({"fecha": str(fecha_sel), "categoria": cat_cal, "descripcion": desc_cal, "monto": monto_cal})
            st.success(f"Gasto guardado para el {fecha_sel}")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📅 Calendario Completo del Año (Meses con días coloreados si hay gasto)")
    
    try:
        partes = mes_seleccionado.split()
        anio = int(partes[1])
    except:
        anio = 2026

    conteo_fechas = {}
    for g in data["gastos_calendario"]:
        try:
            f_obj = datetime.datetime.strptime(g["fecha"], "%Y-%m-%d").date()
            if f_obj.year == anio:
                conteo_fechas[f_obj] = conteo_fechas.get(f_obj, 0) + 1
        except:
            pass

    nombres_meses = [
        ("Enero", 1), ("Febrero", 2), ("Marzo", 3), ("Abril", 4),
        ("Mayo", 5), ("Junio", 6), ("Julio", 7), ("Agosto", 8),
        ("Septiembre", 9), ("Octubre", 10), ("Noviembre", 11), ("Diciembre", 12)
    ]

    for i in range(0, 12, 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < 12:
                m_nombre, m_num = nombres_meses[i + j]
                with cols[j]:
                    st.markdown(f"**{m_nombre} {anio}**")
                    cal = calendar.Calendar(firstweekday=0)
                    semanas = cal.monthdayscalendar(anio, m_num)
                    
                    matriz = []
                    for sem in semanas:
                        fila = {"Sem.": datetime.date(anio, m_num, [d for d in sem if d > 0][0]).isocalendar()[1]}
                        for idx_d, d_val in enumerate(["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]):
                            dia_num = sem[idx_d]
                            if dia_num != 0:
                                fecha_comprobacion = datetime.date(anio, m_num, dia_num)
                                cant_gastos = conteo_fechas.get(fecha_comprobacion, 0)
                                if cant_gastos > 0:
                                    if cant_gastos > 1:
                                        fila[d_val] = f"🔵{cant_gastos} {dia_num}"
                                    else:
                                        fila[d_val] = f"🔵 {dia_num}"
                                else:
                                    fila[d_val] = str(dia_num)
                            else:
                                fila[d_val] = ""
                        matriz.append(fila)
                    
                    df_m = pd.DataFrame(matriz).set_index("Sem.")
                    st.dataframe(df_m, use_container_width=True)

    st.markdown("---")
    st.subheader("📝 Listado y Gestión de Gastos Especiales")
    if data["gastos_calendario"]:
        for idx, g_item in enumerate(data["gastos_calendario"]):
            with st.container():
                col_info1, col_info2, col_info3, col_info4, col_btn1, col_btn2 = st.columns([1.5, 1.5, 2, 1, 1, 1])
                col_info1.write(f"**Fecha:** {g_item['fecha']}")
                col_info2.write(f"**Cat:** {g_item['categoria']}")
                col_info3.write(f"**Desc:** {g_item['descripcion']}")
                col_info4.write(f"**Monto:** {g_item['monto']} €")
                
                if col_btn1.button("✏️ Modificar", key=f"mod_cal_{idx}"):
                    st.session_state[f"edit_cal_{idx}"] = True
                if col_btn2.button("🗑️ Borrar", key=f"del_cal_{idx}"):
                    data["gastos_calendario"].pop(idx)
                    st.rerun()
                
                if st.session_state.get(f"edit_cal_{idx}", False):
                    with st.form(key=f"form_edit_cal_{idx}"):
                        nuevo_f = st.date_input("Nueva fecha", value=datetime.datetime.strptime(g_item["fecha"], "%Y-%m-%d").date(), key=f"ef_{idx}")
                        nueva_c = st.selectbox("Nueva categoría", list(data["presupuesto"].keys()), index=list(data["presupuesto"].keys()).index(g_item["categoria"]) if g_item["categoria"] in data["presupuesto"] else 0, key=f"ec_{idx}")
                        nueva_d = st.text_input("Nueva descripción", value=g_item["descripcion"], key=f"ed_{idx}")
                        nuevo_m = st.number_input("Nuevo monto", value=float(g_item["monto"]), key=f"em_{idx}")
                        
                        if st.form_submit_button("Guardar cambios"):
                            data["gastos_calendario"][idx] = {
                                "fecha": str(nuevo_f),
                                "categoria": nueva_c,
                                "descripcion": nueva_d,
                                "monto": nuevo_m
                            }
                        st.session_state[f"edit_cal_{idx}"] = False
                        st.rerun()
    else:
        st.info("No hay gastos especiales registrados en el calendario todavía.")

with tab4:
    st.header("Estadísticas Mensuales")
    historial = []
    for mes, info in st.session_state.datos_financieros.items():
        g_mes = pd.DataFrame(info["gastos"])["monto"].sum() if info["gastos"] else 0.0
        ing_mes = info["salario"] + info["dinero_extra"]
        ahorro_mes = ing_mes - g_mes - info["ahorro_fijo"]
        historial.append({"Mes": mes, "Ingresos (€)": ing_mes, "Gastos (€)": g_mes, "Ahorro Neto (€)": ahorro_mes})
    
    st.table(pd.DataFrame(historial))

with tab5:
    st.header("Cierre de Mes")
    data["ahorro_cuenta"] = st.number_input("Dinero Total en Cuenta", value=data["ahorro_cuenta"])
    