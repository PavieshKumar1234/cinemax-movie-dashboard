import streamlit as st
import pandas as pd
import requests

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="CINEMAX — Movie Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CSS
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Playfair+Display:wght@700&display=swap');

:root {
    --bg:        #0A0A0F;
    --surface:   #111118;
    --surface2:  #1A1A26;
    --border:    rgba(255,255,255,0.07);
    --gold:      #C9A84C;
    --gold-dim:  rgba(201,168,76,0.15);
    --gold-glow: rgba(201,168,76,0.35);
    --text:      #F0EDE8;
    --muted:     #7A7A8C;
    --radius:    16px;
    --radius-sm: 8px;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1400px !important; }

/* ── CINEMATIC BACKGROUND ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
        url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&q=60') center/cover no-repeat fixed;
    opacity: 0.06;
    pointer-events: none;
    z-index: 0;
}

/* ── FILM GRAIN ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.6;
}

/* ── FILM STRIP BACKGROUND DECORATION ── */
.film-strip-bg {
    position: fixed;
    top: 0; right: -20px;
    width: 60px;
    height: 100vh;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 30px,
        rgba(201,168,76,0.04) 30px,
        rgba(201,168,76,0.04) 35px,
        transparent 35px,
        transparent 65px
    );
    border-left: 1px solid rgba(201,168,76,0.05);
    pointer-events: none;
    z-index: 1;
}

/* ── MASTHEAD ── */
.masthead-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 64px;
    letter-spacing: 4px;
    color: var(--text);
    line-height: 1;
    display: inline;
}
.masthead-logo span { color: var(--gold); }
.masthead-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--gold), transparent);
    margin-bottom: 2.5rem;
    margin-top: 0.6rem;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D14 0%, #111118 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.5rem; }

/* ── INPUT ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: var(--gold) !important;
    color: #0A0A0F !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 20px !important;
    width: 100% !important;
    margin-top: 0.4rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #dbb95a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px var(--gold-glow) !important;
}

/* ── MANUAL FORM BOX ── */
.manual-box {
    background: linear-gradient(135deg, rgba(201,168,76,0.08), rgba(201,168,76,0.02));
    border: 1px solid rgba(201,168,76,0.35);
    border-radius: var(--radius);
    padding: 22px 20px;
    margin-top: 1rem;
}
.manual-box-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 16px;
    letter-spacing: 3px;
    color: var(--gold);
    margin-bottom: 12px;
}

/* ── STAT TILES ── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 2.5rem;
}
.stat-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}
.stat-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
}
.stat-label {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
    font-weight: 500;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 40px;
    letter-spacing: 2px;
    color: var(--gold);
    line-height: 1;
}
.stat-desc {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
    font-weight: 300;
}

/* ── SECTION HEADINGS ── */
.section-heading {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    letter-spacing: 3px;
    color: var(--text);
    margin-bottom: 0.2rem;
    margin-top: 2.5rem;
}
.section-sub {
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── CARD WRAPPER ── */
.card-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    margin-bottom: 1.2rem;
    padding-bottom: 14px;
}
.card-wrap:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    border-color: rgba(201,168,76,0.3);
}
.card-wrap [data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
}
.card-wrap [data-testid="stImage"] { margin-bottom: 0 !important; }
.card-inner { padding: 0 14px; }
.card-badge {
    display: inline-block;
    background: linear-gradient(135deg, #C9A84C, #9A7A30);
    color: #0A0A0F;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 4px;
    margin: 10px 0 6px 0;
}
.manual-badge {
    display: inline-block;
    background: linear-gradient(135deg, #4a7fc1, #2a4f81);
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 4px;
    margin: 10px 0 6px 0;
}
.card-year {
    font-size: 11px;
    letter-spacing: 2px;
    color: var(--gold);
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 3px;
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 5px;
    line-height: 1.25;
}
.card-genre {
    font-size: 11px;
    color: var(--muted);
    margin-bottom: 10px;
    font-weight: 300;
}
.card-rating {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--gold-dim);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 13px;
    font-weight: 600;
    color: var(--gold);
    margin-bottom: 8px;
}
.card-actors {
    font-size: 11px;
    color: var(--muted);
    line-height: 1.5;
    font-style: italic;
    margin-bottom: 8px;
}
.card-plot {
    font-size: 11px;
    color: #9090a0;
    line-height: 1.6;
    padding-top: 8px;
    border-top: 1px solid var(--border);
}

/* ── HERO BANNER WITH MOVIE COLLAGE ── */
.hero-collage {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 6px;
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 2rem;
    height: 180px;
    position: relative;
}
.hero-collage img {
    width: 100%; height: 100%;
    object-fit: cover;
    filter: brightness(0.5) saturate(0.7);
    transition: filter 0.3s;
}
.hero-collage-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(10,10,15,0.9) 0%, rgba(10,10,15,0.3) 50%, rgba(10,10,15,0.6) 100%);
    display: flex;
    align-items: center;
    padding: 0 32px;
}
.hero-quote {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-style: italic;
    color: rgba(240,237,232,0.85);
    max-width: 400px;
    line-height: 1.5;
}
.hero-quote span { color: var(--gold); }

