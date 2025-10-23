import streamlit as st
from config import APP_NAME, PRIMARY_COLOR, SIDEBAR_BG, ROUNDED_RADIUS_PX, COPILOT_URL, ADMIN_ROUTE
from lib.utils import write_log, purge_old_logs
from lib.data_store import list_metiers, list_categories

st.set_page_config(page_title=APP_NAME, layout="wide")

st.markdown("""

<link rel="preconnect" href="https://fonts.googleapis.com">

<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]  { font-family: 'Work Sans', sans-serif; }

section[data-testid="stSidebar"] { background: %(SIDEBAR_BG)s; }

.card { transition: transform .12s ease, box-shadow .12s ease; border-radius: %(RADIUS)spx; }

.card:hover { transform: scale(1.01); box-shadow: 0 4px 18px rgba(0,0,0,0.08); }

.fade-in { animation: fadein .18s ease both; }

@keyframes fadein { from {opacity:0; transform: translateY(4px);} to {opacity:1; transform:none;} }

.sticky { position: sticky; top: 0; z-index: 10; background: white; padding-top: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(0,0,0,0.05); }

.craftfield textarea { background:#f7f7f7 !important; border-radius:%(RADIUS)spx; }

#backToTop { position: fixed; bottom: 20px; right: 20px; display: none; }

</style>

<script>

window.addEventListener('scroll', function(){

  const btn = window.parent.document.getElementById('backToTop');

  if(!btn) return;

  if (window.scrollY > 300) { btn.style.display='block'; } else { btn.style.display='none'; }

});

</script>

""" % {"SIDEBAR_BG": SIDEBAR_BG, "RADIUS": ROUNDED_RADIUS_PX}, unsafe_allow_html=True)

st.markdown('<a id="backToTop" class="card" href="#top" style="padding:10px 12px;background:%s;color:white;text-decoration:none;">Back to top</a>' % PRIMARY_COLOR, unsafe_allow_html=True)

metiers = list_metiers()
active_metier = metiers[0]
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.markdown("### Function")
st.sidebar.write(f"• {active_metier['name']}")
cats = list_categories(active_metier["id"])
st.sidebar.markdown("### Categories")
for c in cats:
    st.sidebar.markdown(f"- [{c['name']}](/?view=category&cat={c['id']})")
st.sidebar.markdown("---")
st.sidebar.markdown("[My saved](/?view=my_saved)")
st.sidebar.markdown("[My submitted](/?view=my_submitted)")

view = st.query_params.get("view", ["home"])[0]

if view == "home":
    import views.home as V
    V.render()
elif view == "category":
    import views.category as V
    V.render()
elif view == "prompt":
    import views.prompt_detail as V
    V.render()
elif view == "new":
    import views.new_prompt as V
    V.render()
elif view == "my_saved":
    import views.my_saved as V
    V.render()
elif view == "my_submitted":
    import views.my_submitted as V
    V.render()
elif view == ADMIN_ROUTE:
    import views.admin as V
    V.render()
else:
    st.error("Page not found.")
