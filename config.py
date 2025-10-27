APP_NAME = "AI Prompt Studio"
PRIMARY_COLOR = "#188d6d"
SIDEBAR_BG = "#ffffff"
ROUNDED_RADIUS_PX = 8
ADMIN_ROUTE = "admincoreteam50"

METIERS = [{"id":"sales","name":"Sales","icon":"sales.svg","is_active":True}]

CATEGORIES = [
    {"id":"prospection","metier_id":"sales","name":"Prospection","is_active":True},
    {"id":"account-planning","metier_id":"sales","name":"Account Planning","is_active":True},
    {"id":"negociation","metier_id":"sales","name":"Négociation","is_active":True}
]

AUTHORS = [{"id":"auth_mansouryoum","display_name":"MansourYoum","normalized_key":"mansouryoum","is_active":True}]

COPILOT_URL = "https://m365.cloud.microsoft/copilot"

LOG_DIR = "logs"
LOG_RETENTION_DAYS = 90
LOG_MAX_BYTES = 10 * 1024 * 1024
