import streamlit as st
import requests

st.title("Chatbot AI")

user_input = st.text_input("Ketik pesan:", "")

if st.button("Kirim"):
    try:
        response = requests.post("https://chatbot-production-22e9.up.railway.app/", json={"user_input": user_input})
        chatbot_response = response.json().get("response", "Error: No response received")
        st.write("Chatbot:", chatbot_response)
    except requests.exceptions.ConnectionError:
        st.write("Error: Tidak dapat terhubung ke server Flask. Pastikan backend berjalan.")
