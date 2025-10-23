import streamlit as st
from lib.data_store import list_submissions

def render():
    st.title("My submitted prompts")
    subs = [s for s in list_submissions() if s.get('created_by','')=='guest']
    if not subs:
        st.info("You haven't submitted any prompts yet.")
        return
    for s in subs:
        st.markdown(f"**{s['title']}** — {s['status']} — {s.get('category_name','')}")
        with st.expander("Preview"):
            st.code(s.get('full_text',''))
