import streamlit as st
from chatbot.core import app  # Importa el flujo de trabajo compilado

# Título de la aplicación
st.title("Chatbot de Soporte Técnico sobre Facturación Electrónica")

# Entrada de texto para la pregunta del usuario
user_question = st.text_input("Escribe tu pregunta sobre facturación electrónica:")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if user_question:
        # Ejecutar el flujo de trabajo con la pregunta del usuario
        inputs = {"question": user_question}
        
        # Mostrar un mensaje de carga mientras se procesa la pregunta
        with st.spinner("Procesando tu pregunta..."):
            # Recorrer las salidas del flujo de trabajo
            for output in app.stream(inputs):
                for key, value in output.items():
                    st.write(f"Finished running: {key}")
                    # Verificar si el valor es un diccionario y contiene "generation"
                    if isinstance(value, dict) and "generation" in value:
                        # Mostrar la respuesta generada
                        st.success("Respuesta generada:")
                        st.write(value["generation"])
    else:
        st.warning("Por favor, escribe una pregunta.")