# Essence Homeopathy — Streamlit website MVP

A responsive, olive-green-and-white clinic website for:
- Essence Homeopathy
- Dr Faihad Waris Saifi
- Morning: 10:00 AM–2:00 PM
- Evening: 5:00 PM–9:00 PM

## Included
- Clinic Gallery tab containing all 13 clinic photographs supplied for this project
- Home, doctor information, clinic photo gallery, appointment request, AI clinic assistant, and contact sections
- Appointment request storage in a local SQLite database
- Optional OpenAI-powered administrative FAQ assistant
- Safe fallback FAQ assistant when no API key is configured
- Medical-safety guardrails: no diagnosis, prescribing, dosage advice, or cure claims

## Run locally

Python 3.10+ recommended.

### macOS / Linux
```bash
cd essence_homeopathy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell
```powershell
cd essence_homeopathy
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Optional AI configuration

The website works without an API key. To enable the LLM-backed administrative assistant:

1. Copy `.env.example` to `.env`.
2. Add your API key to `.env`.
3. Install `python-dotenv` or, preferably, configure the key as a Streamlit secret/environment variable.

For Streamlit secrets, create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-key-here"
OPENAI_MODEL = "gpt-4o-mini"
```

Then update `assistant.py` to read `st.secrets` or export the environment variables before running. Never commit secrets to GitHub.

## Before publishing
The following details are intentionally not invented and must be added:
- Clinic address and map link
- Phone / WhatsApp number
- Verified doctor qualifications and registration details
- Any approved description of services
- Privacy notice, data-retention policy, and clinic contact for privacy requests

## Important privacy and safety notes
- The appointment form stores data locally in `clinic.db`. This is suitable only for a local prototype, not a production patient-record system.
- Do not collect detailed health histories through this basic form.
- Before collecting real patient information or deploying publicly, arrange appropriate security, access controls, encryption, backups, retention/deletion processes, consent, and a legal review of applicable Indian data-protection and professional rules.
- The AI assistant is for administrative information only. It must not diagnose, prescribe, recommend remedies, or replace medical care.
- The clinic must confirm every appointment request manually. The form does not show live availability.

## Admin note
This MVP does not yet include an admin dashboard. Appointment requests are stored in `clinic.db`; add a properly authenticated staff-only dashboard before using it operationally.
