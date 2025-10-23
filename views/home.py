import streamlit as st
from config import APP_NAME
from lib.data_store import DB

def render():
    st.title(APP_NAME)
    st.caption("Home")
    st.markdown('<div class="sticky">', unsafe_allow_html=True)
    q = st.text_input("Rechercher un prompt (mot-clé, auteur…)", key="home_search")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Categories")
    sales_cats = [c for c in DB["categories"] if c["metier_id"]=="sales" and c.get("is_active",True)]
    cols = st.columns(3)
    for i,c in enumerate(sales_cats[:3]):
        with cols[i%3]:
            st.markdown(f"""<div class="card fade-in" style="border:1px solid #eaeaea;padding:18px;border-radius:8px;">
  <a href='/?view=category&cat={c['id']}' style='text-decoration:none;color:inherit;'>
  <b>{c['name']}</b>
  </a>
</div>
""", unsafe_allow_html=True)

    if q:
        st.subheader(f"Résultats pour “{q}”")
        hits = []
        for p in DB["prompts"]:
            hay = (p.get("title","")+" "+p.get("description","")+" "+p.get("full_text","")).lower()
            if all(t in hay for t in q.lower().split()):
                hits.append(p)
        if not hits:
            st.info("Aucun résultat.")
        else:
            for p in hits:
                col1,col2 = st.columns([4,1])
                with col1:
                    st.markdown(f"**{p['title']}**  
_{p.get('description','')[:120]}_")
                    st.caption(f"by {p.get('author_display_name_snapshot','')} • ★ {p.get('avg_rating',0):.1f} • {p.get('uses_total',0)} uses")
                with col2:
                    st.link_button("Open", f"/?view=prompt&id={p['id']}")
