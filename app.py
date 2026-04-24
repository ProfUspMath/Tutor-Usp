import streamlit as st
from groq import Groq

# 1. Configuración de la página (Siempre debe ser lo primero)
st.set_page_config(page_title="Asistente Matemático", page_icon="🧮")

st.title("🍎 Profesor de Matemáticas IA")
st.markdown("""
Bienvenido. Soy un agente especializado en resolver problemas matemáticos 
utilizando notación profesional en **LaTeX**.
""")

# 2. Inicialización segura del cliente
# Usamos .get para que la app no explote si no encuentra la llave
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ Error: No se encontró la variable 'GROQ_API_KEY' en los Secrets de Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada del usuario
if prompt := st.chat_input("Escribe tu problema matemático aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del Agente
    with st.chat_message("assistant"):
        mensaje_placeholder = st.empty()
        full_response = ""
        
        try:
            # Petición a la API
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un experto profesor de matemáticas. "
                                   "IMPORTANTE: Siempre que escribas fórmulas matemáticas, "
                                   "utiliza el formato LaTeX entre símbolos de dólar $$ para bloques "
                                   "o $ para fórmulas en línea. Explica paso a paso."
                    },
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    mensaje_placeholder.markdown(full_response + "▌")
            
            mensaje_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Se produjo un error al conectar con Groq: {e}")
            # Esto nos dirá si es un error 401 (llave mal), 429 (límite de uso) o 500 (caída)