/* ── ANALYTICS ── */
.chart-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius) var(--radius) 0 0;
    padding: 18px 22px 10px;
    border-bottom: none;
}
.chart-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    color: var(--text);
}
.chart-sub {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
[data-testid="stVegaLiteChart"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    padding: 12px !important;
}

/* ── TOP BANNER ── */
.top-banner {
    background: linear-gradient(135deg, rgba(201,168,76,0.12), rgba(201,168,76,0.04));
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: var(--radius);
    padding: 20px 28px;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    gap: 16px;
}
.top-banner-icon { font-size: 36px; }
.top-banner-label {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C9A84C;
    font-weight: 600;
    margin-bottom: 4px;
}
.top-banner-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: #F0EDE8;
    font-weight: 700;
}
.top-banner-meta {
    font-size: 12px;
    color: #7A7A8C;
    margin-top: 2px;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 80px 40px;
    background: var(--surface);
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: var(--radius);
    margin-top: 2rem;
}
.empty-icon { font-size: 56px; margin-bottom: 16px; }
.empty-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    letter-spacing: 3px;
    color: var(--muted);
    margin-bottom: 8px;
}
.empty-text { font-size: 13px; color: var(--muted); font-weight: 300; }

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}

[data-testid="caption"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# FETCH FROM OMDB
# ================================================================
def fetch_movie(name: str):
    api_key = "8d349c39"
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={name}"
    try:
        data = requests.get(url, timeout=8).json()
        if data.get("Response") == "True":
            return {
                "title":    data.get("Title", "N/A"),
                "genre":    data.get("Genre", "N/A"),
                "rating":   float(data["imdbRating"]) if data.get("imdbRating", "N/A") != "N/A" else 0.0,
                "poster":   data["Poster"] if data.get("Poster", "N/A") != "N/A" else None,
                "year":     data.get("Year", "N/A"),
                "actors":   data.get("Actors", "N/A"),
                "plot":     data.get("Plot", "N/A"),
                "manual":   False,
            }
    except Exception:
        pass
    return None


# ================================================================
# SESSION
# ================================================================
if "movies" not in st.session_state:
    st.session_state.movies = []
if "show_manual_form" not in st.session_state:
    st.session_state.show_manual_form = False
if "pending_manual_title" not in st.session_state:
    st.session_state.pending_manual_title = ""


# ================================================================
# SIDEBAR
# ================================================================
with st.sidebar:
    st.markdown(
        "<div style='font-family:Bebas Neue,sans-serif;font-size:22px;"
        "letter-spacing:3px;color:#C9A84C;margin-bottom:1.5rem'>🎬 CINEMAX</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='font-size:10px;letter-spacing:3px;text-transform:uppercase;"
        "color:#7A7A8C;margin-bottom:0.6rem;font-weight:500'>Search Movie</div>",
        unsafe_allow_html=True
    )

    movie_input = st.text_input(
        label="search",
        placeholder="e.g. Inception, RRR, Leo…",
        label_visibility="collapsed"
    )
    add_clicked = st.button("＋  Add to Collection")

    if add_clicked:
        if movie_input.strip():
            with st.spinner("Fetching from OMDB…"):
                movie = fetch_movie(movie_input.strip())
            if movie:
                existing = [m["title"].lower() for m in st.session_state.movies]
                if movie["title"].lower() not in existing:
                    st.session_state.movies.append(movie)
                    st.success(f"✓ Added: {movie['title']}")
                    st.session_state.show_manual_form = False
                else:
                    st.warning("Already in collection.")
            else:
                # Trigger manual form
                st.session_state.show_manual_form = True
                st.session_state.pending_manual_title = movie_input.strip()
                st.warning("Not found in database. Enter details manually ↓")
        else:
            st.warning("Enter a movie name first.")

    # ── MANUAL ENTRY FORM ──
    if st.session_state.show_manual_form:
        st.markdown(
            "<div class='manual-box'>"
            "<div class='manual-box-title'>✏️ Manual Entry</div>"
            "</div>",
            unsafe_allow_html=True
        )
        with st.form("manual_movie_form", clear_on_submit=True):
            m_title  = st.text_input("Title *", value=st.session_state.pending_manual_title)
            m_year   = st.text_input("Year", placeholder="e.g. 2023")
            m_genre  = st.text_input("Genre", placeholder="e.g. Drama, Action")
            m_rating = st.number_input("Your Rating (0–10)", min_value=0.0, max_value=10.0, step=0.1, value=7.0)
            m_actors = st.text_input("Actors", placeholder="e.g. Actor A, Actor B")
            m_plot   = st.text_area("Plot / Description", placeholder="Brief plot summary…", height=90)
            m_poster = st.text_input("Poster URL (optional)", placeholder="https://…")
            submitted = st.form_submit_button("➕ Add Manually")

            if submitted:
                if m_title.strip():
                    existing = [m["title"].lower() for m in st.session_state.movies]
                    if m_title.strip().lower() not in existing:
                        st.session_state.movies.append({
                            "title":  m_title.strip(),
                            "year":   m_year.strip() or "N/A",
                            "genre":  m_genre.strip() or "N/A",
                            "rating": float(m_rating),
                            "actors": m_actors.strip() or "N/A",
                            "plot":   m_plot.strip() or "N/A",
                            "poster": m_poster.strip() if (m_poster and m_poster.strip().startswith("http")) else None,
                            "manual": True,
                        })
                        st.success(f"✓ Manually added: {m_title.strip()}")
                        st.session_state.show_manual_form = False
                        st.session_state.pending_manual_title = ""
                        st.rerun()
                    else:
                        st.warning("Already in collection.")
                else:
                    st.error("Title is required.")

    if st.session_state.movies:
        st.markdown(
            "<div style='font-size:10px;letter-spacing:3px;text-transform:uppercase;"
            "color:#7A7A8C;margin:1.5rem 0 0.6rem;font-weight:500'>My Collection</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:36px;"
            f"color:#C9A84C;letter-spacing:2px;line-height:1'>"
            f"{len(st.session_state.movies)}</div>"
            f"<div style='font-size:11px;color:#7A7A8C;letter-spacing:2px;"
            f"text-transform:uppercase;margin-top:4px'>Titles</div>",
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("🗑  Clear All"):
            st.session_state.movies = []
            st.session_state.show_manual_form = False
            st.rerun()


# ================================================================
# MASTHEAD
# ================================================================
st.markdown(
    "<div style='display:flex;align-items:baseline;gap:16px;margin-bottom:2px'>"
    "<span style='font-family:Bebas Neue,sans-serif;font-size:64px;letter-spacing:4px;"
    "color:#F0EDE8;line-height:1'>CINE<span style='color:#C9A84C'>MAX</span></span>"
    "<span style='font-size:11px;font-weight:300;letter-spacing:5px;text-transform:uppercase;"
    "color:#7A7A8C;padding-bottom:10px'>Movie Intelligence Dashboard</span>"
    "</div>"
    "<div style='height:1px;background:linear-gradient(90deg,#C9A84C,transparent);"
    "margin-bottom:1.5rem;margin-top:0.5rem'></div>",
    unsafe_allow_html=True
)

# ── CINEMATIC HERO BANNER ──
st.markdown("""
<div style="position:relative;border-radius:16px;overflow:hidden;margin-bottom:2rem;height:180px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;height:100%;gap:4px;">
        <img src="https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=400&q=60"
             style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45) saturate(0.6);">
        <img src="https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&q=60"
             style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45) saturate(0.6);">
        <img src="https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400&q=60"
             style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45) saturate(0.6);">
        <img src="https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&q=60"
             style="width:100%;height:100%;object-fit:cover;filter:brightness(0.45) saturate(0.6);">
    </div>
    <div style="position:absolute;inset:0;
        background:linear-gradient(90deg,rgba(10,10,15,0.92) 0%,rgba(10,10,15,0.35) 60%,rgba(10,10,15,0.7) 100%);
        display:flex;align-items:center;padding:0 36px;">
        <div>
            <div style="font-size:10px;letter-spacing:4px;text-transform:uppercase;
                color:#C9A84C;font-weight:600;margin-bottom:10px;">Cinema Begins Here</div>
            <div style="font-family:'Playfair Display',serif;font-size:20px;
                font-style:italic;color:rgba(240,237,232,0.9);line-height:1.5;max-width:480px;">
                "Every frame is a painting.<br>Every story, a world entire."
            </div>
            <div style="font-size:11px;color:#7A7A8C;margin-top:10px;letter-spacing:2px;">
                — Track, rate and analyse your cinematic universe
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.movies)

# ================================================================
# EMPTY STATE
# ================================================================
if df.empty:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎞️</div>
        <div class="empty-title">Your Collection Awaits</div>
        <div class="empty-text">Search for any movie in the sidebar — or add one manually if it's not in the database</div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# COLLECTION
# ================================================================
else:
    avg_rating  = df["rating"].mean()
    top_movie   = df.loc[df["rating"].idxmax()]
    genre_count = df["genre"].str.split(", ").explode().nunique()
    manual_count = int(df["manual"].sum()) if "manual" in df.columns else 0

    # ── STAT TILES ──
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-tile">
            <div class="stat-label">Films Catalogued</div>
            <div class="stat-value">{len(df)}</div>
            <div class="stat-desc">In your collection ({int(manual_count)} manual)</div>
        </div>
        <div class="stat-tile">
            <div class="stat-label">Average IMDb Rating</div>
            <div class="stat-value">{avg_rating:.1f}</div>
            <div class="stat-desc">Across all titles</div>
        </div>
        <div class="stat-tile">
            <div class="stat-label">Genres Represented</div>
            <div class="stat-value">{genre_count}</div>
            <div class="stat-desc">Unique categories</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION HEADING ──
    st.markdown('<div class="section-heading">COLLECTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your curated film library</div>', unsafe_allow_html=True)

    # ── MOVIE CARDS ──
    cols = st.columns(4, gap="medium")

    for i, row in df.iterrows():
        col = cols[i % 4]
        is_top    = row["title"] == top_movie["title"]
        is_manual = bool(row["manual"]) if "manual" in df.columns else False

        with col:
            st.markdown('<div class="card-wrap">', unsafe_allow_html=True)

            # Poster — safely handle None, NaN, float, empty string
            poster_val = row.get("poster", None)
            has_poster = (
                poster_val is not None
                and isinstance(poster_val, str)
                and poster_val.strip().startswith("http")
            )
            if has_poster:
                st.image(poster_val.strip(), use_container_width=True)
            else:
                # Fallback: cinematic placeholder from Unsplash
                placeholder_urls = [
                    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&q=50",
                    "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?w=300&q=50",
                    "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&q=50",
                    "https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=300&q=50",
                ]
                ph = placeholder_urls[i % len(placeholder_urls)]
                st.markdown(
                    f"<div style='position:relative;overflow:hidden;'>"
                    f"<img src='{ph}' style='width:100%;aspect-ratio:2/3;object-fit:cover;"
                    f"filter:brightness(0.5) saturate(0.5);'>"
                    f"<div style='position:absolute;inset:0;display:flex;align-items:center;"
                    f"justify-content:center;font-size:40px;'>🎬</div></div>",
                    unsafe_allow_html=True
                )

            st.markdown('<div class="card-inner">', unsafe_allow_html=True)

            if is_top:
                st.markdown('<div class="card-badge">⭐ Top Rated</div>', unsafe_allow_html=True)
            if is_manual:
                st.markdown('<div class="manual-badge">✏️ Manual Entry</div>', unsafe_allow_html=True)

            st.markdown(f"<div class='card-year'>{row['year']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>{row['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-genre'>{row['genre']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-rating'>★ {row['rating']:.1f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-actors'>{row['actors']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-plot'>{row['plot']}</div>", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── ANALYTICS ──
    st.markdown('<div class="section-heading">ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Insights from your collection</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("""
        <div class="chart-header">
            <div class="chart-title">GENRES</div>
            <div class="chart-sub">Distribution across collection</div>
        </div>
        """, unsafe_allow_html=True)
        genre_series = df["genre"].str.split(", ").explode().value_counts()
        st.bar_chart(genre_series, color="#C9A84C")

    with c2:
        st.markdown("""
        <div class="chart-header">
            <div class="chart-title">RATINGS</div>
            <div class="chart-sub">IMDb score per title</div>
        </div>
        """, unsafe_allow_html=True)
        rating_df = df.set_index("title")["rating"]
        st.bar_chart(rating_df, color="#C9A84C")

    # ── TOP MOVIE BANNER ──
    st.markdown(f"""
    <div class="top-banner">
        <div class="top-banner-icon">🏆</div>
        <div>
            <div class="top-banner-label">Top Rated Film</div>
            <div class="top-banner-title">{top_movie['title']}</div>
            <div class="top-banner-meta">★ {top_movie['rating']:.1f} &nbsp;·&nbsp; {top_movie['genre']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================================================================
# FOOTER
# ================================================================
st.markdown(
    '<div class="footer">© 2025 Cinemax — Movie Intelligence Platform</div>',
    unsafe_allow_html=True
)
