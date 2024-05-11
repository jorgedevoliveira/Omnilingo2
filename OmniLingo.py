import streamlit as st
import google.generativeai as genai

# Configurando a API Key do GEMINI AI
genai.configure(api_key="AIzaSyCk282dAS15LSTOU7GOjsmWOkoFhmMoUlI")


# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
]

system_instruction = "Responda como um professor de idiomas, \nna primeira resposta, solicite o idioma que a pessoa quer praticar e que para encerrar do chat basta digitar sair,\nresponda no idioma pt-br e no idioma solicitado no promp\nse o prompt não for relacionado a idiomas solicite uma pergunta sobre idioma\n"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

# Função para interação com o chatbot

def main():
    st.title("Omnilingo - Chatbot poliglota com Gemini AI")
    st.markdown("Este é um chatbot alimentado por GEMINI AI, onde você pode praticar idiomas.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat()  

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(""):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.chat.send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

        with st.chat_message("assistant"):
            st.markdown(response.text)

if __name__ == "__main__":
    main()
