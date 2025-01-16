import streamlit as st
import json

# Configurazione tema
st.set_page_config(
    page_title="Business Plan App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funzione per inizializzare lo stato della sessione se non esiste
def initialize_session_state():
    fields = [
        'nome_azienda', 'motivazione_bp', 'nome_prodotto', 'mercato_target',
        'strategia_marketing', 'piano_operativo', 'canali_distribuzione',
        'budget_marketing', 'nome_fondatore', 'ruolo_fondatore',
        'sito_web', 'budget_marketing',
        'stato_azienda', 'descrizione_attivita', 'contesto_aziendale',
        'storia_aziendale', 'obiettivi_aziendali'
    ]
    
    for field in fields:
        if field not in st.session_state:
            st.session_state[field] = ""
    
    if 'budget_marketing' not in st.session_state or not isinstance(st.session_state['budget_marketing'], (int, float)):
        st.session_state['budget_marketing'] = 0
    
    if 'stato_azienda' not in st.session_state or st.session_state['stato_azienda'] not in ["Esistente", "Da Creare"]:
        st.session_state['stato_azienda'] = "Esistente"

# Calcola il progresso di compilazione
def calculate_progress():
    required_fields = [
        'nome_azienda', 'motivazione_bp', 'descrizione_attivita', 'nome_prodotto',
        'mercato_target', 'strategia_marketing', 'piano_operativo',
        'canali_distribuzione', 'team_members'
    ]
    
    completed = 0
    for field in required_fields:
        if field == 'team_members':
            # Check if at least one team member has been added with required fields
            if (st.session_state.get('team_members') and
                any(member['nome'].strip() and member['ruolo'].strip()
                    for member in st.session_state['team_members'])):
                completed += 1
        else:
            if st.session_state.get(field, "").strip():
                completed += 1
    
    return completed / len(required_fields)

st.title("Raccolta Informazioni Business Plan")

initialize_session_state()

# Mostra progresso compilazione nella sidebar
st.sidebar.markdown("### Progresso Compilazione")
progress_value = calculate_progress()
st.sidebar.progress(progress_value)
st.sidebar.caption(f"Completamento: {int(progress_value*100)}%")

# Mostra indicatori per ogni tab
st.sidebar.markdown("**Completamento Sezioni:**")
tabs = {
    "Informazioni Generali": ['nome_azienda', 'motivazione_bp'],
    "Prodotto/Servizio": ['nome_prodotto'],
    "Analisi di Mercato": ['mercato_target'],
    "Strategia": ['strategia_marketing', 'piano_operativo', 'canali_distribuzione'],
    "Team": ['nome_fondatore', 'ruolo_fondatore', 'esperiencia_team']
}

for tab_name, fields in tabs.items():
    completed = sum(1 for f in fields if st.session_state.get(f, "").strip())
    total = len(fields)
    st.sidebar.markdown(f"- {tab_name}: {'✅' if completed == total else '🟡'} ({completed}/{total})")

# Mostra progresso compilazione nella sidebar
progress_value = calculate_progress()
st.sidebar.markdown("---")
st.sidebar.markdown(f"### Progresso Compilazione: {int(progress_value*100)}%")
st.sidebar.progress(progress_value)

# Aggiungi istruzioni per la navigazione
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-right: 4px;
        padding-left: 4px;
        white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("⬅️ Scorri le schede a destra e sinistra per vedere tutte le sezioni ➡️")

# Crea tabs per ogni sezione
tab_info_generali, tab_allegati_iniziali, tab_prodotto_servizio, \
tab_analisi_mercato, tab_strategia, tab_team, tab_piano_finanziario = \
    st.tabs(["📋 Informazioni Generali", "📎 Allegati Iniziali", "🛠️ Prodotto/Servizio",
             "📊 Analisi di Mercato", "🎯 Strategia", "👥 Team", "💰 Piano Finanziario"])

# Contenuto per ogni tab
with tab_info_generali:
    st.header("📋 Informazioni Generali dell'Azienda")
    
    col1, col2 = st.columns(2)
    with col1:
        nome_azienda = st.text_input("Nome dell'Azienda *",
                                  key="tab1_nome_azienda",
                                  placeholder="Es. InnovaTech Srl")
        if not nome_azienda.strip():
            st.error("Il nome dell'azienda è obbligatorio")
        
        forma_giuridica = st.selectbox("Forma Giuridica *",
                                    ["Seleziona...", "Individuale", "Società di Persone",
                                     "Società di Capitali", "Altro"],
                                    key="tab1_forma_giuridica")
    
    with col2:
        email = st.text_input("Email Aziendale *",
                           key="tab1_email",
                           placeholder="esempio@azienda.com")
        if email and "@" not in email:
            st.error("Inserisci un indirizzo email valido")
        
        stato_azienda = st.radio("Stato Azienda",
                              ["Esistente", "Da Creare"],
                              key="tab1_stato_azienda")
    
    motivazione = st.text_area("Motivazione alla Creazione di questo Business Plan *",
                            key="tab1_motivazione_bp",
                            placeholder="Es. Stiamo cercando finanziamenti seed per espandere il nostro team...")
    if not motivazione.strip():
        st.error("La motivazione è obbligatoria")

with tab_allegati_iniziali:
    st.header("📎 Allegati Iniziali")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Documenti Ufficiali")
        visura = st.file_uploader("Carica Visura Camerale",
                               key="tab2_visura",
                               accept_multiple_files=False,
                               type=['pdf'])
    
    with col2:
        st.subheader("Business Plan Esistenti")
        business_plan = st.file_uploader("Carica Business Plan",
                                     key="tab2_business_plan",
                                     accept_multiple_files=True,
                                     type=['pdf', 'doc', 'docx'])

with tab_prodotto_servizio:
    st.header("🛠️ Prodotto o Servizio")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome del Prodotto/Servizio *",
                    key="tab3_nome_prodotto",
                    placeholder="Es. Software di gestione progetti")
    
    with col2:
        st.text_input("Prezzo Indicativo",
                    key="tab3_prezzo",
                    placeholder="Es. €99/mese")
    
    st.text_area("Descrizione Dettagliata *",
               key="tab3_descrizione",
               placeholder="Descrivi le funzionalità principali...")

