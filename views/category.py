import streamlit as st
from lib.data_store import DB
def render():
    cat = st.query_params.get("cat", [None])[0]
    if not cat:
        st.error("Catégorie manquante.")
        return
    cat_name = next((c["name"] for c in DB["categories"] if c["id"]==cat), cat)
    st.title(cat_name)
    st.caption("Prompt list (tri par défaut: Highest rated)")
    st.markdown('<div class="sticky">', unsafe_allow_html=True)
    sort = st.selectbox("Sort by", options=["Highest rated","Most used","Recently added"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    prompts = [p for p in DB["prompts"] if p["category_id"]==cat and p["status"]=="published"]
    def sort_key(p):
        if sort=="Highest rated":
            return (-p.get("avg_rating",0), -p.get("uses_total",0))
        if sort=="Most used":
            return (-p.get("uses_total",0), -p.get("avg_rating",0))
        if sort=="Recently added":
            return p.get("id","")
    prompts = sorted(prompts, key=sort_key)

    if not prompts:
        st.info("No prompt available in this category yet.")
        st.link_button("Create one", "/?view=new")
        return

    for p in prompts:
        col1,col2 = st.columns([4,1])
        with col1:
            st.markdown(f"""<div class="card fade-in" style="border:1px solid #eaeaea;padding:16px;border-radius:8px;">
  <div><b>{p['title']}</b></div>
  <div><i>{p.get('description','')[:140]}</i></div>
</div>
""", unsafe_allow_html=True)
            st.caption(f"by {p.get('author_display_name_snapshot','')} • ★ {p.get('avg_rating',0):.1f} • {p.get('uses_total',0)} uses")
        with col2:
            st.link_button("Open", f"/?view=prompt&id={p['id']}")
            from lib.data_store import toggle_bookmark
            if st.button("Bookmark", key=f"bm_{p['id']}"):
                added = toggle_bookmark(st.session_state.get('user_key','guest'), p['id'])
                st.toast("Ajouté aux favoris ✓" if added else "Retiré des favoris")
