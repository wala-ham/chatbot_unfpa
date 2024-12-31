import matplotlib.pyplot as plt
from vertexai.generative_models import GenerationConfig, GenerativeModel
import re
import streamlit as st


def needs_graphic(query, response):
    """Détermine si un graphique est nécessaire."""

    # Initialize the Gemini model
    MODEL_ID = "gemini-2.0-flash-exp" 
    model = GenerativeModel(MODEL_ID)

    # Construct a prompt to guide Gemini's analysis
    prompt = f"""
    Requête : {query}
    Réponse : {response}

    Considering the query and response above, would a graph be helpful to visualize the information? 
    Answer with a concise explanation of your reasoning.
    """

    # Generate a response from Gemini
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="text/plain" 
        )
    )

    # Analyze Gemini's response
    gemini_response = response.text.lower()

    # Keywords for comparisons, trends, or multiple data points
    comparison_keywords = ["compare", "contrast", "difference", "similar", "greater than", "less than", "versus"]
    trend_keywords = ["trend", "growth", "decline", "increase", "decrease", "fluctuate", "change over time"]
    distribution_keywords = ["distribution", "spread", "range", "percentage", "proportion", "average"]

    # Check if the query or response involves comparisons, trends, distributions, or numerical breakdowns
    if any(keyword in query.lower() for keyword in comparison_keywords) or \
       any(keyword in query.lower() for keyword in trend_keywords) or \
       any(keyword in query.lower() for keyword in distribution_keywords) or \
       any(keyword in gemini_response for keyword in comparison_keywords) or \
       any(keyword in gemini_response for keyword in trend_keywords) or \
       any(keyword in gemini_response for keyword in distribution_keywords):
        return True

    # If the response includes multiple numerical values or categories, suggest a graph
    if len([word for word in response.text.split() if word.isdigit()]) > 3:
        return True

    # If no clear indication is found, assume no graph is needed
    return False

def generate_graphic(query, response):
    """Génère un graphique et permet de le télécharger avec une flèche indiquant le téléchargement."""
    
    # Initialisation du modèle Gemini
    MODEL_ID = "gemini-2.0-flash-exp"  
    model = GenerativeModel(MODEL_ID)
    
    # Création du prompt pour guider la génération du graphique
    prompt = f"""
    Requête : {query}
    Réponse : {response}

    Générer un extrait de code Python utilisant matplotlib pour créer un graphique 
    représentant les données dans la réponse. Assurez-vous que le graphique soit 
    précis, avec des axes étiquetés, un titre et une légende si nécessaire.
    """
    
    # Génération de la réponse du modèle Gemini
    response_from_gemini = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="text/plain" 
        )
    )
    
    # Récupération du texte généré
    generated_text = response_from_gemini.text
    
    # Affichage du texte généré pour vérification
    print(f"Generated response from Gemini: {generated_text}")
    
    # Utilisation d'une expression régulière pour extraire le code Python
    match = re.search(r'```python(.*?)```', generated_text, re.DOTALL)
    
    if match:
        # Récupération du code Python extrait
        code_snippet = match.group(1).strip()
        
        # Affichage du code pour vérification
        print(f"Code généré :\n{code_snippet}")
        
        try:
            # Vérification de la syntaxe avant l'exécution
            compile(code_snippet, "<string>", "exec")
            
            # Exécution du code généré
            exec(code_snippet)
            
            # Sauvegarde du graphique 
            image_path = 'generated_graph.png'
            plt.savefig(image_path)  
            
            # Affichage du graphique dans l'interface
            st.image(image_path, caption="Graphique généré")
            
            # Affichage de l'icône de téléchargement sous l'image avec une flèche
            st.markdown(f"""
            <div style="text-align:center;">
                <a href="data:file/png;base64,{get_file_base64(image_path)}" download="generated_graph.png">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Arrow_down_icon.svg" alt="Download" width="50">
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            return code_snippet
        except SyntaxError as e:
            print(f"Erreur de syntaxe : {e}")
            return None
        except Exception as e:
            print(f"Erreur lors de l'exécution du code : {e}")
            return None
    else:
        print("Aucun code Python valide trouvé.")
        return None

def get_file_base64(file_path):
    """Convertit un fichier en base64 pour une utilisation dans un lien de téléchargement."""
    import base64
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()
