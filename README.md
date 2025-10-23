# AI Prompt Studio — Streamlit MVP

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Routes (via query param `view`):
- `/?view=home` (default)
- `/?view=category&cat=<category-id>`
- `/?view=prompt&id=<prompt-id>`
- `/?view=new`
- `/?view=my_saved`
- `/?view=my_submitted`
- `/?view=admincoreteam50`  (no link, no password)

Branding: Work Sans, primary #188d6d, rounded 8px, minimalist.
UX: hover subtle, fade-in, sticky search, micro-toasts, CRAFT fields differentiated, progress bar, back-to-top.

Data: in-memory (no seeds). Submit a prompt, approve it in Admin, then it appears in Category.
Logs: CSV files in /logs, export in Admin > Logs.