with tab_analisi_mercato:
    st.header("📊 Analisi di Mercato")
    
    st.text_area("Descrizione del Mercato *",
               key="tab4_mercato",
               placeholder="Descrivi il mercato di riferimento...")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Punti di Forza",
                   key="tab4_forza",
                   placeholder="Elenca i punti di forza...")
    with col2:
        st.text_area("Punti di Debolezza",
                   key="tab4_debolezza",
                   placeholder="Elenca i punti di debolezza...")

with tab_strategia:
    st.header("🎯 Strategia e Implementazione")
    
    st.text_area("Strategia di Marketing",
               key="tab5_marketing",
               placeholder="Descrivi la tua strategia di marketing...")
    st.text_area("Piano Operativo",
               key="tab5_operativo",
               placeholder="Descrivi il piano operativo...")
    st.text_input("Canali di Distribuzione",
                key="tab5_canali",
                placeholder="Es. E-commerce, negozi fisici...")

with tab_team:
    st.header("👥 Team di Gestione")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome Fondatore",
                    key="tab6_nome",
                    placeholder="Nome e cognome del fondatore")
    with col2:
        st.text_input("Ruolo",
                    key="tab6_ruolo",
                    placeholder="Es. CEO, CTO...")
    
    st.text_area("Esperienza",
               key="tab6_esperienza",
               placeholder="Descrivi l'esperienza del team...")

