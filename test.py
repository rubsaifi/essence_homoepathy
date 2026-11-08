import streamlit as st
from pathlib import Path
from datetime import date, time
from database import init_db, save_appointment
from assistant import clinic_assistant_reply

st.set_page_config(
    page_title="Essence Homeopathy | Dr Faihad Waris Saifi",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

# ---------- Olive green + white theme ----------
st.markdown("""
<style>
:root { --olive:#65743A; --olive-dark:#455326; --olive-soft:#EEF1E5; --ink:#24301F; }
.stApp { background:#FFFFFF; color:var(--ink); }
[data-testid="stHeader"] { background:rgba(255,255,255,0.96); }
.block-container { max-width:1180px; padding-top:1.4rem; padding-bottom:3rem; }
section[data-testid="stSidebar"] { background:#F5F7F0; }
h1,h2,h3 { color:#455326 !important; }
p,li,label { color:#35402E; }
div.stButton > button, div.stFormSubmitButton > button {
    background:#65743A; color:white; border:1px solid #65743A;
    border-radius:10px; padding:0.55rem 1.15rem; font-weight:600;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    background:#455326; color:white; border-color:#455326;
}
a { color:#65743A !important; }
.hero {
    background:linear-gradient(115deg,#EEF1E5 0%,#FFFFFF 72%);
    border:1px solid #E2E8D5; border-radius:22px; padding:2.4rem 2.2rem;
}
.eyebrow { color:#65743A; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; font-size:0.78rem; }
.hero-title { color:#455326; font-size:clamp(2.2rem,5vw,3.7rem); line-height:1.05; font-weight:800; margin:0.45rem 0 0.8rem; }
.hero-copy { color:#4D5943; font-size:1.08rem; max-width:680px; }
.info-card {
    background:#F7F8F4; border:1px solid #E5E9DC; border-radius:16px;
    padding:1.15rem; min-height:145px;
}
.info-card h3 { margin-top:0; font-size:1.05rem; }
.pill { display:inline-block; background:#E5EBD8; color:#455326; border-radius:999px; padding:0.35rem 0.75rem; font-size:0.82rem; font-weight:650; }
.small-note { color:#687260; font-size:0.88rem; }
.footer { border-top:1px solid #E7EADF; margin-top:3rem; padding-top:1.2rem; color:#707967; font-size:0.85rem; }
div[data-testid="stChatMessage"] { border:1px solid #E8EDE0; border-radius:14px; }
</style>
""", unsafe_allow_html=True)

# ---------- Header / navigation ----------
left, right = st.columns([2.2, 1], vertical_alignment="center")
with left:
    st.markdown("### 🌿 ESSENCE HOMEOPATHY")
    st.caption("A welcoming space for your consultation")
with right:
    st.markdown('<div style="text-align:right"><span class="pill">Appointments by request</span></div>', unsafe_allow_html=True)

nav = st.radio(
    "Navigate",
    ["Home", "About the Doctor", "Clinic Gallery", "Book Appointment", "AI Clinic Assistant", "Contact"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

if nav == "Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Welcome to Essence Homeopathy</div>
      <div class="hero-title">Your health conversations,<br>with care and attention.</div>
      <div class="hero-copy">Meet <b>Dr Faihad Waris Saifi</b> and get in touch with the clinic to enquire about consultation availability.</div>
      <br><span class="pill">Morning · 10:00 AM – 2:00 PM</span>
      &nbsp; <span class="pill">Evening · 5:00 PM – 9:00 PM</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.subheader("Welcome")
    st.write(
        "Essence Homeopathy provides a simple way to learn about the clinic, "
        "ask administrative questions, and request an appointment. Please contact "
        "the clinic directly for consultation and medical advice."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3>🩺 Personal consultation</h3><p>Connect with the doctor to discuss your concerns during a consultation.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3>📅 Appointment requests</h3><p>Send your preferred date and time. The clinic will confirm availability.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><h3>💬 Clinic assistant</h3><p>Get quick answers about clinic timings and appointment requests.</p></div>', unsafe_allow_html=True)
    st.write("")
    st.info("Clinic timings: Morning 10:00 AM–2:00 PM | Evening 5:00 PM–9:00 PM")

elif nav == "About the Doctor":
    st.title("About the Doctor")
    st.subheader("Dr Faihad Waris Saifi")
    st.write(
        "Dr Faihad Waris Saifi welcomes patients to Essence Homeopathy. "
        "For information about qualifications, registration, areas of practice, "
        "and consultation approach, please contact the clinic."
    )
    st.warning("Doctor qualifications, registration details, and professional credentials should be added here only after they are verified.")


elif nav == "Clinic Gallery":
    st.title("Clinic Gallery")
    st.write("Take a look inside Essence Homeopathy.")
    st.caption("A photo tour of the clinic's entrance, reception, consultation room, and interiors.")

    gallery_images = [
        ("Clinic entrance", "clinic_photo_01.webp"),
        ("Consultation room", "clinic_photo_02.webp"),
        ("Doctor's desk", "clinic_photo_03.webp"),
        ("Clinic glass entrance", "clinic_photo_04.webp"),
        ("Clinic exterior and signboard", "clinic_photo_05.webp"),
        ("Consultation area", "clinic_photo_06.webp"),
        ("Reception and consultation space", "clinic_photo_07.webp"),
        ("Consultation room interior", "clinic_photo_08.webp"),
        ("Doctor's consultation desk", "clinic_photo_09.webp"),
        ("Clinic signboard", "clinic_photo_10.webp"),
        ("Clinic certificates display", "clinic_photo_11.webp"),
        ("Waiting and entrance area", "clinic_photo_12.webp"),
        ("Clinic exterior", "clinic_photo_13.webp"),
    ]

    for start in range(0, len(gallery_images), 3):
        cols = st.columns(3, gap="medium")
        for col, (caption, filename) in zip(cols, gallery_images[start:start + 3]):
            with col:
                image_path = Path(__file__).parent / "assets" / "clinic_gallery" / filename
                st.image(str(image_path), caption=caption, use_container_width=True)
    st.caption("All photographs displayed here were supplied by the clinic.")

elif nav == "Book Appointment":
    st.title("Request an Appointment")
    st.write("Share your preferred appointment details. This is a request only; the clinic must confirm the slot.")
    with st.form("appointment_form", clear_on_submit=True):
        name = st.text_input("Full name *")
        phone = st.text_input("Phone number *", max_chars=20, help="Enter a number the clinic can use to contact you.")
        appt_date = st.date_input("Preferred date", min_value=date.today())
        slot = st.selectbox("Preferred time", ["Morning (10 AM – 2 PM)", "Evening (5 PM – 9 PM)"])
        preferred_time = st.selectbox(
            "Preferred time within the selected session",
            ["10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM"]
            if slot.startswith("Morning") else
            ["5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM"]
        )
        reason = st.text_area(
            "Reason for appointment (optional)",
            placeholder="Please avoid sharing detailed or sensitive medical information in this form.",
            max_chars=300,
        )
        consent = st.checkbox("I agree that the clinic may contact me about this appointment request. *")
        submitted = st.form_submit_button("Send appointment request")
        if submitted:
            if not name.strip() or not phone.strip() or not consent:
                st.error("Please complete your name, phone number, and contact consent.")
            else:
                try:
                    request_id = save_appointment(
                        name=name.strip(), phone=phone.strip(),
                        appt_date=appt_date.isoformat(), session=slot,
                        preferred_time=preferred_time, reason=reason.strip()
                    )
                    st.success(f"Your request has been received. Reference: EH-{request_id:05d}. The clinic will contact you to confirm.")
                except Exception:
                    st.error("We couldn't save your request. Please try again or contact the clinic directly.")
    st.caption("Please do not use this form for emergencies. For urgent symptoms, contact local emergency services or go to the nearest emergency department.")

elif nav == "AI Clinic Assistant":
    st.title("AI Clinic Assistant")
    st.write("Ask about clinic timings, the doctor, or how to request an appointment.")
    st.caption("This assistant provides administrative information only. It does not diagnose, prescribe, or replace a consultation.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I’m the Essence Homeopathy clinic assistant. I can help with clinic timings and appointment requests. How may I help?"}
        ]
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("Type your question...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        answer = clinic_assistant_reply(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

elif nav == "Contact":
    st.title("Contact Essence Homeopathy")
    st.subheader("Dr Faihad Waris Saifi")
    st.write("**Clinic timings**")
    st.write("☀️ Morning: 10:00 AM – 2:00 PM")
    st.write("🌙 Evening: 5:00 PM – 9:00 PM")
    st.markdown("**Clinic address:** 6/31, Geeta Colony Rd, near post office, Block 6, Geeta Colony, New Delhi, Delhi, 110032")
    st.markdown("**Phone / WhatsApp:** +91 9315331235")
    st.markdown("**Google Map :**https://www.google.com/maps/place/Essence-The+Homeopathic+Clinic/@28.6530365,77.2731503,17z/data=!3m1!4b1!4m6!3m5!1s0x390cfd2087a8ca41:0xb4999b0dadd37cbf!8m2!3d28.6530365!4d77.2731503!16s%2Fg%2F11z_208w28?entry=ttu&g_ep=EgoyMDI2MTEwMy4wIKXMDSoASAFQAw%3D%3D")
    

st.markdown("""
<div class="footer">
  <b>Essence Homeopathy</b> · Dr Faihad Waris Saifi<br>
  This website provides clinic and appointment information, not medical diagnosis or treatment.
  In an emergency, seek urgent medical care.
</div>
""", unsafe_allow_html=True)
