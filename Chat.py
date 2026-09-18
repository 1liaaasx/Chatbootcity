import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections

# -------------------------------------------------------------
# Configuration de la page
# -------------------------------------------------------------
st.set_page_config(
    page_title="Morocco Travel AI",
    page_icon="🇲🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Base de connaissances du Chatbot (NLTK)
# -------------------------------------------------------------
pairs = [
    [r"mon nom est (.*)", ["Enchanté %1 ! Prêt à explorer le Maroc avec moi ?"]],
    [r"bonjour|salut|coucou|salam", [
        "Salam ! Prêt à découvrir les merveilles du Maroc ?",
        "Bonjour ! Quelle destination marocaine t'intéresse aujourd'hui ?"
    ]],
    [r"(.*)capitale(.*)", ["La capitale administrative et politique du Maroc est Rabat."]],
    [r"(.*)marrakech(.*)", ["Marrakech, la ville ocre ! Célèbre pour sa médina, la place Jemaa el-Fna, les jardins Majorelle et ses souks vivants."]],
    [r"(.*)casablanca(.*)", ["Casablanca est la capitale économique du pays, réputée pour sa spectaculaire Mosquée Hassan II bâtie sur l'océan."]],
    [r"(.*)chefchaouen(.*)", ["Chefchaouen, la perle bleue nichée dans les montagnes du Rif, idéale pour des balades relaxantes et des photos superbes."]],
    [r"(.*)agadir(.*)", ["Agadir est parfaite pour le soleil toute l'année, sa corniche animée, ses plages dorées et ses spots de surf."]],
    [r"(.*)safi(.*)", ["Safi est renommée pour sa poterie artisanale réputée mondialement, sa colline des potiers et son riche passé atlantique."]],
    [r"(.*)essaouira(.*)", ["Essaouira (l'ancienne Mogador) séduit par ses remparts maritimes, son festival Gnaoua, ses galeries d'art et son vent parfait pour le kitesurf."]],
    [r"(.*)monument(.*)", ["Parmi les monuments incontournables : la Mosquée Hassan II, la Koutoubia à Marrakech, la Tour Hassan à Rabat, et Volubilis."]],
    [r"(.*)desert(.*)", ["Le désert marocain offre des paysages féeriques, notamment les majestueuses dunes de Merzouga (Erg Chebbi) et de Zagora (Erg Chigaga)."]],
    [r"(.*)montagne(.*)", ["Le Maroc abrite de superbes massifs : le Haut Atlas (avec le mont Toubkal à 4 167 m), le Moyen Atlas et la chaîne du Rif."]],
    [r"(.*)cuisine(.*)|(.*)manger(.*)|(.*)plat(.*)", ["La gastronomie marocaine est un régal : couscous du vendredi, tajines mijotés, pastilla aux amandes ou fruits de mer, et le thé à la menthe."]],
    [r"(.*)meilleure destination(.*)", ["Tout dépend de tes envies : Marrakech pour l'ambiance et la culture, Agadir ou Taghazout pour la mer, et Merzouga pour les nuits sous les étoiles."]],
    [r"merci(.*)", ["Avec grand plaisir ! N'hésite pas si tu as d'autres questions sur le Maroc. 🇲🇦"]],
    [r"au revoir|bye|quitter", ["Au revoir et excellent séjour au Maroc ! À très bientôt."]],
    [r"(.*)", ["Je ne suis pas sûr de saisir. Pose-moi une question sur une ville, un plat traditionnel ou un monument marocain !"]]
]

chatbot = Chat(pairs, reflections)

# Comptes utilisateurs de démo (À remplacer par une DB ou hash sécurisé en prod)
USER_CREDENTIALS = {
    "admin": "admin123",
    "visiteur": "maroc2026"
}

# -------------------------------------------------------------
# Gestion de l'état (Session State)
# -------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Marhaban ! Je suis votre guide virtuel. Que souhaitez-vous découvrir au Maroc ?"}
    ]

# -------------------------------------------------------------
# Fonctions d'authentification
# -------------------------------------------------------------
def login():
    st.markdown("<h2 style='text-align: center;'>🇲🇦 Morocco Explorer AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Connectez-vous pour accéder à votre guide touristique personnalisé</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form", clear_on_submit=False):
            username_input = st.text_input("Nom d'utilisateur", placeholder="admin ou visiteur")
            password_input = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Se connecter", use_container_width=True)

            if submit:
                if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
                    st.session_state.authenticated = True
                    st.session_state.username = username_input
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Veuillez réessayer.")

        st.info("💡 **Comptes de test disponibles :**\n- `admin` / `admin123`\n- `visiteur` / `maroc2026`")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.messages = [
        {"role": "assistant", "content": "Marhaban ! Je suis votre guide virtuel. Que souhaitez-vous découvrir au Maroc ?"}
    ]
    st.rerun()

# -------------------------------------------------------------
# Interface Principale du Chatbot
# -------------------------------------------------------------
def chat_interface():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"### 👋 Bonjour, **{st.session_state.username.capitalize()}** !")
        st.caption("Session active")
        
        st.markdown("---")
        st.markdown("#### 💡 Suggestions rapides")
        
        suggestions = [
            "Que faire à Marrakech ?",
            "Parle-moi de Casablanca",
            "Quels sont les plats typiques ?",
            "Parle-moi du désert",
            "Quels monuments visiter ?"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, use_container_width=True):
                # Ajoute la suggestion directement dans la discussion
                st.session_state.messages.append({"role": "user", "content": suggestion})
                bot_reply = chatbot.respond(suggestion)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.rerun()

        st.markdown("---")
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Historique réinitialisé ! Quelle destination vous intéresse ?"}
            ]
            st.rerun()

        if st.button("🚪 Déconnexion", use_container_width=True, type="secondary"):
            logout()

    # --- Fenêtre principale du Chat ---
    st.title("🇲🇦 Guide Touristique Virtuel du Maroc")
    st.markdown("Posez vos questions sur les villes, la gastronomie, les montagnes ou le patrimoine marocain.")

    # Affichage des messages historiques
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Zone de saisie (Chat Input)
    if prompt := st.chat_input("Écrivez votre question ici... (ex: Parle-moi d'Essaouira)"):
        # Affichage du message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Génération de la réponse
        bot_reply = chatbot.respond(prompt)
        if not bot_reply:
            bot_reply = "Je ne comprends pas encore cette demande. Pose-moi une question sur le tourisme au Maroc !"

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# -------------------------------------------------------------
# Point d'entrée
# -------------------------------------------------------------
if not st.session_state.authenticated:
    login()
else:
    chat_interface()