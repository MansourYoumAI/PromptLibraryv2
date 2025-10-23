import streamlit as st
from lib.data_store import get_prompt, rate_prompt, toggle_bookmark

def render():
    pid = st.query_params.get("id",[None])[0]
    if not pid:
        st.error("Paramètre id manquant.")
        return
    p = get_prompt(pid)
    if not p:
        st.error("Prompt introuvable.")
        return

    st.title(p["title"])
    st.caption(f"{p.get('category_name','')} • by {p.get('author_display_name_snapshot','')} • Uses {p.get('uses_total',0)} • ★ {p.get('avg_rating',0):.1f}")

    view = st.segmented_control("View", ["CRAFT","Full"], selection_mode="single", default="CRAFT")

    if view=="CRAFT":
        st.markdown(f"**[CONTEXT]** {p.get('craft_context','')}")
        st.markdown(f"**[ROLE]** {p.get('craft_role','')}")
        st.markdown(f"**[ACTION]** {p.get('craft_action','')}")
        st.markdown(f"**[FORMAT]** {p.get('craft_format','')}")
        st.markdown(f"**[TONE]** {p.get('craft_tone','')}")
        text_to_copy = assemble_craft(p)
    else:
        st.code(p.get("full_text",""), language=None)
        text_to_copy = p.get("full_text","")

    col1,col2,col3 = st.columns(3)
    with col1:
        if st.button("Copy prompt"):
            st.clipboard(text_to_copy)
            st.toast("Copié ✓")
    with col2:
        from config import COPILOT_URL
        st.link_button("Open Copilot", COPILOT_URL)
    with col3:
        if st.button("Save (bookmark)"):
            from lib.data_store import toggle_bookmark
            added = toggle_bookmark(st.session_state.get('user_key','guest'), p["id"])
            st.toast("Ajouté aux favoris ✓" if added else "Retiré des favoris")

    st.markdown("---")
    stars = st.slider("Rate this prompt", 1, 5, 5, step=1)
    if st.button("Submit rating"):
        rate_prompt(st.session_state.get('user_key','guest'), p["id"], stars)
        st.toast("Merci pour votre note.")

def assemble_craft(p):
    parts = []
    for key,label in [("craft_context","CONTEXT"),("craft_role","ROLE"),("craft_action","ACTION"),("craft_format","FORMAT"),("craft_tone","TONE")]:
        val = p.get(key,"").strip()
        if val:
            parts.append(f"[{label}] {val}")
    return "\n\n".join(parts)
