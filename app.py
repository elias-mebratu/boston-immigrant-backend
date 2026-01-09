from flask import Flask, jsonify, request, send_from_directory  # import Flask server, JSON helpers, query parsing, and static file serving
from flask_cors import CORS  # import CORS so browsers can call the API safely
import os  # import os for building safe file paths
import copy  # import copy so we can safely duplicate resource objects before translating them
@app.get("/")  # define a simple root endpoint
def root():  # function that runs when someone visits /
    return jsonify(ok=True, message="Boston Immigrant Resources API is running")  # return a clear JSON response
app = Flask(__name__)  # create the Flask application instance
CORS(app, resources={r"/api/*": {"origins": ["https://bostonimmigrantresources.org"]}})  # allow only your production Netlify domain to call /api endpoints
  # enable CORS (safe even when serving frontend from same server)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get absolute path to the folder that contains this file


# -----------------------------
# LANGUAGE SUPPORT (4 LANGUAGES)
# -----------------------------
SUPPORTED_LANGS = {"en", "es", "ar", "am"}  # define the supported language codes (English, Spanish, Arabic, Amharic)

LANG_LABELS = {  # define human-friendly labels for each supported language
    "en": "English",  # English label
    "es": "Español",  # Spanish label
    "ar": "العربية",  # Arabic label
    "am": "አማርኛ",  # Amharic label
}  # end language labels


# UI translations (use these for buttons, headings, placeholders, etc.)  # explain that this dict is for frontend UI text
UI_I18N = {  # create a dictionary for UI translation strings
    "en": {  # English UI strings
        "title": "Boston Immigrant Resources",  # site title
        "subtitle": "Search for legal aid, housing, jobs, healthcare, and more.",  # site subtitle
        "search_placeholder": "Try: housing, legal, halal...",  # search input placeholder
        "search_button": "Search",  # search button label
        "browse_by_category": "Browse by Category",  # category section heading
        "all": "All",  # "All" category label
        "address": "Address",  # label for address
        "phone": "Phone",  # label for phone
        "website": "Website",  # label for website
        "no_results": "No results found.",  # message when there are no results
    },  # end English UI strings
    "es": {  # Spanish UI strings
        "title": "Recursos para Inmigrantes en Boston",  # translated title
        "subtitle": "Busca ayuda legal, vivienda, empleo, salud y más.",  # translated subtitle
        "search_placeholder": "Ejemplo: vivienda, legal, halal...",  # translated placeholder
        "search_button": "Buscar",  # translated button
        "browse_by_category": "Explorar por categoría",  # translated heading
        "all": "Todos",  # translated "All"
        "address": "Dirección",  # translated address label
        "phone": "Teléfono",  # translated phone label
        "website": "Sitio web",  # translated website label
        "no_results": "No se encontraron resultados.",  # translated no results
    },  # end Spanish UI strings
    "ar": {  # Arabic UI strings
        "title": "موارد المهاجرين في بوسطن",  # translated title
        "subtitle": "ابحث عن المساعدة القانونية والسكن والعمل والرعاية الصحية والمزيد.",  # translated subtitle
        "search_placeholder": "جرّب: السكن، القانون، حلال...",  # translated placeholder
        "search_button": "بحث",  # translated button
        "browse_by_category": "تصفّح حسب الفئة",  # translated heading
        "all": "الكل",  # translated "All"
        "address": "العنوان",  # translated address label
        "phone": "الهاتف",  # translated phone label
        "website": "الموقع",  # translated website label
        "no_results": "لا توجد نتائج.",  # translated no results
    },  # end Arabic UI strings
    "am": {  # Amharic UI strings
        "title": "የቦስተን ለስደተኞች መረጃ ምንጮች",  # translated title
        "subtitle": "የህግ እገዛ፣ መኖሪያ፣ ስራ፣ ጤና እና ሌሎችን ይፈልጉ።",  # translated subtitle
        "search_placeholder": "ሞክር: መኖሪያ, ህጋዊ, ሀላል...",  # translated placeholder
        "search_button": "ፈልግ",  # translated button
        "browse_by_category": "በምድብ ያስሱ",  # translated heading
        "all": "ሁሉም",  # translated "All"
        "address": "አድራሻ",  # translated address label
        "phone": "ስልክ",  # translated phone label
        "website": "ድህረገፅ",  # translated website label
        "no_results": "ምንም ውጤት አልተገኘም።",  # translated no results
    },  # end Amharic UI strings
}  # end UI_I18N dictionary