with tab_piano_finanziario:
    st.header("💰 Piano Finanziario")
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Budget Marketing (€)",
                     key="tab7_budget",
                     min_value=0,
                     step=1000)
    with col2:
        st.number_input("Investimento Iniziale (€)",
                     key="tab7_investimento",
                     min_value=0,
                     step=5000)
    
    st.text_area("Proiezioni Finanziarie",
               key="tab7_proiezioni",
               placeholder="Descrivi le proiezioni finanziarie...")

# Definisci l'ordine delle sezioni
SECTIONS = ["Informazioni Generali", "Allegati Iniziali", "Prodotto/Servizio",
           "Analisi di Mercato", "Strategia e Implementazione",
           "Team di Gestione", "Piano Finanziario"]


st.markdown("---")

with tab_info_generali:
    st.header("Informazioni Generali dell'Azienda")
    
    # Nome azienda con validazione
    nome_azienda = st.text_input("Nome dell'Azienda *", key="nome_azienda",
                               placeholder="Es. InnovaTech Srl")
    if not nome_azienda.strip():
        st.error("Il nome dell'azienda è obbligatorio")
    
    # Motivazione con validazione
    motivazione = st.text_area("Motivazione alla Creazione di questo Business Plan *",
                             key="motivazione_bp",
                             placeholder="Es. Stiamo cercando finanziamenti seed per espandere il nostro team...",
                             help="Spiega perché stai redigendo questo business plan.")
    if not motivazione.strip():
        st.error("La motivazione è obbligatoria")
    
    # Forma giuridica con campi condizionali
    forma_giuridica = st.selectbox("Forma Giuridica *",
                                 ["Seleziona...", "Individuale", "Società di Persone",
                                  "Società di Capitali", "Altro"],
                                 key="forma_giuridica")
    
    if forma_giuridica == "Società di Capitali":
        st.subheader("Informazioni Specifiche per Società di Capitali")
        partita_iva = st.text_input("Partita IVA *", key="partita_iva",
                                  placeholder="Inserisci la partita IVA")
        if partita_iva and (len(partita_iva) != 11 or not partita_iva.isdigit()):
            st.error("La partita IVA deve essere composta da 11 cifre")
        
        capitale_sociale = st.number_input("Capitale Sociale (€) *",
                                        key="capitale_sociale",
                                        min_value=0.0,
                                        step=1000.0)
        if capitale_sociale <= 0:
            st.error("Il capitale sociale deve essere maggiore di 0")
    
    # Email validation
    email = st.text_input("Email Aziendale *", key="email_aziendale",
                        placeholder="esempio@azienda.com")
    if email and "@" not in email:
        st.error("Inserisci un indirizzo email valido")
    
    # Stato azienda
    stato_azienda = st.radio("Stato Azienda",
                           ["Esistente", "Da Creare"],
                           key="stato_azienda",
                           help="Seleziona se l'azienda è già esistente o se deve essere creata")
    
    # Descrizione attività
    st.text_area("Descrizione Attività *",
                key="descrizione_attivita",
                placeholder="Descrivi in dettaglio cosa fa l'azienda, i suoi prodotti/servizi principali...",
                help="Fornisci una descrizione completa dell'attività dell'azienda")
    
    # Contesto aziendale
    st.text_area("Contesto Aziendale",
                key="contesto_aziendale",
                placeholder="Descrivi il contesto in cui opera l'azienda (settore, mercato, tendenze...)",
                help="Fornisci informazioni sul contesto in cui opera l'azienda")
    
    # Storia aziendale
    if stato_azienda == "Esistente":
        st.text_area("Storia Aziendale",
                    key="storia_aziendale",
                    placeholder="Descrivi la storia dell'azienda (anno di fondazione, tappe importanti, evoluzione...)",
                    help="Fornisci informazioni sulla storia dell'azienda")
    
    # Obiettivi
    st.text_area("Obiettivi Aziendali",
                key="obiettivi_aziendali",
                placeholder="Descrivi gli obiettivi a breve e lungo termine dell'azienda...",
                help="Fornisci informazioni sugli obiettivi aziendali")

