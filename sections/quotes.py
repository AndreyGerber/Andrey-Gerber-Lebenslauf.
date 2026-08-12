"""
sections/quotes.py

"Die 3 größten Fehlschätzungen meines Lebens" - drei Zitat-Karten.
Statisch, keine Interaktivität -> kein @st.fragment nötig.
"""

import streamlit as st

_CSS = """
<style>
    :root, [data-testid="stHorizontalBlock"] {
        --size-quote: 21px;
        --size-year: 18px;
    }
    [data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: stretch;
    }
    .quote-card {
        background: #ffffff;
        border-top: 5px solid #8e44ad;
        border-radius: 12px;
        padding: 25px;
        height: 100%;
        min-height: 180px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease;
    }
    .quote-card:hover { transform: translateY(-5px); }
    .quote-content {
        font-style: italic;
        color: #1e293b;
        font-size: var(--size-quote);
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .quote-year {
        text-align: right;
        font-weight: bold;
        color: #8e44ad;
        font-size: var(--size-year);
    }
    .quote-year::before { content: "— "; }
</style>
"""


def render_quotes(t: dict):
    st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: left;'>{t['quotes_title']}</h2>", unsafe_allow_html=True)
    st.markdown(_CSS, unsafe_allow_html=True)

    q_col1, q_col2, q_col3 = st.columns(3)

    with q_col1:
        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-content">"{t['quotes_1_text']}"</div>
            <div class="quote-year">{t['quotes_1_year']}</div>
        </div>
        """, unsafe_allow_html=True)

    with q_col2:
        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-content">"{t['quotes_2_text']}"</div>
            <div class="quote-year">{t['quotes_2_year']}</div>
        </div>
        """, unsafe_allow_html=True)

    with q_col3:
        st.markdown(f"""
        <div class="quote-card">
            <div class="quote-content">"{t['quotes_3_text']}"</div>
            <div class="quote-year">{t['quotes_3_year']}</div>
        </div>
        """, unsafe_allow_html=True)