# Category translations (these translate ONLY display labels; your data stays stored in English)  # explain purpose of category translation map
CATEGORY_I18N = {  # create a dictionary to translate category names
    "Housing Help": {  # category: Housing Help
        "en": "Housing Help",  # English
        "es": "Ayuda de Vivienda",  # Spanish
        "ar": "مساعدة السكن",  # Arabic
        "am": "የመኖሪያ እገዛ",  # Amharic
    },  # end Housing Help mapping
    "Food Security": {  # category: Food Security
        "en": "Food Security",  # English
        "es": "Seguridad Alimentaria",  # Spanish
        "ar": "الأمن الغذائي",  # Arabic
        "am": "የምግብ ደህንነት",  # Amharic
    },  # end Food Security mapping
    "Cash & Income Assistance": {  # category: Cash & Income Assistance
        "en": "Cash & Income Assistance",  # English
        "es": "Asistencia Económica",  # Spanish
        "ar": "مساعدة مالية ودخل",  # Arabic
        "am": "የገንዘብ እና ገቢ እገዛ",  # Amharic
    },  # end Cash & Income Assistance mapping
    "Healthcare": {  # category: Healthcare
        "en": "Healthcare",  # English
        "es": "Atención Médica",  # Spanish
        "ar": "الرعاية الصحية",  # Arabic
        "am": "ጤና እንክብካቤ",  # Amharic
    },  # end Healthcare mapping
    "Employment & Training": {  # category: Employment & Training
        "en": "Employment & Training",  # English
        "es": "Empleo y Capacitación",  # Spanish
        "ar": "العمل والتدريب",  # Arabic
        "am": "ስራ እና ስልጠና",  # Amharic
    },  # end Employment & Training mapping
    "ESL & Education": {  # category: ESL & Education
        "en": "ESL & Education",  # English
        "es": "Inglés y Educación",  # Spanish
        "ar": "تعلم الإنجليزية والتعليم",  # Arabic
        "am": "እንግሊዝኛ (ESL) እና ትምህርት",  # Amharic
    },  # end ESL & Education mapping
    "Youth & Education": {  # category: Youth & Education
        "en": "Youth & Education",  # English
        "es": "Jóvenes y Educación",  # Spanish
        "ar": "الشباب والتعليم",  # Arabic
        "am": "ወጣቶች እና ትምህርት",  # Amharic
    },  # end Youth & Education mapping
    "Transportation": {  # category: Transportation
        "en": "Transportation",  # English
        "es": "Transporte",  # Spanish
        "ar": "المواصلات",  # Arabic
        "am": "መጓጓዣ",  # Amharic
    },  # end Transportation mapping
    "Legal Aid": {  # category: Legal Aid
        "en": "Legal Aid",  # English
        "es": "Asistencia Legal",  # Spanish
        "ar": "مساعدة قانونية",  # Arabic
        "am": "የህግ እገዛ",  # Amharic
    },  # end Legal Aid mapping
    "Religious Institutions": {  # category: Religious Institutions
        "en": "Religious Institutions",  # English
        "es": "Instituciones Religiosas",  # Spanish
        "ar": "مؤسسات دينية",  # Arabic
        "am": "የሃይማኖት ተቋማት",  # Amharic
    },  # end Religious Institutions mapping
    "Food & Dining": {  # category: Food & Dining
        "en": "Food & Dining",  # English
        "es": "Comida y Restaurantes",  # Spanish
        "ar": "الطعام والمطاعم",  # Arabic
        "am": "ምግብ እና መመገቢያ",  # Amharic
    },  # end Food & Dining mapping
}  # end CATEGORY_I18N mapping


def get_lang():  # define a helper to read the requested language from the URL
    lang = request.args.get("lang", "en").strip().lower()  # read ?lang= and default to English if missing
    return lang if lang in SUPPORTED_LANGS else "en"  # return the language if supported, otherwise fall back to English


def t_category(category_en, lang):  # define a helper to translate a category name
    mapping = CATEGORY_I18N.get(category_en, None)  # get the translation mapping for this category, if available
    if not mapping:  # if there is no mapping for this category
        return category_en  # return the original English category as a safe fallback
    return mapping.get(lang, category_en)  # return the requested language translation or fall back to English


def localize_resource(resource, lang):  # define a helper to create a translated copy of a resource
    r = copy.deepcopy(resource)  # deep copy so we never mutate the original in-memory data
    r["category_en"] = resource.get("category", "")  # preserve the original English category in the response
    r["category"] = t_category(resource.get("category", ""), lang)  # replace category display label with the translated version
    r["lang"] = lang  # include which language was applied to this record
    return r  # return the localized resource copy