with tab_allegati_iniziali:
    st.header("Allegati Iniziali")
    
    st.subheader("Documenti Ufficiali")
    visura = st.file_uploader("Carica Visura Camerale",
                            accept_multiple_files=False,
                            type=['pdf'],
                            help="Carica la visura camerale in formato PDF")
    
    st.subheader("Business Plan Esistenti")
    business_plan = st.file_uploader("Carica Business Plan Esistenti",
                                   accept_multiple_files=True,
                                   type=['pdf', 'doc', 'docx'],
                                   help="Puoi caricare business plan esistenti in formato PDF o Word")
    
    st.subheader("Immagini Sito Web")
    col1, col2 = st.columns(2)
    with col1:
        sito_azienda = st.file_uploader("Screenshot Sito Aziendale",
                                      accept_multiple_files=True,
                                      type=['png', 'jpg', 'jpeg'],
                                      help="Carica screenshot del sito aziendale")
    with col2:
        sito_concorrenti = st.file_uploader("Screenshot Siti Concorrenti",
                                          accept_multiple_files=True,
                                          type=['png', 'jpg', 'jpeg'],
                                          help="Carica screenshot dei siti dei concorrenti")
    
    # Mostra anteprima file caricati
    if visura or business_plan or sito_azienda or sito_concorrenti:
        st.subheader("Anteprima Allegati")
        if visura:
            st.write(f"Visura caricata: {visura.name}")
        if business_plan:
            for bp in business_plan:
                st.write(f"Business Plan: {bp.name}")
        if sito_azienda:
            for img in sito_azienda:
                st.image(img, caption=f"Screenshot sito aziendale: {img.name}")
        if sito_concorrenti:
            for img in sito_concorrenti:
                st.image(img, caption=f"Screenshot sito concorrente: {img.name}")

with tab_prodotto_servizio:
    st.header("Prodotto o Servizio")
    
    if 'prodotti' not in st.session_state:
        st.session_state.prodotti = [{
            'nome': '',
            'descrizione': '',
            'immagine': None
        }]
    
    for i, prodotto in enumerate(st.session_state.prodotti):
        with st.expander(f"Prodotto/Servizio #{i+1}" if i > 0 else "Primo Prodotto/Servizio"):
            # Nome prodotto
            st.text_input("Nome del Prodotto/Servizio *",
                         key=f"prodotto_{i}_nome",
                         value=prodotto['nome'],
                         placeholder="Es. Software di gestione progetti 'ProjectZen'")
            
            # Descrizione prodotto
            st.text_area("Descrizione Dettagliata *",
                       key=f"prodotto_{i}_descrizione",
                       value=prodotto['descrizione'],
                       placeholder="Descrivi le funzionalità principali, come funziona, i materiali utilizzati, ecc.",
                       help="Fornisci una descrizione completa del tuo prodotto o servizio.")
            
            # Immagine prodotto
            uploaded_file = st.file_uploader(f"Carica immagine del prodotto #{i+1}",
                                           type=['png', 'jpg', 'jpeg'],
                                           key=f"prodotto_{i}_immagine")
            if uploaded_file:
                st.image(uploaded_file, caption=f"Anteprima immagine prodotto #{i+1}")
                st.session_state.prodotti[i]['immagine'] = uploaded_file
            
            st.markdown("---")
            
        # Aggiungi nuovo prodotto
        if i == len(st.session_state.prodotti) - 1:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Aggiungi Altro Prodotto/Servizio"):
                    st.session_state.prodotti.append({
                        'nome': '',
                        'descrizione': '',
                        'immagine': None
                    })
                    st.rerun()
            with col2:
                if len(st.session_state.prodotti) > 1:
                    if st.button("❌ Rimuovi Ultimo Prodotto"):
                        st.session_state.prodotti.pop()
                        st.rerun()

