import streamlit as st
import pandas as pd, glob, os
from lib.data_store import DB, list_metiers, list_categories, get_or_create_category, list_submissions, approve_submission
from config import ADMIN_ROUTE

def render():
    st.title("Admin — core team")
    st.caption(f"Access via '/?view={ADMIN_ROUTE}' (no link)")

    tab1, tab2, tab5, tab6 = st.tabs(["Pending", "Published", "Categories", "Logs"])

    with tab1:
        subs = [s for s in DB["submissions"] if s["status"]=="pending"]
        if not subs:
            st.info("No pending submissions.")
        for s in subs:
            with st.expander(f"{s['title']} — {s['author_display_name_snapshot']} — {s['category_name']}"):
                v = st.segmented_control("View", ["CRAFT","Full"], default="CRAFT", key=f"sv_{s['id']}")
                if v=="CRAFT":
                    st.markdown(f"**[CONTEXT]** {s['craft_context']}")
                    st.markdown(f"**[ROLE]** {s['craft_role']}")
                    st.markdown(f"**[ACTION]** {s['craft_action']}")
                    st.markdown(f"**[FORMAT]** {s['craft_format']}")
                    st.markdown(f"**[TONE]** {s['craft_tone']}")
                else:
                    st.code(s.get("full_text",""))
                c1,c2 = st.columns(2)
                with c1:
                    if st.button("Approve → Publish", key=f"ap_{s['id']}"):
                        approve_submission(s["id"])
                        st.toast("Published ✓")
                with c2:
                    if st.button("Reject", key=f"rj_{s['id']}"):
                        s["status"]="rejected"
                        st.toast("Rejected")

    with tab2:
        items = [p for p in DB["prompts"] if p["status"]=="published"]
        if not items:
            st.info("No published prompts yet.")
        else:
            df = pd.DataFrame([{
                "id":p["id"], "title":p["title"], "category":p.get("category_name",""),
                "author":p.get("author_display_name_snapshot",""), "rating":p.get("avg_rating",0),
                "uses":p.get("uses_total",0), "version":p.get("version","1.0")
            } for p in items])
            st.dataframe(df, use_container_width=True)

    with tab5:
        mets = list_metiers()
        metier = st.selectbox("Function", options=[(m["name"], m["id"]) for m in mets], format_func=lambda x:x[0] if isinstance(x,tuple) else x, index=0, key="adm_met")
        metier_id = metier[1]
        cats = list_categories(metier_id, active_only=False)
        df = pd.DataFrame(cats)
        st.dataframe(df, use_container_width=True)
        st.markdown("### Add category")
        name = st.text_input("Category name")
        if st.button("Create category"):
            if name.strip():
                get_or_create_category(metier_id, name.strip())
                st.toast("Category created")

    with tab6:
        st.markdown("### Logs")
        files = sorted(glob.glob("logs/*.csv"))
        if not files:
            st.info("No logs yet.")
        else:
            choice = st.selectbox("Select file", options=files[::-1])
            df = pd.read_csv(choice)
            st.dataframe(df, use_container_width=True)
            st.download_button("Export filtered CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="logs_export.csv", mime="text/csv")
