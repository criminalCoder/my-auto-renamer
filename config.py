import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "24638450")

API_HASH = os.environ.get("API_HASH", "b720cf2f8cd64bc0ecee7ea3652a1cd1")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7058431670:AAEJ7MoIcYRQcmHUPRtSjb60ByGWMWCkkRw") 

FORCE_SUB = os.environ.get("FORCE_SUB", "botupdatesimplifytuber") 

DB_NAME = os.environ.get("DB_NAME","Yashkalvar07")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://Yashkalvar07:Yashkalvar07@yashkalvar07.cylum.mongodb.net/?retryWrites=true&w=majority")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/rv8Lds3/ALL-RENAMER-LOGO-YASH-GOYAL.jpg")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5965340120 6632019361 5497792868').split()]

# Bot_Username = "@LazyPrincessXBOT"
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@All_renamer_bot")
MAX_ACTIVE_TASKS = int(os.environ.get("MAX_ACTIVE_TASKS", "5"))
MAX_FORWARD = int(os.environ.get("MAX_FORWARD", "20"))
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "Yash-Goyal")
PORT = os.environ.get('PORT', '8080')

Lazy_session = {}
Lazy_api_id ={}
Lazy_api_hash ={}

String_Session  = "None"

Permanent_4gb = "-100XXX"
