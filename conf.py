import os

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_PATH = os.path.join(BASE_DIR, 'static')

if not os.path.exists(STATIC_PATH):
    os.mkdir(STATIC_PATH)

INTERMEDIATE_FILE = os.path.join(STATIC_PATH, 'intermediate_file.json')
# retrying on scraping error or if scraped data is loss
STYLEINFORM_RETRY_TIMES = 3

# ----------------- AUTH DATA
STYLEINFORM_USERNAME = os.environ['STYLEINFORM_USERNAME']
STYLEINFORM_PASSWORD = os.environ['STYLEINFORM_PASSWORD']

# ------------------ GOOGLE
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = os.path.join(STATIC_PATH, 'credentials.json')

STYLEINFORM_SHEET_NAME = os.environ['STYLEINFORM_SHEET_NAME']
STYLEINFORM_REPORT_SHEET = os.environ['STYLEINFORM_REPORT_SHEET']

# --------------------- Other
REDIS_CONNECTION = os.environ['REDIS_CONNECTION']

SCHEDULING_TZ = 'US/Pacific'
