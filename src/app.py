import streamlit as st
from chatbot.core import app  # Importa el flujo de trabajo compilado

# Configuración de la página
st.set_page_config(page_title="Chatbot de Soporte Técnico", page_icon="🤖" )

# Estilos CSS para el título
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;900&display=swap');

.sifen-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.8em;  /* Tamaño más pequeño */
  background: linear-gradient(90deg, #ff6a00, #ee0979);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  margin: 0;
  padding: 10px 0;
  text-align: center;
  line-height: 1.2;  /* Ajuste de interlineado */
}
</style>
<div class="sifen-title">MANUAL TÉCNICO<br>SISTEMA INTEGRADO<br>DE FACTURACIÓN<br>ELECTRÓNICA<br>NACIONAL (SIFEN)</div>
""", unsafe_allow_html=True)

# Inicializar el historial del chat si no existe
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Función para mostrar el historial del chat
def display_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**Tú:** {message['content']}")  # Mensaje del usuario
        else:
            st.write(f"**Bot:** {message['content']}")  # Mensaje del bot

# Sidebar con preguntas frecuentes en formato de acordeón
with st.sidebar:
    st.header("📚 Preguntas Frecuentes")
    st.markdown("Selecciona una pregunta para ver la respuesta:")

    # Preguntas frecuentes en formato de acordeón
    with st.expander("¿La DNIT autoriza a los Proveedores de Servicios Tecnológicos a prestar los servicios de Facturación Electrónica en SIFEN?"):
        st.markdown("""
        **Respuesta:**  
        NO. El modelo operativo de SIFEN entiende que la interacción de la DNIT con los facturadores electrónicos es de manera directa y sin necesidad de intermediación obligatoria de un actor diferente. Quiere decir esto que, a discreción y decisión de los contribuyentes, estos podrán acudir o NO a los servicios de proveedores tecnológicos.
        """)

    with st.expander("¿Cuáles son los contribuyentes que se encuentran habilitados a facturar Electrónicamente en SIFEN?"):
        st.markdown("""
        **Respuesta:**  
        La SET dispone las listas de todos los contribuyentes habilitados como Facturadores Electrónicos. Los cuales pueden ser consultados en la sección "Facturadores Electrónicos" en el inicio de esta página de e-Kuatia.
        """)

    with st.expander("¿Por cuánto tiempo se deben conservar los Documentos Electrónicos (DE)?"):
        st.markdown("""
        **Respuesta:**  
        El facturador electrónico deberá conservar en su sistema de facturación, por el plazo de prescripción del tributo establecido en la Ley Tributaria, todos aquellos DE y DTE que haya emitido, recibido, transmitido, debiendo garantizar la integridad, confidencialidad, accesibilidad o consulta posterior de los mismos, sin perjuicio que el contribuyente pueda conservar dichos documentos por un plazo mayor al establecido. Del mismo modo, deberá conservar los archivos electrónicos de los eventos de los DTE emitidos o recibidos y de los eventos de inutilización de número de DE.
        """)

    with st.expander("¿Cuáles son los Eventos realizados por el Receptor?"):
        st.markdown("""
        **Respuesta:**  
        1. **Conformidad con el DTE:** El receptor informa a la Administración Tributaria que conoce dicho documento y confirma que están correctos todas las informaciones del DTE, que no existen errores o inconsistencias en forma parcial o total y que ha recibido la mercadería o servicio.  
        2. **Disconformidad con el DTE:** El receptor informa a la Administración Tributaria que conoce dicho documento, pero que en el comprobante existen errores o inconsistencias en forma parcial o total y tiene objeciones sobre la mercadería recibida y/o servicio prestado.  
        3. **Desconocimiento con el DE o DTE:** El receptor informa a la Administración Tributaria que desconoce el documento que fuera emitido a su nombre y la operación detallada en el mismo.  
        4. **Notificación de recepción de un DE o DTE:** El receptor informa a la Administración Tributaria que ha recibido dicho documento, sin embargo, aún no tiene condiciones para manifestarse de forma conclusiva (con Conformidad, Disconformidad o Desconocimiento).
        """)

    with st.expander("¿A qué nos referimos cuando hablamos de Eventos del Receptor?"):
        st.markdown("""
        **Respuesta:**  
        Son aquellos eventos generados por una persona física o jurídica, a cuyo nombre fue emitido un documento electrónico. El registro del evento de receptor se puede dar sobre un DE o DTE. Los eventos del receptor no invalidarán el DE o DTE, sino que quedarán marcados en el SIFEN y el emisor electrónico podrá conocer dicha situación.
        """)

    with st.expander("¿Un Documento Tributario Electrónico (DTE) puede ser Cancelado?"):
        st.markdown("""
        **Respuesta:**  
        El facturador electrónico podrá solicitar la cancelación de la FE hasta las 48 horas posteriores a la fecha y hora de aprobación del DTE por parte del SIFEN, y para la cancelación de los demás documentos hasta las 168 horas (7 días) posteriores a la fecha y hora de aprobación del DTE. Como resultado de esto, el DTE quedará registrado con el estado “cancelado” en el SIFEN. El DTE cancelado por el emisor no tendrá validez legal ni tributaria para respaldar débito fiscal y/o crédito fiscal, así como los ingresos, costos y/o gastos.
        """)

    with st.expander("¿Se puede Inutilizar un Documento Electrónico (DE)?"):
        st.markdown("""
        **Respuesta:**  
        En caso de que existiera salto en la numeración correlativa del DE o error por fallo en el sistema informático o en el llenado de estos; el facturador electrónico, dentro de los quince (15) primeros días del mes siguiente de ocurrido el error, deberá comunicar la inutilización de la numeración del Documento Electrónico (DE), conforme a las condiciones establecidas en el Manual Técnico del SIFEN.
        """)

    with st.expander("¿Cuáles son los Eventos realizados por el Emisor?"):
        st.markdown("""
        **Respuesta:**  
        1. **Inutilización de número de DE:** Es un evento solicitado por el emisor electrónico. Pueden darse tres situaciones:  
           - Saltos en la numeración: Por algún error en el sistema de facturación del emisor, se produce un salto en la numeración.  
           - Detección de errores técnicos (de llenado) en la emisión del DE.  
           - Por rechazo del SIFEN: Cuando un DE ha sido rechazado por el SIFEN y su ajuste implique la modificación del CDC, indefectiblemente esa numeración no utilizada debe ser inutilizada.
        """)

    with st.expander("¿A qué nos referimos cuando hablamos de Eventos del Emisor?"):
        st.markdown("""
        **Respuesta:**  
        Son aquellos eventos originados por el emisor, cuando surge alguna situación que modifica la secuencia numérica o el contenido del Documento Electrónico (DE).
        """)

    with st.expander("¿Cómo se realiza un Evento?"):
        st.markdown("""
        **Respuesta:**  
        - Los eventos deben ser estructurados en un archivo XML por eventos.  
        - Cada evento deberá estar firmado digitalmente.  
        - Los eventos del emisor y receptor deberán ser transmitidos por los Web Services disponibles para dicha gestión.  
        - Los eventos deberán ser enviados en lotes de hasta 15 eventos de cualquier tipo (emisor y/o receptor).  
        - La Inutilización de un número de Documento Electrónico (DE) debe ser solicitada por rango secuencial o correlativo.
        """)

# Mostrar el historial del chat
display_chat_history()

# Entrada de texto para la pregunta del usuario
user_question = st.chat_input("Escribe tu pregunta sobre facturación electrónica:")

if user_question:
    # Mostrar la pregunta del usuario
    st.write(f"**Tú:** {user_question}")
    
    # Añadir la pregunta del usuario al historial del chat
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    # Ejecutar el flujo de trabajo con la pregunta del usuario
    inputs = {"question": user_question}

    # Mostrar un mensaje de carga mientras se procesa la pregunta
    with st.spinner("Procesando tu pregunta..."):
        # Variable para almacenar la respuesta final del bot
        bot_response = ""

        # Recorrer las salidas del flujo de trabajo
        for output in app.stream(inputs):
            for key, value in output.items():
                # Verificar si el valor es un diccionario y contiene "generation"
                if isinstance(value, dict) and "generation" in value:
                    # Concatenar la respuesta generada
                    bot_response += value["generation"] + " "

        # Añadir la respuesta final del bot al historial del chat
        if bot_response:
            st.session_state.chat_history.append({"role": "bot", "content": bot_response.strip()})

    # Recargar la página para limpiar el input
    st.rerun()