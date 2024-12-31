import streamlit as st
from retrieval_agent import retrieve_chunks
from response_agent import generate_response
from visualization_agent import needs_graphic, generate_graphic

# --- Interface Streamlit ---
st.title("Chat with Gemini")

# Initialiser l'état de la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone d'entrée pour l'utilisateur
query = st.chat_input("Posez une question ici...")

# Si l'utilisateur pose une question
if query:
    # Ajouter la requête utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Récupérer des documents pertinents (chunks)
    chunks = retrieve_chunks(query)
    combined_input = " ".join([chunk["chunk"] for chunk in chunks]) if chunks else query

    # Générer une réponse à partir du modèle
    response = generate_response(query, combined_input)
    
    # Afficher la réponse du modèle
    with st.chat_message("assistant"):
        st.markdown(response)

        # Vérifier si un graphique est nécessaire
        if needs_graphic(query, response):
            st.write("A graphic is required. Generating...")
            code_snippet = generate_graphic(query, response)
            if code_snippet:
                st.write("Generated Python Code for the Graphic:")
                st.code(code_snippet, language="python")
                st.image("generated_graph.png", caption="Generated Graphic")
            else:
                st.error("Failed to generate a graphic.")
        else:
            st.write("No graphic is needed for this response.")

    # Ajouter la réponse du modèle à l'historique des messages
    st.session_state.messages.append({"role": "assistant", "content": response})

