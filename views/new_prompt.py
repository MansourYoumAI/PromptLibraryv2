import streamlit as st
from lib.data_store import list_metiers, list_categories, get_or_create_category, get_or_create_author, create_submission

def render():
    st.title("Create a new prompt (CRAFT only)")

    progress = 0
    title = st.text_input("Prompt name *")
    desc = st.text_area("Description (optional)", height=80)

    mets = list_metiers()
    metier = st.selectbox("Function *", options=[(m["name"], m["id"]) for m in mets], format_func=lambda x:x[0] if isinstance(x,tuple) else x, index=0)
    metier_id = metier[1]

    cats = list_categories(metier_id)
    cat_names = [c["name"] for c in cats] + ["+ New category…"]
    cat_choice = st.selectbox("Category *", options=cat_names)
    if cat_choice == "+ New category…":
        new_cat = st.text_input("New category name *")
        category = get_or_create_category(metier_id, new_cat.strip()) if new_cat.strip() else None
    else:
        category = next(c for c in cats if c["name"]==cat_choice)

    from lib.data_store import list_authors
    authors = list_authors()
    author_names = [a["display_name"] for a in authors] + ["+ New author…"]
    author_choice = st.selectbox("Author *", options=author_names, index=0)
    if author_choice == "+ New author…":
        author_display = st.text_input("New author name *", value="")
    else:
        author_display = author_choice

    st.markdown("### CRAFT")
    context = st.text_area("[CONTEXT] *", height=100, key="ctx")
    role = st.text_area("[ROLE] *", height=80, key="role")
    action = st.text_area("[ACTION] *", height=100, key="action")
    fmt = st.text_area("[FORMAT] *", height=80, key="format")
    tone = st.text_area("[TONE] *", height=60, key="tone")

    for f in [context, role, action, fmt, tone]:
        if f.strip(): progress += 1
    st.progress(progress/5.0, text=f"{progress}/5")

    if st.button("Preview Full Text"):
        full = assemble_full(context, role, action, fmt, tone)
        st.code(full)

    disabled = not (title.strip() and metier_id and category and author_display.strip() and all([context.strip(), role.strip(), action.strip(), fmt.strip(), tone.strip()]))
    if st.button("Save prompt (submit for review)", disabled=disabled):
        author = get_or_create_author(author_display)
        full = assemble_full(context, role, action, fmt, tone)
        sub = create_submission({
            "title": title.strip(),
            "description": desc.strip(),
            "metier_id": metier_id,
            "category": category,
            "author_display_name": author["display_name"],
            "craft_context": context.strip(),
            "craft_role": role.strip(),
            "craft_action": action.strip(),
            "craft_format": fmt.strip(),
            "craft_tone": tone.strip(),
            "full_text": full,
            "user_key": "guest"
        })
        st.success("Prompt submitted for review.")
        st.link_button("Go to My submitted", "/?view=my_submitted")

def assemble_full(context, role, action, fmt, tone):
    parts = []
    if context.strip(): parts.append(f"[CONTEXT] {context.strip()}")
    if role.strip(): parts.append(f"[ROLE] {role.strip()}")
    if action.strip(): parts.append(f"[ACTION] {action.strip()}")
    if fmt.strip(): parts.append(f"[FORMAT] {fmt.strip()}")
    if tone.strip(): parts.append(f"[TONE] {tone.strip()}")
    return "\n\n".join(parts)
