from faker import Faker
from datetime import datetime
import random
import gspread
from google.oauth2.service_account import Credentials

# --------- Configuration ---------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = 'credentials.json'  # your service account JSON
SHEET_NAME = 'NPMP Signup Form for 2025-2026 (Responses)'
MENTOR_TAB = 'Mentor Responses'
MENTEE_TAB = 'Mentee Responses'


fake = Faker()

# --------- Possible options ---------
PROGRAMS = ['BSc(N)', 'BNI Online', 'BNI On Campus', 'MScA in Nursing (Direct Entry)', 'MScA in Advanced Nursing (Nurse Entry)', 'MScA in Nurse Practitioner']
YEARS = ['U0 (Undergraduate Year 0)', 'U1 (Undergraduate Year 1)', 'U2 (Undergraduate Year 2)',
         'U3 (Undergraduate Year 3)', 'M1 (Masters Year 1)', 'M2 (Masters Year 2)', 'Graduated']
SPECIALTIES = ['pediatrics', 'Critical Care / ICU' 'geriatrics', 'medical-surgical nursing' 'oncology', 'emergency', 'mental_health / psychiatry', 'community', 'obstetrics / labor & delivery', 'emergency medicine', 'home health', 'public health', 'none']
BASE_LANGUAGES = ['English', 'French']
OTHER_LANGUAGES = ['Spanish', 'Mandarin', 'Arabic', 'Hindi']
EXTRACURRICULARS = ['volunteering', 'student_council', 'research', 'sports', 'arts', 'none']
ETHNICITIES = ['asian / asian american', 'black / african american', 'white / caucasian', 'hispanic / latino', 'indigenous', 'middle_eastern', 'other']
LGBTQ_OPTIONS = ['Yes', 'No', 'Prefer not to answer']
MAX_MENTEES = ['1', '2', '3', 'No preference']

# --------- Setup Google Sheets ---------
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME)
mentor_ws = sheet.worksheet(MENTOR_TAB)
mentee_ws = sheet.worksheet(MENTEE_TAB)

# --------- Helpers ---------
def random_subset(options, max_count=3):
    count = random.randint(0, max_count)
    subset = random.sample(options, count) if count > 0 else []
    return subset if subset else []

def make_email(name):
    return f"{name.lower().replace(' ', '.')}@mail.mcgill.ca"

def generate_languages(i):
    # first entry guarantees "Other"
    if i == 0:
        return "English, Spanish"

    # choose 1–2 base languages
    selected = random.sample(BASE_LANGUAGES, random.randint(1, 2))

    # occasionally add an "Other"
    if random.random() < 0.25:
        selected.append(random.choice(OTHER_LANGUAGES))

    return ", ".join(selected)

# --------- Generate Mentors ---------
mentors = []
for i in range(30):
    name = fake.name()
    program = PROGRAMS[i % len(PROGRAMS)]  # ensure at least one of each program
    year = YEARS[i % len(YEARS)]            # ensure at least one of each year
    specialties = ', '.join(random_subset(SPECIALTIES))
    languages = generate_languages(i)
    extracurriculars = ', '.join(random_subset(EXTRACURRICULARS))
    ethnicity = random.choice(ETHNICITIES)
    lgbtq = random.choice(LGBTQ_OPTIONS)
    max_mentees = random.choice(MAX_MENTEES)
    preferred_mentees = '' if i < 2 else f"Mentee {random.randint(1,10)}, Mentee {random.randint(1,10)}"
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    interest = 'Yes'
    feedback = ''
    consent = 'Yes'

    # order is important
    row = [
        timestamp,
        name,
        make_email(name),
        program,
        year,
        languages,
        specialties,
        extracurriculars,
        ethnicity,
        lgbtq,
        preferred_mentees,
        interest,
        feedback,
        max_mentees,
        consent
        
    ]
    mentors.append(row)
mentor_ws.append_rows(mentors)

mentees = []
# --------- Generate Mentees ---------
for i in range(50):
    name = fake.name()
    program = PROGRAMS[i % len(PROGRAMS)]
    year = YEARS[i % len(YEARS)]
    specialties = ', '.join(random_subset(SPECIALTIES))
    languages = generate_languages(i)
    extracurriculars = ', '.join(random_subset(EXTRACURRICULARS))
    ethnicity = random.choice(ETHNICITIES)
    lgbtq = random.choice(LGBTQ_OPTIONS)
    preferred_mentor = '' if i < 2 else f"Mentor {random.randint(1,10)}, Mentor {random.randint(1,10)}"
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    interest = 'Yes'
    consent = 'Yes'

    row = [
        timestamp,
        name,
        make_email(name),
        program,
        year,
        languages,
        specialties,
        extracurriculars,
        ethnicity,
        lgbtq,
        preferred_mentor, 
        interest
    ]
    mentees.append(row)

mentee_ws.append_rows(mentees)

print("Sample data added: 30 mentors and 50 mentees.")