with tab_analisi_mercato:
    st.header("Analisi di Mercato")
    
    # Analisi generale
    st.subheader("Analisi Generale")
    analisi_mercato = st.text_area("Descrizione del Mercato *",
                                 placeholder="Descrivi il mercato di riferimento, dimensioni, tendenze, ecc.",
                                 help="Fornisci una panoramica completa del mercato")
    
    # Concorrenti
    st.subheader("Analisi della Concorrenza")
    
    if 'concorrenti' not in st.session_state:
        st.session_state.concorrenti = [{
            'nome': '',
            'url': '',
            'note': ''
        }]
    
    for i, concorrente in enumerate(st.session_state.concorrenti):
        with st.expander(f"Concorrente #{i+1}" if i > 0 else "Primo Concorrente"):
            cols = st.columns([3, 5, 4])
            with cols[0]:
                st.text_input("Nome Concorrente *",
                            key=f"concorrente_{i}_nome",
                            value=concorrente['nome'],
                            placeholder="Nome del concorrente")
            with cols[1]:
                st.text_input("URL Sito Web",
                            key=f"concorrente_{i}_url",
                            value=concorrente['url'],
                            placeholder="Inserisci l'URL del sito")
            with cols[2]:
                st.text_area("Note",
                           key=f"concorrente_{i}_note",
                           value=concorrente['note'],
                           placeholder="Inserisci note aggiuntive")
        
        # Aggiungi/Rimuovi concorrenti
        if i == len(st.session_state.concorrenti) - 1:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Aggiungi Altro Concorrente"):
                    st.session_state.concorrenti.append({
                        'nome': '',
                        'url': '',
                        'note': ''
                    })
                    st.rerun()
            with col2:
                if len(st.session_state.concorrenti) > 1:
                    if st.button("❌ Rimuovi Ultimo Concorrente"):
                        st.session_state.concorrenti.pop()
                        st.rerun()
    
    # SWOT Analysis
    st.subheader("Analisi SWOT")
    col1, col2 = st.columns(2)
    with col1:
        punti_di_forza = st.text_area("Punti di Forza",
                                    placeholder="Inserisci i punti di forza della tua azienda")
        opportunita = st.text_area("Opportunità",
                                 placeholder="Inserisci le opportunità del mercato")
    with col2:
        punti_di_debolezza = st.text_area("Punti di Debolezza",
                                        placeholder="Inserisci i punti di debolezza della tua azienda")
        minacce = st.text_area("Minacce",
                             placeholder="Inserisci le minacce del mercato")

with tab_strategia:
    st.header("Strategia e Implementazione")
    st.text_area("Strategia di Marketing", key="strategia_marketing",
                placeholder="Descrivi la tua strategia di marketing...")
    st.text_area("Piano Operativo", key="piano_operativo",
                placeholder="Descrivi il piano operativo...")
    st.text_input("Canali di Distribuzione", key="canali_distribuzione",
                 placeholder="Es. E-commerce, negozi fisici...")
    st.number_input("Budget Marketing (€)", key="budget_marketing",
                   min_value=0, step=1000)

with tab_team:
    st.header("Team di Gestione")
    
    if 'team_members' not in st.session_state:
        st.session_state.team_members = [{
            'nome': '',
            'ruolo': '',
            'esperienza': ''
        }]
    
    for i, member in enumerate(st.session_state.team_members):
        with st.expander(f"Membro del Team #{i+1}" if i > 0 else "Primo Membro del Team"):
            cols = st.columns([2, 2, 4])
            with cols[0]:
                st.text_input("Nome e Cognome",
                            key=f"team_member_{i}_nome",
                            value=member['nome'],
                            placeholder="Nome e cognome")
            with cols[1]:
                st.text_input("Ruolo",
                            key=f"team_member_{i}_ruolo",
                            value=member['ruolo'],
                            placeholder="Es. CEO, CTO...")
            with cols[2]:
                st.text_area("Esperienza",
                           key=f"team_member_{i}_esperienza",
                           value=member['esperienza'],
                           placeholder="Descrivi l'esperienza...")
        
        if i == len(st.session_state.team_members) - 1:
            if st.button("➕ Aggiungi Membro del Team"):
                st.session_state.team_members.append({
                    'nome': '',
                    'ruolo': '',
                    'esperienza': ''
                })
                st.rerun()
    
    st.file_uploader("Carica CV Team", accept_multiple_files=True,
                   key="cv_team",
                   help="Puoi caricare i CV di tutti i membri del team")

