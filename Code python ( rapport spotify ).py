import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import time

# Configuration de la page
st.set_page_config(
    page_title="🎵 Rapport Analyse Spotify 2024",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    /* Variables CSS */
    :root {
        --spotify-green: #1DB954;
        --spotify-dark: #191414;
        --spotify-light: #1ed760;
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-spotify: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    }
    
    /* Styles généraux */
    .main > div {
        padding-top: 2rem;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #1DB954 !important;
    }
    
    /* Header principal */
    .main-header {
        background: var(--gradient-spotify);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Cartes KPI */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 200px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-spotify);
    }
    
    .kpi-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1DB954;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .kpi-unit {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: var(--gradient-primary);
    }
    
    /* Métriques Streamlit personnalisées */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    div[data-testid="metric-container"] > label {
        color: #1DB954 !important;
        font-weight: 600 !important;
    }
    
    /* Graphiques */
    .plot-container {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Boutons */
    .stButton > button {
        background: var(--gradient-spotify) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour créer des données simulées réalistes
@st.cache_data
def create_sample_data():
    """Crée des données d'exemple basées sur le rapport"""
    
    # Top 10 chansons
    top_songs = pd.DataFrame({
        'Chanson': [
            'Blinding Lights - The Weeknd',
            'Shape of You - Ed Sheeran', 
            'Watermelon Sugar - Harry Styles',
            'Levitating - Dua Lipa',
            'Bad Habits - Ed Sheeran',
            'Stay - The Kid LAROI & Justin Bieber',
            'Good 4 U - Olivia Rodrigo',
            'Industry Baby - Lil Nas X',
            'Heat Waves - Glass Animals',
            'Peaches - Justin Bieber'
        ],
        'Streams_Spotify': [3200000000, 3100000000, 2800000000, 2600000000, 2400000000, 
                           2200000000, 2000000000, 1900000000, 1800000000, 1700000000],
        'Revenue_USD': [9600000, 9300000, 8400000, 7800000, 7200000, 
                       6600000, 6000000, 5700000, 5400000, 5100000],
        'YouTube_Views': [2800000000, 5600000000, 1200000000, 1800000000, 1500000000,
                         900000000, 1100000000, 800000000, 600000000, 700000000],
        'TikTok_Views': [8500000000, 4200000000, 3800000000, 6200000000, 2900000000,
                        5100000000, 4800000000, 3600000000, 2200000000, 1900000000]
    })
    
    # Données de corrélation TikTok vs Spotify
    correlation_data = pd.DataFrame({
        'TikTok_Views': np.random.lognormal(20, 1.5, 100),
        'Spotify_Streams': np.random.lognormal(19, 1.2, 100)
    })
    
    # Données explicite vs non-explicite
    explicit_data = pd.DataFrame({
        'Type': ['Non-Explicite', 'Explicite'],
        'Streams_Moyens': [420000000, 460000000],
        'Nombre_Chansons': [2800, 1685]
    })
    
    return top_songs, correlation_data, explicit_data

# Fonction pour afficher les KPIs avec animation
def display_kpis():
    """Affiche les KPIs principaux avec un design moderne"""
    
    st.markdown('<div class="main-header animate-fade-in">', unsafe_allow_html=True)
    st.markdown('<h1>🎵 Rapport Analyse Spotify 2024</h1>', unsafe_allow_html=True)
    st.markdown('<p>Analyse complète des tendances musicales et performances multi-plateformes</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # KPIs principaux avec colonnes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎵 Chansons Analysées",
            value="4,485",
            delta="Titres musicaux"
        )
        
    with col2:
        st.metric(
            label="🎧 Écoutes Moyennes",
            value="437.9M",
            delta="Streams Spotify"
        )
        
    with col3:
        st.metric(
            label="💰 Revenu Moyen",
            value="$1.31M",
            delta="USD par titre"
        )
    
    st.markdown("---")
    
    # Deuxième rangée de KPIs
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric(
            label="📱 TikTok Moyennes",
            value="1.14B",
            delta="Vues par contenu"
        )
        
    with col5:
        st.metric(
            label="🎥 YouTube Moyennes", 
            value="396.5M",
            delta="Vues par vidéo"
        )
        
    with col6:
        st.metric(
            label="📻 Portée Playlists",
            value="23.6M",
            delta="Auditeurs Spotify"
        )

# Fonction pour créer le graphique du Top 10
def create_top_songs_chart(data):
    """Crée un graphique moderne du Top 10"""
    
    fig = px.bar(
        data.head(10),
        x='Streams_Spotify',
        y='Chanson',
        orientation='h',
        title='🏆 Top 10 Chansons - Écoutes Spotify',
        color='Streams_Spotify',
        color_continuous_scale='viridis',
        text='Streams_Spotify'
    )
    
    fig.update_layout(
        height=600,
        title_font_size=20,
        title_font_color='#1DB954',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif"),
        yaxis={'categoryorder':'total ascending'}
    )
    
    fig.update_traces(
        texttemplate='%{text:.2s}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )
    
    return fig

# Fonction pour créer le graphique des revenus
def create_revenue_chart(data):
    """Crée un graphique des revenus estimés"""
    
    fig = px.bar(
        data.head(10),
        x='Chanson',
        y='Revenue_USD',
        title='💰 Top 10 Revenus Estimés (Spotify)',
        color='Revenue_USD',
        color_continuous_scale='greens',
        text='Revenue_USD'
    )
    
    fig.update_layout(
        height=500,
        title_font_size=20,
        title_font_color='#1DB954',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif"),
        xaxis_tickangle=-45
    )
    
    fig.update_traces(
        texttemplate='$%{text:.2s}',
        textposition='outside'
    )
    
    return fig

# Fonction pour créer le graphique de corrélation
def create_correlation_chart(data):
    """Crée un scatter plot de corrélation TikTok vs Spotify"""
    
    fig = px.scatter(
        data,
        x='TikTok_Views',
        y='Spotify_Streams',
        title='🔗 Corrélation entre TikTok Views et Spotify Streams',
        trendline='ols',
        opacity=0.7,
        size_max=10
    )
    
    fig.update_layout(
        height=500,
        title_font_size=20,
        title_font_color='#1DB954',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif")
    )
    
    fig.update_traces(
        marker=dict(size=8, color='#1DB954', opacity=0.6)
    )
    
    return fig

# Fonction pour créer le graphique explicite vs non-explicite
def create_explicit_chart(data):
    """Crée un graphique comparatif explicite vs non-explicite"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Streams Moyens',
        x=data['Type'],
        y=data['Streams_Moyens'],
        marker_color=['#1DB954', '#1ed760'],
        text=data['Streams_Moyens'],
        texttemplate='%{text:.2s}',
        textposition='outside'
    ))
    
    fig.update_layout(
        title='🔞 Écoutes Moyennes - Explicite vs Non-explicite',
        height=400,
        title_font_size=20,
        title_font_color='#1DB954',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif"),
        showlegend=False
    )
    
    return fig

# Interface principale
def main():
    """Fonction principale de l'application"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        
        page = st.selectbox(
            "Choisir une section:",
            ["📊 Vue d'ensemble", "🏆 Top Chansons", "💰 Revenus", "📱 Corrélations", "🔞 Analyse Contenu"]
        )
        
        st.markdown("---")
        st.markdown("### 📈 Filtres")
        
        # Slider pour filtrer les données
        top_n = st.slider("Nombre de chansons à afficher:", 5, 20, 10)
        
        # Bouton de refresh
        if st.button("🔄 Actualiser les données"):
            st.cache_data.clear()
            st.experimental_rerun()
    
    # Chargement des données
    top_songs, correlation_data, explicit_data = create_sample_data()
    
    # Affichage selon la page sélectionnée
    if page == "📊 Vue d'ensemble":
        display_kpis()
        
        # Graphiques en colonnes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)
            fig1 = create_top_songs_chart(top_songs)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)
            fig2 = create_revenue_chart(top_songs)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "🏆 Top Chansons":
        st.markdown("## 🏆 Classement des Chansons")
        
        # Tableau interactif
        st.dataframe(
            top_songs.head(top_n),
            use_container_width=True,
            hide_index=True
        )
        
        # Graphique
        fig = create_top_songs_chart(top_songs.head(top_n))
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "💰 Revenus":
        st.markdown("## 💰 Analyse des Revenus")
        
        # Métriques de revenus
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenus Top 10", f"${top_songs['Revenue_USD'].head(10).sum():,.0f}")
        with col2:
            st.metric("Revenu Moyen", f"${top_songs['Revenue_USD'].mean():,.0f}")
        with col3:
            st.metric("Revenu Maximum", f"${top_songs['Revenue_USD'].max():,.0f}")
        
        fig = create_revenue_chart(top_songs.head(top_n))
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "📱 Corrélations":
        st.markdown("## 📱 Analyse des Corrélations")
        
        # Calcul de la corrélation
        corr_coef = np.corrcoef(correlation_data['TikTok_Views'], correlation_data['Spotify_Streams'])[0,1]
        
        st.info(f"📊 Coefficient de corrélation TikTok-Spotify: **{corr_coef:.3f}**")
        
        fig = create_correlation_chart(correlation_data)
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "🔞 Analyse Contenu":
        st.markdown("## 🔞 Contenu Explicite vs Non-Explicite")
        
        # Métriques comparatives
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Streams Non-Explicite", "420M", "Moyenne")
        with col2:
            st.metric("Streams Explicite", "460M", "+9.5% vs Non-Explicite")
        
        fig = create_explicit_chart(explicit_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p>🎼 Rapport généré avec Streamlit • Données Spotify Analytics 2024</p>
            <p style='font-size: 0.8rem; opacity: 0.8;'>
                4,485 chansons analysées • Multi-plateformes • Insights en temps réel
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()