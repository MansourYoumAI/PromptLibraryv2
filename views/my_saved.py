import streamlit as st
from lib.data_store import list_bookmarks

def render():
    st.title("My saved prompts")
    items = list_bookmarks(st.session_state.get('user_key','guest'))
    if not items:
        st.info("No bookmarks yet.")
        return
    for p in items:
        st.markdown(f"**{p['title']}** — {p.get('category_name','')}")
        st.link_button("Open", f"/?view=prompt&id={p['id']}")