with tab_piano_finanziario:
    st.header("Piano Finanziario")
    st.markdown("""
    **Istruzioni:**
    Fornisci una stima delle tue proiezioni finanziarie per i prossimi anni.
    Se non disponi di dati precisi, indica valori approssimativi.
    """)
    
    # Durata business plan
    anni_bp = st.number_input("Durata Business Plan (anni)",
                            min_value=1, max_value=5, value=3,
                            help="Indica per quanti anni vuoi pianificare")
    
    # Proiezioni annuali con calcoli automatici
    st.subheader("Proiezioni Annuali")
    proiezioni = {}
    totali = {'ricavi': 0, 'costi': 0, 'profitti': 0}
    
    for anno in range(1, anni_bp + 1):
        with st.expander(f"Anno {anno}"):
            ricavi = st.number_input(f"Ricavi Previsti Anno {anno} (€) *",
                                   key=f"ricavi_anno{anno}",
                                   min_value=0, step=1000)
            costi = st.number_input(f"Costi Totali Anno {anno} (€) *",
                                  key=f"costi_anno{anno}",
                                  min_value=0, step=1000)
            
            if ricavi and costi:
                profitto = ricavi - costi
                st.metric(f"Profitto Anno {anno}", f"€ {profitto:,.2f}")
                
                if profitto < 0:
                    st.error("Attenzione: Proiezione di perdita per questo anno")
                elif profitto == 0:
                    st.warning("Proiezione di pareggio per questo anno")
                
                # Aggiorna totali
                totali['ricavi'] += ricavi
                totali['costi'] += costi
                totali['profitti'] += profitto
                
                proiezioni[anno] = {
                    'ricavi': ricavi,
                    'costi': costi,
                    'profitto': profitto
                }
    
    # Riepilogo finanziario
    st.subheader("Riepilogo Finanziario")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ricavi Totali", f"€ {totali['ricavi']:,.2f}")
    with col2:
        st.metric("Costi Totali", f"€ {totali['costi']:,.2f}")
    with col3:
        st.metric("Profitto Totale", f"€ {totali['profitti']:,.2f}",
                 delta_color="inverse" if totali['profitti'] < 0 else "normal")
    
    # Caricamento documenti aggiuntivi
    st.subheader("Documenti Aggiuntivi")
    st.markdown("""
    Puoi caricare qui eventuali documenti utili come:
    - Analisi di mercato
    - Dati sui concorrenti
    - Report finanziari
    - Altri documenti rilevanti
    """)
    doc_finanziari = st.file_uploader("Carica documenti finanziari",
                                    accept_multiple_files=True,
                                    key="doc_finanziari")
    
    # Link utili
    st.subheader("Risorse Online")
    st.text_input("Sito Web Aziendale", key="sito_web",
                 placeholder="Inserisci l'URL del tuo sito web")
    st.text_input("Siti Web Concorenti", key="siti_concorrenti",
                 placeholder="Inserisci URL separati da virgola")
    st.text_input("Fonti di Ricerca di Mercato", key="fonti_mercato",
                 placeholder="Inserisci URL di ricerche di mercato")

