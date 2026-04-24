import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Asistente Matemático", page_icon="🧮")

st.title("🍎 Profesor de Matemáticas IA")
st.markdown("""
Bienvenido. Soy un agente especializado en resolver problemas matemáticos 
utilizando notación profesional en **LaTeX**.
""")

# Configura tu API Key de Groq (la guardaremos en los secretos de Streamlit más adelante)
# Para probar localmente puedes ponerla directamente, pero no la subas a GitHub
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu problema matemático aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del Agente
    with st.chat_message("assistant"):
        mensaje_placeholder = st.empty()
        full_response = ""
        
        # Instrucción del sistema para que use LaTeX
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un experto profesor de matemáticas. "
                               "IMPORTANTE: Siempre que escribas fórmulas matemáticas, "
                               "utiliza el formato LaTeX entre símbolos de dólar doble $$ para bloques "
                               "o simple $ para fórmulas en línea. Explica paso a paso."
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