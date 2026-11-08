import streamlit as st
from pathlib import Path
from datetime import date, time
import base64
import html as html_lib
import streamlit.components.v1 as components
from assistant import clinic_assistant_reply

st.set_page_config(
    page_title="Essence Homeopathy | Dr Faihad Waris Saifi",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()

ASSET_DIR = Path(__file__).parent / "assets"

def find_asset(*filenames):
    """Return the first matching asset path, ignoring filename case."""
    if not ASSET_DIR.exists():
        return None
    available = {p.name.lower(): p for p in ASSET_DIR.iterdir() if p.is_file()}
    for filename in filenames:
        match = available.get(filename.lower())
        if match and match.exists():
            return match
    return None

# ---------- Olive green + white theme ----------
st.markdown("""
<style>
:root { --olive:#65743A; --olive-dark:#123D32; --olive-soft:#EEF4E9; --ink:#24301F; --mint:#C7DEC9; }
.stApp { background:#FFFFFF; color:var(--ink); }
[data-testid="stHeader"] { background:rgba(255,255,255,0.96); }
.block-container { max-width:1220px; padding-top:1.15rem; padding-bottom:3rem; }
h1,h2,h3 { color:#123D32 !important; }
p,li,label { color:#35402E; }
a { color:#65743A !important; }
div.stButton > button, div.stFormSubmitButton > button {
    background:#65743A; color:white; border:1px solid #65743A;
    border-radius:12px; padding:0.6rem 1.2rem; font-weight:650;
    transition:all .22s ease; box-shadow:0 4px 12px rgba(69,83,38,.10);
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    background:#455326; color:white; border-color:#455326;
    transform:translateY(-2px); box-shadow:0 7px 18px rgba(69,83,38,.18);
}
.hero {
    background:linear-gradient(115deg,#EEF4E9 0%,#FFFFFF 72%);
    border:1px solid #DDE8D9; border-radius:24px; padding:2.5rem 2.2rem;
    box-shadow:0 12px 32px rgba(18,61,50,.06);
    animation:fadeUp .75s ease both;
}
.eyebrow { color:#65743A; font-weight:750; letter-spacing:.13em; text-transform:uppercase; font-size:.78rem; }
.hero-title { color:#123D32; font-size:clamp(2.2rem,5vw,3.7rem); line-height:1.05; font-weight:850; margin:.45rem 0 .8rem; }
.hero-copy { color:#4D5943; font-size:1.08rem; max-width:680px; }
.info-card {
    background:#F7F9F5; border:1px solid #E2EADD; border-radius:18px;
    padding:1.25rem; min-height:145px; height:100%;
    transition:transform .25s ease, box-shadow .25s ease;
    animation:fadeUp .7s ease both;
}
.info-card:hover { transform:translateY(-5px); box-shadow:0 12px 24px rgba(18,61,50,.09); }
.info-card h3 { margin-top:0; font-size:1.05rem; }
.pill { display:inline-block; background:#E5EBD8; color:#455326; border-radius:999px; padding:.38rem .8rem; font-size:.82rem; font-weight:700; }
.small-note { color:#687260; font-size:.88rem; }
.footer { border-top:1px solid #E7EADF; margin-top:3rem; padding-top:1.2rem; color:#707967; font-size:.85rem; }
div[data-testid="stChatMessage"] { border:1px solid #E8EDE0; border-radius:14px; }
div[role="radiogroup"] {
    gap:.55rem !important; flex-wrap:wrap; padding:.55rem;
    background:linear-gradient(100deg,#F5F7F1,#FFFFFF);
    border:1px solid #E2EADD; border-radius:18px;
    box-shadow:0 7px 22px rgba(18,61,50,.055);
}
div[role="radiogroup"] label {
    position:relative; overflow:hidden;
    background:#FFFFFF; border:1px solid #DDE6D5; border-radius:999px;
    padding:.58rem 1rem; transition:all .28s cubic-bezier(.2,.8,.2,1);
    cursor:pointer; box-shadow:0 2px 7px rgba(18,61,50,.035);
}
div[role="radiogroup"] label:hover {
    background:#EAF0E3; border-color:#9DAE83;
    transform:translateY(-3px); box-shadow:0 7px 15px rgba(18,61,50,.10);
}
div[role="radiogroup"] label[data-checked="true"] {
    background:#123D32 !important; border-color:#123D32 !important;
    color:#fff !important; box-shadow:0 6px 16px rgba(18,61,50,.20);
    animation:navPop .28s ease both;
}
div[role="radiogroup"] label[data-checked="true"] * { color:#fff !important; }
div[role="radiogroup"] label[data-checked="true"]::after {
    content:""; position:absolute; left:22%; right:22%; bottom:3px;
    height:2px; border-radius:9px; background:#C7DEC9;
    animation:navUnderline .35s ease both;
}
@keyframes navPop {
    0% { transform:scale(.96) translateY(2px); }
    70% { transform:scale(1.025); }
    100% { transform:scale(1) translateY(0); }
}
@keyframes navUnderline {
    from { transform:scaleX(.2); opacity:0; }
    to { transform:scaleX(1); opacity:1; }
}
[data-testid="stImage"] img { border-radius:16px; }
.section-kicker { color:#65743A; font-size:.78rem; font-weight:750; letter-spacing:.12em; text-transform:uppercase; }
.doctor-panel { background:#F7F9F5; border:1px solid #E2EADD; border-radius:20px; padding:1.2rem; }
@keyframes fadeUp { from {opacity:0; transform:translateY(16px);} to {opacity:1; transform:translateY(0);} }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration:.01ms !important; transition-duration:.01ms !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Header / navigation ----------
left, right = st.columns([2.2, 1], vertical_alignment="center")
with left:
    st.markdown("### 🌿 ESSENCE HOMEOPATHY")
    st.caption("A welcoming space for your consultation")
with right:
    st.markdown('<div style="text-align:right"><span class="pill">Appointments by request</span></div>', unsafe_allow_html=True)

st.markdown('<div class="section-kicker">Explore the clinic</div>', unsafe_allow_html=True)
nav = st.radio(
    "Navigate",
    ["Home", "About the Doctor", "Clinic Gallery", "Book Appointment", "AI Clinic Assistant", "Contact", "Admin Dashboard"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

if nav == "Home":
    left, right = st.columns([1.65, 1], gap="large", vertical_alignment="center")
    with left:
        st.markdown("""
        <div class="hero">
          <div class="eyebrow">Welcome to Essence Homeopathy</div>
          <div class="hero-title">Care that begins<br>with listening.</div>
          <div class="hero-copy">Meet <b>Dr Faihad Waris Saifi</b> and connect with our clinic to enquire about consultation availability.</div>
          <br><span class="pill">☀️ Morning · 10 AM – 2 PM</span>
          &nbsp; <span class="pill">🌙 Evening · 5 PM – 9 PM</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("### A warm welcome")
        st.write(
            "Explore the clinic, learn about the doctor, and send an appointment request. "
            "For diagnosis and treatment advice, please speak directly with the doctor."
        )
    with right:
        doctor_photo = find_asset("Dr.jpg", "dr.jpg", "Doctor.jpg", "doctor.jpg")
        if doctor_photo is not None and doctor_photo.exists():
            st.image(str(doctor_photo), caption="Dr Faihad Waris Saifi", use_container_width=True)
        else:
            st.markdown('<div class="doctor-panel"><div class="section-kicker">Your doctor</div><h2>Dr Faihad Waris Saifi</h2><p>Essence Homeopathy</p><p class="small-note">Add the doctor portrait as <b>assets/Dr.jpg</b> to display it here.</p></div>', unsafe_allow_html=True)

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3>🩺 Personal consultation</h3><p>Connect with the doctor to discuss your concerns during a consultation.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3>📅 Appointment requests</h3><p>Share your preferred date and time. The clinic will confirm availability.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><h3>🌿 Visit the clinic</h3><p>View clinic photographs and find directions before your visit.</p></div>', unsafe_allow_html=True)
    st.write("")
    st.info("Clinic timings: Morning 10:00 AM–2:00 PM | Evening 5:00 PM–9:00 PM")

elif nav == "About the Doctor":
    st.markdown('<div class="section-kicker">Meet your doctor</div>', unsafe_allow_html=True)
    st.title("Dr Faihad Waris Saifi")
    photo_col, detail_col = st.columns([1, 1.7], gap="large", vertical_alignment="center")
    doctor_photo = find_asset("Dr.jpg", "dr.jpg", "Doctor.jpg", "doctor.jpg")
    with photo_col:
        if doctor_photo is not None and doctor_photo.exists():
            st.image(str(doctor_photo), caption="Dr Faihad Waris Saifi", use_container_width=True)
        else:
            st.info("Doctor profile photo not found. Place the image at assets/Dr.jpg.")
    with detail_col:
        st.markdown("### Welcome to Essence Homeopathy")
        st.write(
            "Dr Faihad Waris Saifi welcomes patients to Essence Homeopathy. "
            "For verified information about qualifications, registration, areas of practice, "
            "and consultation approach, please contact the clinic."
        )
        st.markdown('<span class="pill">BHMS · NHMC (Delhi University)</span>', unsafe_allow_html=True)
        st.caption("Please verify the displayed qualification and registration details before publishing.")
        st.warning("Professional credentials and registration details should be checked against the original documents before the website goes live.")

elif nav == "Clinic Gallery":
    st.title("Clinic Gallery")
    st.write("A little look inside Essence Homeopathy.")
    st.caption("The photo strip moves automatically. Hover over it to pause.")

    gallery_dir = Path(__file__).parent / "assets" / "clinic_gallery"
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

    # Build a seamless, automatically scrolling strip from the local clinic photos.
    cards = []
    for caption, filename in gallery_images:
        image_path = gallery_dir / filename
        if image_path.exists():
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            cards.append(
                f'<div class="gallery-card"><img src="data:image/webp;base64,{encoded}" alt="{html_lib.escape(caption)}">'
                f'<div class="gallery-caption">{html_lib.escape(caption)}</div></div>'
            )
    if cards:
        card_html = "".join(cards)
        components.html(f"""
        <style>
          * {{ box-sizing:border-box; }}
          .gallery-window {{ width:100%; overflow:hidden; padding:10px 0 18px; }}
          .gallery-track {{ display:flex; width:max-content; gap:18px; animation:galleryScroll 48s linear infinite; }}
          .gallery-window:hover .gallery-track {{ animation-play-state:paused; }}
          .gallery-card {{ width:290px; flex:0 0 290px; background:#F7F9F5; border:1px solid #E2EADD; border-radius:17px; overflow:hidden; box-shadow:0 7px 20px rgba(18,61,50,.08); }}
          .gallery-card img {{ display:block; width:100%; height:205px; object-fit:cover; }}
          .gallery-caption {{ padding:11px 13px; color:#294337; font:600 14px Arial,sans-serif; }}
          @keyframes galleryScroll {{ from {{ transform:translateX(0); }} to {{ transform:translateX(calc(-50% - 9px)); }} }}
          @media (prefers-reduced-motion: reduce) {{ .gallery-track {{ animation:none; }} }}
        </style>
        <div class="gallery-window"><div class="gallery-track">{card_html}{card_html}</div></div>
        """, height=270, scrolling=False)
    else:
        st.warning("No gallery photos were found in assets/clinic_gallery.")

    st.subheader("Explore the clinic")
    for start_idx in range(0, len(gallery_images), 3):
        cols = st.columns(3, gap="medium")
        for col, (caption, filename) in zip(cols, gallery_images[start_idx:start_idx + 3]):
            image_path = gallery_dir / filename
            if image_path.exists():
                with col:
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
    st.info("Clinic address and phone number have not yet been provided. Add verified details in the configuration before publishing this website.")
    st.markdown("**Clinic address:** To be added")
    st.markdown("**Phone / WhatsApp:** +91 95554 31235")
    st.markdown("[Call the clinic](tel:+919555431235) · [WhatsApp the clinic](https://wa.me/919555431235)")
    st.write("")
    qr_path = find_asset("qr_Code.jpg", "QR_Code.jpg", "qr_code.jpg", "QR_Code.png", "qr_code.png")
    qr_col, map_col = st.columns([1, 1.6], gap="large", vertical_alignment="center")
    with qr_col:
        if qr_path is not None and qr_path.exists():
            st.image(str(qr_path), caption="Scan to open the clinic location", width=230)
        else:
            st.info("Map QR image not found. Add qr_Code.jpg or QR_Code.png inside the assets folder.")
    with map_col:
        st.markdown("### Find the clinic")
        st.write("Scan the QR code or open the clinic location in Google Maps.")
        st.link_button("Open Google Maps", "https://www.google.com/maps/place/Essence-The+Homeopathic+Clinic/@28.6530365,77.2731503,17z/")


elif nav == "Admin Dashboard":
    st.title("Clinic Admin Dashboard")
    st.caption("Private clinic workspace · appointment and collection management")

    def read_admin_password():
        import os
        password = os.getenv("ESSENCE_ADMIN_PASSWORD", "")
        try:
            password = st.secrets.get("ESSENCE_ADMIN_PASSWORD", password)
        except Exception:
            pass
        return password

    configured_password = read_admin_password()
    if not configured_password:
        st.warning("Admin access is locked until you configure ESSENCE_ADMIN_PASSWORD. Do not publish the admin dashboard with an empty password.")
        st.code('export ESSENCE_ADMIN_PASSWORD="use-a-long-unique-password"', language="bash")
        st.caption("For Streamlit Community Cloud, add ESSENCE_ADMIN_PASSWORD under App → Settings → Secrets.")
    else:
        if not st.session_state.get("admin_authenticated", False):
            with st.form("admin_login"):
                entered_password = st.text_input("Admin password", type="password")
                login_clicked = st.form_submit_button("Sign in")
                if login_clicked:
                    if entered_password == configured_password:
                        st.session_state.admin_authenticated = True
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
        else:
            top_left, top_right = st.columns([4, 1])
            with top_right:
                if st.button("Sign out"):
                    st.session_state.admin_authenticated = False
                    st.rerun()

            appointments = get_appointments()
            payments = get_payments()
            today_text = date.today().isoformat()
            total_appointments = len(appointments)
            pending_count = sum(1 for row in appointments if row["status"] == "Pending")
            today_count = sum(1 for row in appointments if row["appointment_date"] == today_text)
            total_revenue = sum(float(row["amount"]) for row in payments)
            month_prefix = date.today().strftime("%Y-%m")
            month_revenue = sum(float(row["amount"]) for row in payments if row["payment_date"].startswith(month_prefix))

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total requests", total_appointments)
            m2.metric("Pending", pending_count)
            m3.metric("Today's appointments", today_count)
            m4.metric("Recorded collections", f"₹{total_revenue:,.0f}")
            st.metric("Collections this month", f"₹{month_revenue:,.0f}")

            st.subheader("Appointment requests")
            if appointments:
                import pandas as pd
                rows = [dict(row) for row in appointments]
                display_rows = [{
                    "ID": f"EH-{r['id']:05d}",
                    "Patient": r["name"],
                    "Phone": r["phone"],
                    "Date": r["appointment_date"],
                    "Session": r["session"],
                    "Preferred time": r["preferred_time"],
                    "Status": r["status"],
                    "Received": r["created_at"],
                } for r in rows]
                st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)
                st.markdown("**Update appointment status**")
                selected_id = st.selectbox(
                    "Select request",
                    options=[r["id"] for r in rows],
                    format_func=lambda value: next(
                        f"EH-{r['id']:05d} · {r['name']} · {r['appointment_date']} · {r['status']}"
                        for r in rows if r["id"] == value
                    )
                )
                selected_row = next(r for r in rows if r["id"] == selected_id)
                new_status = st.selectbox(
                    "New status",
                    ["Pending", "Confirmed", "Completed", "Cancelled"],
                    index=["Pending", "Confirmed", "Completed", "Cancelled"].index(selected_row["status"])
                )
                if st.button("Save appointment status"):
                    update_appointment_status(selected_id, new_status)
                    st.success("Appointment status updated.")
                    st.rerun()
                with st.expander("View request note"):
                    st.write(selected_row.get("reason") or "No note provided.")
            else:
                st.info("No appointment requests yet.")

            st.divider()
            st.subheader("Record a clinic collection")
            with st.form("record_payment", clear_on_submit=True):
                pay_col1, pay_col2 = st.columns(2)
                with pay_col1:
                    patient_name = st.text_input("Patient name")
                    amount = st.number_input("Amount received (₹)", min_value=0.0, step=100.0)
                with pay_col2:
                    payment_date = st.date_input("Payment date", value=date.today())
                    payment_method = st.selectbox("Payment method", ["Cash", "UPI", "Card", "Bank transfer", "Other"])
                payment_notes = st.text_input("Notes (optional)")
                payment_submitted = st.form_submit_button("Save collection")
                if payment_submitted:
                    if not patient_name.strip() or amount <= 0:
                        st.error("Enter a patient name and an amount greater than zero.")
                    else:
                        save_payment(
                            patient_name=patient_name.strip(),
                            amount=amount,
                            payment_date=payment_date.isoformat(),
                            payment_method=payment_method,
                            notes=payment_notes.strip()
                        )
                        st.success("Collection recorded.")
                        st.rerun()

            st.subheader("Recent collections")
            if payments:
                payment_rows = [{
                    "Date": r["payment_date"],
                    "Patient": r["patient_name"],
                    "Amount (₹)": f"{float(r['amount']):,.2f}",
                    "Method": r["payment_method"],
                    "Notes": r["notes"] or "",
                } for r in payments]
                st.dataframe(pd.DataFrame(payment_rows), use_container_width=True, hide_index=True)
            else:
                st.caption("No collections have been recorded yet.")

            st.warning("This starter admin area uses password protection but is not a full clinical record system. Use HTTPS, a strong unique password, restricted hosting, backups, and a privacy review before storing real patient information. Avoid entering diagnosis or detailed medical history here.")


st.markdown("""
<div class="footer">
  <b>Essence Homeopathy</b> · Dr Faihad Waris Saifi<br>
  This website provides clinic and appointment information, not medical diagnosis or treatment.
  In an emergency, seek urgent medical care.
</div>
""", unsafe_allow_html=True)