# -----------------------------
# DATA: your in-memory database
# -----------------------------
resources_data = [  # list of all resources (each item becomes a card on the website and a record in the API)

    # =========================
    # HOUSING HELP
    # =========================
    {  # resource: emergency shelter access points
        "id": 1001,  # unique ID
        "name": "Boston Emergency Shelter (City Intake / Access Points)",  # display name
        "category": "Housing Help",  # top-level category (tabs)
        "subcategory": "Emergency & No-Income Housing",  # second-level grouping
        "services": ["Emergency shelter navigation", "Same-day access guidance"],  # services offered
        "eligibility": "No housing / crisis situation; ID helpful but not always required; immigration status typically not asked",  # eligibility notes
        "requirements": ["ID helpful (not always required)", "No income required"],  # typical requirements
        "location": "Boston, MA (city intake / access points vary)",  # address / location text
        "phone": "",  # phone number (blank if unknown)
        "website": "",  # website URL (blank if unknown)
        "details": "Start here if someone has no housing, no income, and needs immediate shelter guidance.",  # short description
        "tags": ["shelter", "emergency", "no income", "intake"],  # search keywords
    },
    {  # resource: Pine Street Inn
        "id": 1002,
        "name": "Pine Street Inn",
        "category": "Housing Help",
        "subcategory": "Emergency & No-Income Housing",
        "services": ["Emergency shelter", "Outreach"],
        "eligibility": "Adults needing emergency shelter; ID helpful; no income required; immigration status typically not asked",
        "requirements": ["ID helpful (not always required)"],
        "location": "444 Harrison Avenue, Boston, MA 02118",
        "phone": "617-892-9100",
        "website": "https://www.pinestreetinn.org",
        "details": "Emergency shelter for adults and street outreach services.",
        "tags": ["shelter", "emergency", "adults", "outreach"],
    },
    {  # resource: Rosie's Place
        "id": 1003,
        "name": "Rosie’s Place",
        "category": "Housing Help",
        "subcategory": "Emergency & No-Income Housing",
        "services": ["Women-only shelter options", "Meals", "Basic needs support", "Referrals"],
        "eligibility": "Women in crisis; ID helpful; no income required; immigration status typically not asked",
        "requirements": ["ID helpful (not always required)"],
        "location": "889 Harrison Avenue, Boston, MA 02118",
        "phone": "617-442-9322",
        "website": "https://www.rosiesplace.org",
        "details": "Support and pathways for women needing shelter, meals, and basic services.",
        "tags": ["women", "shelter", "meals", "clothing"],
    },
    {  # resource: Bridge Over Troubled Waters
        "id": 1004,
        "name": "Bridge Over Troubled Waters",
        "category": "Housing Help",
        "subcategory": "Youth (18–24) & Crisis Support",
        "services": ["Crisis support", "Case management", "Stabilization services", "Referrals"],
        "eligibility": "Homeless/runaway/at-risk youth; documentation often not required for initial help (program dependent)",
        "requirements": ["Program intake (varies)"],
        "location": "47 West Street, Boston, MA 02111",
        "phone": "617-423-9575",
        "website": "https://bridgeotw.org/get-help/",
        "details": "Support for homeless/runaway/at-risk youth including counseling, education pathways, and stabilization services.",
        "tags": ["youth", "18-24", "crisis", "stabilization"],
    },
    {  # resource: transitional housing (concept)
        "id": 1101,
        "name": "Transitional Housing Programs (3–24 months)",
        "category": "Housing Help",
        "subcategory": "Transitional Housing",
        "services": ["Short-term housing", "Case management", "Help with documents/jobs/benefits"],
        "eligibility": "Homeless or at risk; must follow program rules; no minimum income needed at entry (often)",
        "requirements": ["Program participation rules"],
        "location": "Boston, MA (provider dependent)",
        "phone": "",
        "website": "",
        "details": "Stabilization stage after emergency shelter; includes case management support.",
        "tags": ["transitional", "case management", "stabilization"],
    },
    {  # resource: BHA public housing (concept)
        "id": 1201,
        "name": "Boston Housing Authority (BHA) – Public Housing",
        "category": "Housing Help",
        "subcategory": "Public & Subsidized Housing",
        "services": ["Public housing applications", "Housing support programs (varies)"],
        "eligibility": "Very low income; seniors; people with disabilities; families; long waitlists are common",
        "requirements": ["Application required", "Income verification (varies)"],
        "location": "Boston, MA",
        "phone": "",
        "website": "",
        "details": "Public housing options with rent typically capped around ~30% of income (program rules apply).",
        "tags": ["public housing", "BHA", "low income", "waitlist"],
    },
    {  # resource: Section 8 (concept)
        "id": 1202,
        "name": "Section 8 / Housing Choice Vouchers (Rental Assistance)",
        "category": "Housing Help",
        "subcategory": "Public & Subsidized Housing",
        "services": ["Rental assistance vouchers", "Rent subsidy support"],
        "eligibility": "Very low income; limited supply; waitlists; acceptance depends on availability",
        "requirements": ["Application/waitlist"],
        "location": "Boston-area",
        "phone": "",
        "website": "",
        "details": "Vouchers cover part or most of rent depending on program and income.",
        "tags": ["section 8", "voucher", "rent assistance", "subsidy"],
    },
    {  # resource: Metrolist (concept)
        "id": 1301,
        "name": "Metrolist (Income-Restricted Apartments)",
        "category": "Housing Help",
        "subcategory": "Affordable Rentals",
        "services": ["Income-restricted housing listings", "Lottery listings (varies)"],
        "eligibility": "Income-restricted units (often 30%/50%/80% AMI tiers; listing-specific)",
        "requirements": ["Application required", "Income verification"],
        "location": "Boston-area",
        "phone": "",
        "website": "",
        "details": "Primary access point for Boston-area income-restricted apartment listings.",
        "tags": ["affordable", "income restricted", "AMI", "lottery", "metrolist"],
    },
    {  # resource: tenant rights (concept)
        "id": 1401,
        "name": "Tenant Rights & Legal Protections (Boston)",
        "category": "Housing Help",
        "subcategory": "Tenant Rights",
        "services": ["Eviction help", "Unsafe housing help", "Discrimination support", "Mediation referrals"],
        "eligibility": "All renters; free help often available for low-income renters",
        "requirements": [],
        "location": "Boston, MA",
        "phone": "",
        "website": "",
        "details": "If facing eviction, unsafe housing, or discrimination, seek legal aid and city navigation resources.",
        "tags": ["tenant", "eviction", "unsafe housing", "discrimination"],
    },

    # =========================
    # FOOD SECURITY
    # =========================
    {  # resource: GBFB
        "id": 3001,
        "name": "The Greater Boston Food Bank",
        "category": "Food Security",
        "subcategory": "Food Pantries & SNAP Support",
        "services": ["Food pantry network support", "Emergency food access pathways", "SNAP outreach (varies)"],
        "eligibility": "Food assistance; pantry rules vary; many access points do not require ID",
        "requirements": [],
        "location": "70 South Bay Avenue, Boston, MA 02118",
        "phone": "617-427-5200",
        "website": "https://www.gbfb.org/contact-us/",
        "details": "Food bank network supporting pantries and meal programs; also offers SNAP outreach assistance.",
        "tags": ["food", "pantry", "meals", "no ID", "SNAP"],
    },
    {  # resource: St. Francis House
        "id": 3002,
        "name": "St. Francis House",
        "category": "Food Security",
        "subcategory": "Meals, Clothing, and Basic Needs",
        "services": ["Daily meals", "Clothing", "Day shelter services", "Support programs (varies)"],
        "eligibility": "Low-barrier access; many services available to people without housing",
        "requirements": [],
        "location": "39 Boylston Street, Boston, MA 02116",
        "phone": "617-542-4211",
        "website": "https://stfrancishouse.org/contact-us/",
        "details": "Day shelter and services including meals, clothing, and support programs.",
        "tags": ["meals", "clothing", "hygiene", "homeless"],
    },
    {  # resource: Project Bread
        "id": 3003,
        "name": "Project Bread",
        "category": "Food Security",
        "subcategory": "SNAP & Food Assistance Navigation",
        "services": ["Food assistance navigation", "SNAP/EBT support and guidance"],
        "eligibility": "SNAP is income-based; application required; meal programs vary",
        "requirements": ["Income-based verification for SNAP (varies)"],
        "location": "145 Border Street, East Boston, MA 02128",
        "phone": "617-723-5000",
        "website": "https://projectbread.org/contact-us",
        "details": "Food assistance organization helping residents access meal resources and benefits like SNAP.",
        "tags": ["SNAP", "EBT", "food", "benefits"],
    },

    # =========================
    # CASH & INCOME ASSISTANCE
    # =========================
    {  # resource: MA DTA
        "id": 4001,
        "name": "Massachusetts Department of Transitional Assistance (DTA)",
        "category": "Cash & Income Assistance",
        "subcategory": "Cash Benefits, SNAP, Emergency Help",
        "services": ["Emergency cash assistance", "Family benefits", "SNAP/EBT (program dependent)"],
        "eligibility": "Income-tested; can include $0 income eligibility depending on program",
        "requirements": ["Often requires verification/documents (program dependent)"],
        "location": "Massachusetts (statewide support)",
        "phone": "877-382-2363",
        "website": "https://www.mass.gov/orgs/department-of-transitional-assistance",
        "details": "State benefits agency for SNAP/EBT, cash assistance, and related programs.",
        "tags": ["cash assistance", "benefits", "low income", "DTA", "SNAP"],
    },

    # =========================
    # HEALTHCARE
    # =========================
    {  # resource: ER concept
        "id": 2001,
        "name": "Emergency Rooms (ER) – Any Hospital (EMTALA)",
        "category": "Healthcare",
        "subcategory": "Emergency Care",
        "services": ["Emergency medical care", "Emergency mental health crisis care"],
        "eligibility": "Anyone with an emergency; hospitals cannot refuse emergency stabilizing care; no payment upfront (emergency context)",
        "requirements": [],
        "location": "Any hospital emergency department",
        "phone": "911",
        "website": "",
        "details": "If it is an emergency (physical or mental health), go to an ER or call 911.",
        "tags": ["ER", "emergency", "911", "no insurance"],
    },
    {  # resource: MGH (basic)
        "id": 2002,
        "name": "Massachusetts General Hospital (MGH)",
        "category": "Healthcare",
        "subcategory": "Emergency Care",
        "services": ["Emergency care", "Specialty care"],
        "eligibility": "Emergency care available regardless of ability to pay in emergencies; other services depend on coverage/assistance",
        "requirements": [],
        "location": "Boston, MA",
        "phone": "",
        "website": "",
        "details": "Major Boston hospital with ER and specialty services.",
        "tags": ["hospital", "ER", "emergency"],
    },
    {  # resource: BWH (basic)
        "id": 2003,
        "name": "Brigham and Women’s Hospital",
        "category": "Healthcare",
        "subcategory": "Emergency Care",
        "services": ["Emergency care", "Specialty care"],
        "eligibility": "Emergency care available regardless of ability to pay in emergencies; other services depend on coverage/assistance",
        "requirements": [],
        "location": "Boston, MA",
        "phone": "",
        "website": "",
        "details": "Major Boston hospital with ER and specialty services.",
        "tags": ["hospital", "ER", "emergency"],
    },
    {  # resource: BMC
        "id": 2004,
        "name": "Boston Medical Center (BMC)",
        "category": "Healthcare",
        "subcategory": "Safety-Net / Uninsured Care",
        "services": ["Primary care", "Mental health", "Addiction treatment", "Prenatal care"],
        "eligibility": "Strong safety-net services for uninsured, low-income, and homeless patients (program rules vary)",
        "requirements": [],
        "location": "1 Boston Medical Center Place, Boston, MA",
        "phone": "617-638-8000",
        "website": "https://www.bmc.org",
        "details": "Safety-net hospital with wide services and support programs.",
        "tags": ["uninsured", "low income", "mental health", "prenatal"],
    },
    {  # resource: MassHealth (concept)
        "id": 2006,
        "name": "MassHealth (Massachusetts Medicaid)",
        "category": "Healthcare",
        "subcategory": "Public Health Insurance",
        "services": ["Health insurance coverage", "Doctors", "Hospitals", "Mental health", "Medications"],
        "eligibility": "Low income; families; children; pregnant people; seniors; people with disabilities (rules vary)",
        "requirements": ["Application required", "Income verification (varies)"],
        "location": "Massachusetts (Boston included)",
        "phone": "",
        "website": "",
        "details": "Public health insurance. Many people qualify for $0 monthly cost depending on income and category.",
        "tags": ["Medicaid", "insurance", "MassHealth", "low income"],
    },
    {  # resource: 988
        "id": 2007,
        "name": "988 Mental Health Crisis Line (24/7)",
        "category": "Healthcare",
        "subcategory": "Mental Health",
        "services": ["Crisis counseling", "Immediate support", "Referrals"],
        "eligibility": "Anyone in mental health crisis or needing immediate support",
        "requirements": [],
        "location": "Anywhere (phone)",
        "phone": "988",
        "website": "",
        "details": "Free 24/7 crisis support line for mental health emergencies and urgent support.",
        "tags": ["988", "crisis", "mental health", "24/7"],
    },
    {  # resource: MA Health Connector (you had it in your JSON list)
        "id": 2010,
        "name": "Massachusetts Health Connector (Customer Service)",
        "category": "Healthcare",
        "subcategory": "Insurance Marketplace & Subsidized Plans",
        "services": ["Plan enrollment help", "Eligibility guidance", "Subsidized plan support (varies)"],
        "eligibility": "People without employer insurance; subsidy eligibility depends on income and household",
        "requirements": ["Enrollment/application (varies)"],
        "location": "Massachusetts (phone support)",
        "phone": "877-623-6765",
        "website": "https://www.mahealthconnector.org/about/contact",
        "details": "State health insurance marketplace; customer service helps with enrollment, plans, and eligibility.",
        "tags": ["insurance", "marketplace", "health connector", "plans"],
    },

    # =========================
    # EMPLOYMENT & TRAINING
    # =========================
    {  # resource: MassHire Downtown Boston (you had this in your JSON list)
        "id": 5001,
        "name": "MassHire Downtown Boston Career Center",
        "category": "Employment & Training",
        "subcategory": "Job Search, Training, Resume Help",
        "services": ["Job search help", "Training referrals", "Resume/interview support", "Career coaching"],
        "eligibility": "Unemployed/underemployed; counseling/training often available regardless of documentation (job placement can depend on work authorization)",
        "requirements": ["Program enrollment (varies)"],
        "location": "75 Federal Street, 3rd Floor, Boston, MA 02110",
        "phone": "617-399-3100",
        "website": "https://masshiredowntownboston.org/contact/",
        "details": "Workforce services including job search help, training referrals, resume/interview support, and career coaching.",
        "tags": ["jobs", "training", "resume", "MassHire", "career center"],
    },

    # =========================
    # ESL & EDUCATION
    # =========================
    {  # resource: IINE (ESL + support)
        "id": 6003,
        "name": "International Institute of New England (IINE)",
        "category": "ESL & Education",
        "subcategory": "Immigrant/Refugee Support",
        "services": ["ESL classes", "Job readiness for immigrants", "Refugee workforce programs", "Immigration referrals (varies)"],
        "eligibility": "Immigrants, refugees, asylees (program rules vary)",
        "requirements": ["Program enrollment (varies)"],
        "location": "Boston-area",
        "phone": "",
        "website": "https://iine.org",
        "details": "Support services for immigrants/refugees including ESL and workforce programs.",
        "tags": ["immigrants", "refugees", "ESL", "workforce"],
    },

    # =========================
    # YOUTH & EDUCATION (employment programs)
    # =========================
    {  # resource: Youth summer jobs (concept)
        "id": 7001,
        "name": "Boston Summer Youth Employment Program",
        "category": "Youth & Education",
        "subcategory": "Youth Employment",
        "services": ["Paid summer jobs", "Workplace training", "Career exploration"],
        "eligibility": "Youth ages ~14–24 (program rules vary)",
        "requirements": ["Application required"],
        "location": "Boston, MA",
        "phone": "",
        "website": "",
        "details": "City youth program offering paid summer jobs and work readiness experiences.",
        "tags": ["youth", "summer jobs", "paid"],
    },

    # =========================
    # TRANSPORTATION
    # =========================
    {  # resource: MBTA (concept)
        "id": 8001,
        "name": "MBTA (Public Transportation)",
        "category": "Transportation",
        "subcategory": "Public Transit",
        "services": ["Subway", "Buses", "Commuter rail", "Reduced fare passes"],
        "eligibility": "Reduced fares available for low-income, seniors, disabled riders (program rules vary)",
        "requirements": ["Reduced fare application (for discounts)"],
        "location": "Greater Boston",
        "phone": "",
        "website": "",
        "details": "Public transit system; reduced fares can be critical for accessing services and work.",
        "tags": ["MBTA", "subway", "bus", "reduced fare"],
    },

    # =========================
    # LEGAL AID
    # =========================
    {  # resource: GBLS (you had address/phone/website)
        "id": 9001,
        "name": "Greater Boston Legal Services (GBLS)",
        "category": "Legal Aid",
        "subcategory": "Housing, Benefits, Employment, Immigration Referrals",
        "services": ["Housing law", "Benefits help", "Worker rights", "Legal aid (issue dependent)"],
        "eligibility": "Eligible low-income residents; tenants (including undocumented) may qualify depending on issue",
        "requirements": ["Intake screening (income/issue-based)"],
        "location": "197 Friend Street, Boston, MA 02114",
        "phone": "617-371-1234",
        "website": "https://www.gbls.org/contact_us",
        "details": "Free civil legal aid for eligible low-income residents; help with housing, benefits, and worker rights.",
        "tags": ["eviction", "tenant rights", "benefits", "wage theft", "legal aid"],
    },
    {  # resource: VLP (you had address/phone/website)
        "id": 9002,
        "name": "Volunteer Lawyers Project (VLP)",
        "category": "Legal Aid",
        "subcategory": "Eviction Clinics & Civil Legal Help",
        "services": ["Eviction-related clinics", "Advice and referrals", "Civil legal support (varies)"],
        "eligibility": "Low-income; urgent eviction help; clinic availability varies",
        "requirements": ["Clinic intake (varies)"],
        "location": "7 Winthrop Square, 2nd Floor, Boston, MA 02110",
        "phone": "617-603-1700",
        "website": "https://vlpnet.org/about-us/contact-us/",
        "details": "Civil legal support including eviction-related clinics and advice; hotline available.",
        "tags": ["eviction", "clinic", "mediation", "housing court"],
    },
    {  # resource: PAIR (you had address/phone/website)
        "id": 9101,
        "name": "PAIR Project (Political Asylum / Immigration Representation Project)",
        "category": "Legal Aid",
        "subcategory": "Immigration & Asylum",
        "services": ["Asylum applications", "Deportation defense (varies)", "Pro bono coordination"],
        "eligibility": "Low-income asylum seekers and immigrants; eligibility rules apply",
        "requirements": ["Intake screening"],
        "location": "98 North Washington Street, Suite 106, Boston, MA 02114",
        "phone": "617-742-9296",
        "website": "https://www.pairproject.org/",
        "details": "Immigration and asylum legal support and pro bono coordination; focused on protecting asylum seekers and immigrants.",
        "tags": ["asylum", "immigration", "deportation defense", "refugees"],
    },
    {  # resource: Office of Housing Stability (you had it as a key provider)
        "id": 9102,
        "name": "City of Boston — Office of Housing Stability",
        "category": "Housing Help",
        "subcategory": "Tenant Support, Eviction Prevention & Navigation",
        "services": ["Eviction prevention", "Navigation and referrals", "Emergency rental help guidance (varies)"],
        "eligibility": "Tenants facing eviction or housing instability (referrals vary)",
        "requirements": ["Intake (varies)"],
        "location": "26 Court Street, Boston, MA 02108",
        "phone": "617-635-4200",
        "website": "https://www.boston.gov/departments/housing/office-housing-stability",
        "details": "Helps tenants facing eviction or housing instability with navigation, prevention, and referral support.",
        "tags": ["tenant", "eviction prevention", "rental assistance", "city"],
    },

    # =========================
    # RELIGIOUS INSTITUTIONS (Boston / Greater Boston)
    # =========================
    {  # church
        "id": 10001,
        "name": "Christian Science Plaza",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public (rules vary by event)",
        "requirements": [],
        "location": "210 Massachusetts Ave, Boston, MA 02115",
        "phone": "",
        "website": "",
        "details": "Christian Science campus and church facilities in Boston.",
        "tags": ["church", "christian", "christian science"],
    },
    {  # church
        "id": 10002,
        "name": "Basilica of Our Lady of Perpetual Help",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Mass/services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "1545 Tremont St, Boston, MA 02120",
        "phone": "",
        "website": "",
        "details": "Catholic basilica in Boston (Mission Hill area).",
        "tags": ["church", "catholic", "basilica"],
    },
    {  # church
        "id": 10003,
        "name": "Trinity Church in the City of Boston",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "206 Clarendon St, Boston, MA 02116",
        "phone": "617-536-0944",
        "website": "",
        "details": "Historic church in Copley Square.",
        "tags": ["church", "christian", "trinity", "copley"],
    },
    {  # church
        "id": 10004,
        "name": "Old South Church in Boston",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "645 Boylston St, Boston, MA 02116",
        "phone": "",
        "website": "",
        "details": "Historic church in Back Bay.",
        "tags": ["church", "christian", "old south"],
    },
    {  # church
        "id": 10005,
        "name": "St Cecilia Parish",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Mass/services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "18 Belvidere St, Boston, MA 02115",
        "phone": "",
        "website": "",
        "details": "Catholic parish near Back Bay / Fenway area.",
        "tags": ["church", "catholic", "parish"],
    },
    {  # church
        "id": 10006,
        "name": "Park Street Church",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "1 Park St, Boston, MA 02108",
        "phone": "",
        "website": "",
        "details": "Historic church near Boston Common.",
        "tags": ["church", "christian", "park street"],
    },
    {  # church
        "id": 10007,
        "name": "Renewal Church - Boston",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "175 Tremont St, Boston, MA 02111",
        "phone": "",
        "website": "",
        "details": "Boston church community (services vary).",
        "tags": ["church", "christian"],
    },
    {  # church
        "id": 10008,
        "name": "Boston Church Back Bay",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "180 Berkeley St, Boston, MA 02116",
        "phone": "",
        "website": "",
        "details": "Church community in Back Bay (services vary).",
        "tags": ["church", "christian", "back bay"],
    },
    {  # church
        "id": 10009,
        "name": "Church of the Advent",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "30 Brimmer St, Boston, MA 02108",
        "phone": "",
        "website": "",
        "details": "Episcopal church in Beacon Hill area (services vary).",
        "tags": ["church", "episcopal", "beacon hill"],
    },
    {  # church
        "id": 10010,
        "name": "First Church in Boston",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "66 Marlborough St, Boston, MA 02116",
        "phone": "",
        "website": "",
        "details": "Historic church in Back Bay area.",
        "tags": ["church", "christian", "first church"],
    },
    {  # church
        "id": 10011,
        "name": "Anchor Church Boston",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "351 Boylston St, Boston, MA 02116",
        "phone": "",
        "website": "",
        "details": "Church community (services vary).",
        "tags": ["church", "christian"],
    },
    {  # church
        "id": 10012,
        "name": "King’s Chapel",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)", "Historic site (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "58 Tremont St, Boston, MA 02108",
        "phone": "",
        "website": "",
        "details": "Historic chapel in downtown Boston.",
        "tags": ["church", "chapel", "historic"],
    },
    {  # church
        "id": 10013,
        "name": "The Cathedral Church of Saint Paul",
        "category": "Religious Institutions",
        "subcategory": "Churches (Christian)",
        "services": ["Worship services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "138 Tremont St, Boston, MA 02111",
        "phone": "",
        "website": "",
        "details": "Cathedral church in downtown Boston area.",
        "tags": ["church", "cathedral", "christian"],
    },

    # Ethiopian Orthodox (requested)
    {  # Ethiopian Orthodox church (Boston area)
        "id": 10020,
        "name": "Debre Menkrat St. Gabriel Ethiopian Orthodox Tewahedo Church",
        "category": "Religious Institutions",
        "subcategory": "Ethiopian Orthodox (Tewahedo)",
        "services": ["Worship services (varies)", "Community and cultural support (varies)"],
        "eligibility": "Open to the public (service rules vary)",
        "requirements": [],
        "location": "162 Goddard Ave, Brookline, MA 02445",
        "phone": "857-488-2835",
        "website": "https://stgebrieleotcboston.org/",
        "details": "Ethiopian Orthodox Tewahedo church serving the Boston area.",
        "tags": ["ethiopian orthodox", "tewahedo", "amharic", "church"],
    },

    # Mosques / Islamic Centers
    {  # ISBCC
        "id": 10101,
        "name": "Islamic Society of Boston Cultural Center (ISBCC)",
        "category": "Religious Institutions",
        "subcategory": "Mosques / Islamic Centers",
        "services": ["Prayer services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public (rules vary by event)",
        "requirements": [],
        "location": "100 Malcolm X Blvd, Roxbury, MA 02120",
        "phone": "617-858-6114",
        "website": "https://isbcc.org/",
        "details": "Major Islamic center serving Greater Boston.",
        "tags": ["mosque", "islam", "islamic center", "roxbury"],
    },
    {  # Al-Quran Mosque
        "id": 10102,
        "name": "Al-Quran Mosque",
        "category": "Religious Institutions",
        "subcategory": "Mosques / Islamic Centers",
        "services": ["Prayer services (varies)"],
        "eligibility": "Open to the public (rules vary)",
        "requirements": [],
        "location": "35 Intervale St #37, Boston, MA 02121",
        "phone": "",
        "website": "",
        "details": "Local mosque in Boston (programs vary).",
        "tags": ["mosque", "islam", "dorchester"],
    },
    {  # ICNE Quincy (near Boston)
        "id": 10103,
        "name": "Islamic Center of New England (ICNE) – Quincy",
        "category": "Religious Institutions",
        "subcategory": "Mosques / Islamic Centers",
        "services": ["Prayer services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "470 South St, Quincy, MA 02169",
        "phone": "",
        "website": "",
        "details": "Islamic center in Quincy (Greater Boston area).",
        "tags": ["mosque", "islam", "quincy", "icne"],
    },
    {  # ICNE Sharon (near Boston)
        "id": 10104,
        "name": "Islamic Center of New England (ICNE) – Sharon",
        "category": "Religious Institutions",
        "subcategory": "Mosques / Islamic Centers",
        "services": ["Prayer services (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "74 Chase Dr, Sharon, MA 02067",
        "phone": "",
        "website": "",
        "details": "Islamic center in Sharon (Greater Boston area).",
        "tags": ["mosque", "islam", "sharon", "icne"],
    },

    # Synagogues / Jewish communities
    {  # Temple Israel
        "id": 10201,
        "name": "Temple Israel",
        "category": "Religious Institutions",
        "subcategory": "Synagogues (Jewish)",
        "services": ["Religious services (varies)", "Community programs (varies)"],
        "eligibility": "Open to the public (rules vary)",
        "requirements": [],
        "location": "477 Longwood Ave, Boston, MA 02215",
        "phone": "617-566-3960",
        "website": "",
        "details": "Jewish congregation serving Boston area.",
        "tags": ["synagogue", "jewish", "temple"],
    },
    {  # Walnut Street Synagogue (Chelsea)
        "id": 10202,
        "name": "Walnut Street Synagogue",
        "category": "Religious Institutions",
        "subcategory": "Synagogues (Jewish)",
        "services": ["Religious services (varies)"],
        "eligibility": "Open to the public (rules vary)",
        "requirements": [],
        "location": "145 Walnut St, Chelsea, MA 02150",
        "phone": "",
        "website": "",
        "details": "Synagogue in Chelsea (Greater Boston area).",
        "tags": ["synagogue", "jewish", "chelsea"],
    },
    {  # Adams Street Shul (Newton)
        "id": 10203,
        "name": "The Adams Street Shul",
        "category": "Religious Institutions",
        "subcategory": "Synagogues (Jewish)",
        "services": ["Religious services (varies)"],
        "eligibility": "Open to the public (rules vary)",
        "requirements": [],
        "location": "168 Adams St, Newton, MA 02460",
        "phone": "617-630-0226",
        "website": "",
        "details": "Synagogue in Newton (Greater Boston area).",
        "tags": ["synagogue", "jewish", "newton"],
    },
    {  # Beth Israel (Malden)
        "id": 10204,
        "name": "Congregation Beth Israel (Malden)",
        "category": "Religious Institutions",
        "subcategory": "Synagogues (Jewish)",
        "services": ["Religious services (varies)"],
        "eligibility": "Open to the public (rules vary)",
        "requirements": [],
        "location": "10 Dexter St, Malden, MA 02148",
        "phone": "",
        "website": "",
        "details": "Synagogue in Malden (Greater Boston area).",
        "tags": ["synagogue", "jewish", "malden"],
    },

    # =========================
    # HALAL FOOD PLACES
    # =========================
    {  # Halal Guys
        "id": 11001,
        "name": "The Halal Guys",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Halal platters", "Gyro", "Chicken", "Falafel (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "137 Stuart St, Boston, MA 02116",
        "phone": "857-250-2279",
        "website": "https://thehalalguys.com/locations/137-stuart-street-boston/",
        "details": "Halal food restaurant in Boston.",
        "tags": ["halal", "restaurant", "gyro", "chicken", "falafel"],
    },
    {  # Black Seed
        "id": 11002,
        "name": "Black Seed Halal Grill",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Halal meals (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "140 Tremont St, Boston, MA 02111",
        "phone": "",
        "website": "",
        "details": "Halal grill in downtown Boston area.",
        "tags": ["halal", "grill", "restaurant"],
    },
    {  # Ali Baba
        "id": 11003,
        "name": "Ali Baba",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Halal meals (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "145 E Berkeley St, Boston, MA 02118",
        "phone": "",
        "website": "",
        "details": "Halal-friendly dining option (confirm current halal offerings).",
        "tags": ["halal", "restaurant"],
    },
    {  # Sufra
        "id": 11004,
        "name": "Sufra Mediterranean Food",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Mediterranean food (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "52 Queensberry St, Boston, MA 02215",
        "phone": "",
        "website": "",
        "details": "Mediterranean spot near Fenway area (confirm halal options).",
        "tags": ["halal", "mediterranean", "restaurant"],
    },
    {  # Mo’Rockin
        "id": 11005,
        "name": "Mo’Rockin Fusion",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Fusion cuisine (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "100 Hanover St, Boston, MA 02108",
        "phone": "",
        "website": "",
        "details": "Fusion dining option (confirm halal offerings).",
        "tags": ["halal", "restaurant"],
    },
    {  # Lazuri Cafe
        "id": 11006,
        "name": "Turkish Lazuri Cafe",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Cafe food (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "1 N Beacon St, Allston, MA 02134",
        "phone": "",
        "website": "",
        "details": "Cafe in Allston area (confirm halal offerings).",
        "tags": ["halal", "turkish", "cafe"],
    },
    {  # Shah’s
        "id": 11007,
        "name": "Shah’s Halal Food",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Halal platters (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "1124 Boylston St, Boston, MA 02115",
        "phone": "",
        "website": "",
        "details": "Halal food spot near Boylston St (confirm current details).",
        "tags": ["halal", "restaurant"],
    },
    {  # Ashur
        "id": 11008,
        "name": "Ashur Restaurant",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Restaurant meals (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "291 Roxbury St, Roxbury, MA 02119",
        "phone": "",
        "website": "",
        "details": "Restaurant in Roxbury area (confirm halal offerings).",
        "tags": ["halal", "restaurant", "roxbury"],
    },
    {  # NACHLO
        "id": 11009,
        "name": "NACHLO",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Restaurant meals (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "1443 Tremont St, Boston, MA 02120",
        "phone": "",
        "website": "",
        "details": "Dining option near Mission Hill area (confirm halal offerings).",
        "tags": ["halal", "restaurant"],
    },
    {  # Cafe Vanak (near Boston)
        "id": 11010,
        "name": "Cafe Vanak",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Cafe meals (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "271-275 Belmont St, Belmont, MA 02478",
        "phone": "",
        "website": "",
        "details": "Cafe near Boston (confirm halal offerings).",
        "tags": ["halal", "cafe", "belmont"],
    },
    {  # In House Cafe (Brighton)
        "id": 11011,
        "name": "In House Cafe",
        "category": "Food & Dining",
        "subcategory": "Halal Restaurants",
        "services": ["Halal sandwiches & more (varies)"],
        "eligibility": "Open to the public",
        "requirements": [],
        "location": "132 Chestnut Hill Ave, Brighton, MA 02135",
        "phone": "",
        "website": "",
        "details": "Cafe with halal options (confirm current menu).",
        "tags": ["halal", "cafe", "brighton", "sandwiches"],
    },
]  # end of resources_data list


# --------------------------------
# SEARCH HELPER: normalize any type
# --------------------------------
def normalize_text(value):  # define a helper function for safe searching
    if value is None:  # if the value is missing
        return ""  # return empty string
    if isinstance(value, list):  # if the value is a list
        return " ".join(str(x) for x in value).lower()  # join list into string and lowercase
    return str(value).lower()  # otherwise, convert to string and lowercase


# -----------------------
# FRONTEND: serve website
# -----------------------
@app.route("/", methods=["GET"])  # route for the homepage
def home():  # handler function for homepage
    return send_from_directory(BASE_DIR, "index.html")  # serve index.html from this same folder


@app.route("/style.css", methods=["GET"])  # route for CSS
def serve_css():  # handler function for CSS
    return send_from_directory(BASE_DIR, "style.css")  # serve style.css from this same folder


@app.route("/app.js", methods=["GET"])  # route for JavaScript
def serve_js():  # handler function for JS
    return send_from_directory(BASE_DIR, "app.js")  # serve app.js from this same folder


# -----------------------
# API: UI translation strings
# -----------------------
@app.route("/api/i18n", methods=["GET"])  # endpoint to return UI translation strings
def get_i18n():  # handler to return UI i18n content
    lang = get_lang()  # read requested language
    payload = UI_I18N.get(lang, UI_I18N["en"])  # load UI strings for lang (fallback to English)
    return jsonify({  # return a JSON response
        "success": True,  # success flag
        "lang": lang,  # the selected language
        "languages": LANG_LABELS,  # language labels so the frontend can build a dropdown
        "ui": payload,  # UI strings for the selected language
    })  # end JSON response


# -----------------------
# API: categories for tabs
# -----------------------
@app.route("/api/categories", methods=["GET"])  # endpoint to list unique categories
def get_categories():  # handler to build category list
    lang = get_lang()  # read requested language
    categories_en = sorted(  # sort categories alphabetically
        list(  # convert set to list
            set(  # use set to remove duplicates
                r.get("category", "").strip()  # get category safely and trim whitespace
                for r in resources_data  # loop through all resources
                if r.get("category", "").strip()  # keep only non-empty categories
            )
        )
    )  # end sort for English categories
    categories_localized = [t_category(c, lang) for c in categories_en]  # translate categories for display in requested language
    return jsonify({  # return JSON response
        "success": True,  # success flag
        "lang": lang,  # include language used
        "categories": categories_localized,  # primary key used by newer frontends
        "data": categories_localized,  # compatibility key used by older frontends expecting json.data
        "categories_en": categories_en,  # include the original English category list for stable filtering
        "count": len(categories_localized),  # include how many categories exist
    })  # end JSON response


# -----------------------
# API: list resources
# -----------------------
@app.route("/api/resources", methods=["GET"])  # endpoint to get resources (optional category filter)
def get_resources():  # handler for resource listing
    lang = get_lang()  # read requested language
    category = request.args.get("category", "").strip()  # read ?category= and trim whitespace (expected in English)
    if category:  # if a category was provided
        filtered = [r for r in resources_data if r.get("category", "").strip() == category]  # filter by exact English match
    else:  # if no category provided
        filtered = resources_data  # return everything
    localized = [localize_resource(r, lang) for r in filtered]  # localize each resource for the requested language
    return jsonify({  # return JSON including count
        "success": True,  # success flag
        "lang": lang,  # the selected language
        "count": len(localized),  # how many records are returned
        "data": localized,  # resource list
    })  # end JSON response


# -----------------------
# API: search resources
# -----------------------
@app.route("/api/search", methods=["GET"])  # endpoint for full-text-ish search
def search():  # handler for searching
    lang = get_lang()  # read requested language
    q = request.args.get("q", "")  # read ?q=
    q_norm = normalize_text(q).strip()  # normalize query text
    if not q_norm:  # if query is empty
        localized_all = [localize_resource(r, lang) for r in resources_data]  # localize everything
        return jsonify({  # return all resources
            "success": True,  # success flag
            "lang": lang,  # selected language
            "count": len(localized_all),  # total count
            "data": localized_all,  # full dataset
        })  # end JSON response

    results = []  # list to collect matches
    for r in resources_data:  # loop each resource
        haystack = " ".join([  # build one big searchable string from many fields
            normalize_text(r.get("name")),  # search name
            normalize_text(r.get("category")),  # search category
            normalize_text(r.get("subcategory")),  # search subcategory
            normalize_text(r.get("details")),  # search description
            normalize_text(r.get("location")),  # search address/location
            normalize_text(r.get("phone")),  # search phone
            normalize_text(r.get("website")),  # search website
            normalize_text(r.get("services")),  # search services list
            normalize_text(r.get("eligibility")),  # search eligibility text
            normalize_text(r.get("requirements")),  # search requirements list
            normalize_text(r.get("tags")),  # search tags list
        ])  # end haystack
        if q_norm in haystack:  # if query appears in the combined text
            results.append(r)  # include this resource
    localized_results = [localize_resource(r, lang) for r in results]  # localize matches for requested language
    return jsonify({  # return matches
        "success": True,  # success flag
        "lang": lang,  # selected language
        "count": len(localized_results),  # match count
        "data": localized_results,  # localized matches
    })  # end JSON response


if __name__ == "__main__":  # only run this when launching locally with `python app.py`
    port = int(os.environ.get("PORT", "5001"))  # use platform-provided PORT in production or default to 5001 locally
    app.run(host="0.0.0.0", port=port, debug=True)  # listen on all interfaces so cloud hosting can route traffic to your app
