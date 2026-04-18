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
# CSS — styling only, NO card content in HTML
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
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.5rem; }

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
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

/* ── CARD IMAGE — override Streamlit img ── */
.card-wrap [data-testid="stImage"] img {
    border-radius: 0 !important;
    width: 100% !important;
}
.card-wrap [data-testid="stImage"] {
    margin-bottom: 0 !important;
}

/* ── CARD INNER CONTENT ── */
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

/* ── HIDE STREAMLIT IMAGE CAPTION ── */
[data-testid="caption"] { display: none !important; }

/* ── CHART AREA ── */
[data-testid="stVegaLiteChart"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    padding: 12px !important;
}
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
                "title":  data.get("Title", "N/A"),
                "genre":  data.get("Genre", "N/A"),
                "rating": float(data["imdbRating"]) if data.get("imdbRating", "N/A") != "N/A" else 0.0,
                "poster": data["Poster"] if data.get("Poster", "N/A") != "N/A" else None,
                "year":   data.get("Year", "N/A"),
                "actors": data.get("Actors", "N/A"),
                "plot":   data.get("Plot", "N/A"),
            }
    except Exception:
        pass
    return None


# ================================================================
# SESSION
# ================================================================
if "movies" not in st.session_state:
    st.session_state.movies = []


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
        "color:#7A7A8C;margin-bottom:0.6rem;font-weight:500'>Search</div>",
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
            with st.spinner("Fetching…"):
                movie = fetch_movie(movie_input.strip())
            if movie:
                existing = [m["title"].lower() for m in st.session_state.movies]
                if movie["title"].lower() not in existing:
                    st.session_state.movies.append(movie)
                    st.success(f"✓ Added: {movie['title']}")
                else:
                    st.warning("Already in collection.")
            else:
                st.error("Movie not found. Try another title.")
        else:
            st.warning("Enter a movie name first.")

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
    "margin-bottom:2.5rem;margin-top:0.5rem'></div>",
    unsafe_allow_html=True
)

df = pd.DataFrame(st.session_state.movies)


# ================================================================
# EMPTY STATE
# ================================================================
if df.empty:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎞️</div>
        <div class="empty-title">Your Collection Awaits</div>
        <div class="empty-text">Search for any movie in the sidebar to get started</div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# COLLECTION
# ================================================================
else:
    avg_rating  = df["rating"].mean()
    top_movie   = df.loc[df["rating"].idxmax()]
    genre_count = df["genre"].str.split(", ").explode().nunique()

    # ── STAT TILES ──
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-tile">
            <div class="stat-label">Films Catalogued</div>
            <div class="stat-value">{len(df)}</div>
            <div class="stat-desc">In your collection</div>
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

    # ── MOVIE CARDS — rendered with native Streamlit (no HTML injection per card) ──
    cols = st.columns(4, gap="medium")

    for i, row in df.iterrows():
        col = cols[i % 4]
        is_top = row["title"] == top_movie["title"]

        with col:
            # Card wrapper opens
            st.markdown('<div class="card-wrap">', unsafe_allow_html=True)

            # Poster — native st.image (always works, no HTML needed)
            if row["poster"]:
                st.image(row["poster"], use_container_width=True)
            else:
                st.markdown(
                    "<div style='width:100%;aspect-ratio:2/3;background:#1A1A26;"
                    "display:flex;align-items:center;justify-content:center;"
                    "font-size:48px'>🎬</div>",
                    unsafe_allow_html=True
                )

            # Card body — all static HTML, no dynamic text injected
            st.markdown('<div class="card-inner">', unsafe_allow_html=True)

            if is_top:
                st.markdown('<div class="card-badge">⭐ Top Rated</div>', unsafe_allow_html=True)

            # Year — use st.caption styled via write
            st.markdown(
                f"<div class='card-year'>{row['year']}</div>",
                unsafe_allow_html=True
            )

            # Title — native st.markdown plain text (** bold **)
            st.markdown(
                f"<div class='card-title'>{row['title']}</div>",
                unsafe_allow_html=True
            )

            # Genre
            st.markdown(
                f"<div class='card-genre'>{row['genre']}</div>",
                unsafe_allow_html=True
            )

            # Rating badge
            st.markdown(
                f"<div class='card-rating'>★ {row['rating']:.1f}</div>",
                unsafe_allow_html=True
            )

            # Actors
            st.markdown(
                f"<div class='card-actors'>{row['actors']}</div>",
                unsafe_allow_html=True
            )

            # Plot
            st.markdown(
                f"<div class='card-plot'>{row['plot']}</div>",
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)  # close card-inner
            st.markdown('</div>', unsafe_allow_html=True)  # close card-wrap

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