# Sidebar con bottone di invio
with st.sidebar:
    st.header("Invio Dati")
    # Funzione per validare i dati prima dell'invio
    def validate_data():
        required_fields = [
            'nome_azienda', 'motivazione_bp', 'descrizione_attivita', 'nome_prodotto',
            'mercato_target', 'strategia_marketing', 'piano_operativo',
            'canali_distribuzione', 'nome_fondatore', 'ruolo_fondatore',
            'esperienza_team'
        ]
        
        missing_fields = [f for f in required_fields if not st.session_state.get(f, "").strip()]
        return missing_fields

    # Funzione per generare JSON scaricabile
    def generate_json():
        data = {
            'info_generali': {
                'nome_azienda': st.session_state.get('nome_azienda'),
                'motivazione_bp': st.session_state.get('motivazione_bp'),
                'forma_giuridica': st.session_state.get('forma_giuridica'),
                'partita_iva': st.session_state.get('partita_iva'),
                'capitale_sociale': st.session_state.get('capitale_sociale'),
                'email_aziendale': st.session_state.get('email_aziendale'),
                'stato_azienda': st.session_state.get('stato_azienda'),
                'descrizione_attivita': st.session_state.get('descrizione_attivita'),
                'contesto_aziendale': st.session_state.get('contesto_aziendale'),
                'storia_aziendale': st.session_state.get('storia_aziendale'),
                'obiettivi_aziendali': st.session_state.get('obiettivi_aziendali')
            },
            'prodotto_servizio': {
                'nome_prodotto': st.session_state.get('nome_prodotto'),
                'descrizione': st.session_state.get('descrizione_prodotto')
            },
            'finanziario': {
                'proiezioni': proiezioni,
                'documenti': [f.name for f in doc_finanziari] if doc_finanziari else []
            }
        }
        return data

    if st.button("Invia Informazioni", type="primary", use_container_width=True):
        missing_fields = validate_data()
        
        if missing_fields:
            st.error(f"Campi obbligatori mancanti: {', '.join(missing_fields)}")
        else:
            st.subheader("Riepilogo Dati")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Informazioni Generali**")
                st.write(f"- Nome Azienda: {st.session_state.get('nome_azienda')}")
                st.write(f"- Forma Giuridica: {st.session_state.get('forma_giuridica')}")
                st.write(f"- Email: {st.session_state.get('email_aziendale')}")
                
            with col2:
                st.markdown("**Prodotto/Servizio**")
                st.write(f"- Nome: {st.session_state.get('nome_prodotto')}")
                st.write(f"- Mercato Target: {st.session_state.get('mercato_target')}")
            
            # Genera e scarica JSON
            json_data = generate_json()
            st.download_button(
                label="Scarica Dati in JSON",
                data=json.dumps(json_data, indent=2),
                file_name=f"business_plan_{st.session_state.get('nome_azienda')}.json",
                mime="application/json"
            )
            
            st.success("Informazioni validate e pronte per l'invio!")
    
    # Aggiunta di elementi grafici alla sidebar
    st.markdown("---")
    st.markdown("### Progresso Compilazione")
    progress_value = calculate_progress()
    st.progress(progress_value)
    
    # Mostra indicatori per ogni tab
    st.markdown("**Completamento Sezioni:**")
    tabs = {
        "Informazioni Generali": ['nome_azienda', 'motivazione_bp'],
        "Prodotto/Servizio": ['nome_prodotto'],
        "Analisi di Mercato": ['mercato_target'],
        "Strategia": ['strategia_marketing', 'piano_operativo', 'canali_distribuzione'],
        "Team": ['nome_fondatore', 'ruolo_fondatore', 'esperiencia_team']
    }
    
    for tab_name, fields in tabs.items():
        completed = sum(1 for f in fields if st.session_state.get(f, "").strip())
        total = len(fields)
        st.markdown(f"- {tab_name}: {'✅' if completed == total else '🟡'} ({completed}/{total})")
    
    st.caption(f"Completamento totale: {int(progress_value*100)}%")