import base64
import html
from datetime import date
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

# The assistant is optional. The website will still run if assistant.py
# or one of its optional AI dependencies is unavailable.
try:
    from assistant import clinic_assistant_reply
except Exception:
    clinic_assistant_reply = None


st.set_page_config(
    page_title="Essence Homeopathy | Dr. Faihed Waris Saifi",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"

# Verify this number with the clinic before publishing.
CLINIC_WHATSAPP = "919315331235"


def find_asset(*filenames):
    """Return the first matching file in assets/, ignoring filename case."""
    if not ASSET_DIR.exists():
        return None

    available = {
        path.name.lower(): path
        for path in ASSET_DIR.iterdir()
        if path.is_file()
    }
    for filename in filenames:
        match = available.get(filename.lower())
        if match and match.is_file():
            return match
    return None


# ---------------- Olive green + white theme ----------------
st.markdown(
    """
    <style>
    :root {
        --olive: #65743A;
        --olive-dark: #123D32;
        --olive-soft: #EEF4E9;
        --ink: #24301F;
        --mint: #C7DEC9;
    }
    .stApp { background: #FFFFFF; color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(255,255,255,0.96); }
    .block-container { max-width: 1220px; padding-top: 1.15rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #123D32 !important; }
    p, li, label { color: #35402E; }
    a { color: #65743A !important; }
    div.stButton > button, div.stFormSubmitButton > button,
    div.stLinkButton > a {
        background: #65743A; color: white !important; border: 1px solid #65743A;
        border-radius: 12px; padding: 0.6rem 1.2rem; font-weight: 650;
        transition: all .22s ease; box-shadow: 0 4px 12px rgba(69,83,38,.10);
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover,
    div.stLinkButton > a:hover {
        background: #455326; color: white !important; border-color: #455326;
        transform: translateY(-2px); box-shadow: 0 7px 18px rgba(69,83,38,.18);
    }
    .hero {
        background: linear-gradient(115deg,#EEF4E9 0%,#FFFFFF 72%);
        border: 1px solid #DDE8D9; border-radius: 24px; padding: 2.5rem 2.2rem;
        box-shadow: 0 12px 32px rgba(18,61,50,.06);
        animation: fadeUp .75s ease both;
    }
    .eyebrow { color: #65743A; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; font-size: .78rem; }
    .hero-title { color: #123D32; font-size: clamp(2.2rem,5vw,3.7rem); line-height: 1.05; font-weight: 850; margin: .45rem 0 .8rem; }
    .hero-copy { color: #4D5943; font-size: 1.08rem; max-width: 680px; }
    .info-card {
        background: #F7F9F5; border: 1px solid #E2EADD; border-radius: 18px;
        padding: 1.25rem; min-height: 145px; height: 100%;
        transition: transform .25s ease, box-shadow .25s ease;
        animation: fadeUp .7s ease both;
    }
    .info-card:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(18,61,50,.09); }
    .info-card h3 { margin-top: 0; font-size: 1.05rem; }
    .pill { display: inline-block; background: #E5EBD8; color: #455326; border-radius: 999px; padding: .38rem .8rem; font-size: .82rem; font-weight: 700; }
    .small-note { color: #687260; font-size: .88rem; }
    .footer { border-top: 1px solid #E7EADF; margin-top: 3rem; padding-top: 1.2rem; color: #707967; font-size: .85rem; }
    div[data-testid="stChatMessage"] { border: 1px solid #E8EDE0; border-radius: 14px; }
    div[role="radiogroup"] {
        gap: .55rem !important; flex-wrap: wrap; padding: .55rem;
        background: linear-gradient(100deg,#F5F7F1,#FFFFFF);
        border: 1px solid #E2EADD; border-radius: 18px;
        box-shadow: 0 7px 22px rgba(18,61,50,.055);
    }
    div[role="radiogroup"] label {
        position: relative; overflow: hidden; background: #FFFFFF;
        border: 1px solid #DDE6D5; border-radius: 999px; padding: .58rem 1rem;
        transition: all .28s cubic-bezier(.2,.8,.2,1); cursor: pointer;
        box-shadow: 0 2px 7px rgba(18,61,50,.035);
    }
    div[role="radiogroup"] label:hover {
        background: #EAF0E3; border-color: #9DAE83;
        transform: translateY(-3px); box-shadow: 0 7px 15px rgba(18,61,50,.10);
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background: #123D32 !important; border-color: #123D32 !important;
        color: #fff !important; box-shadow: 0 6px 16px rgba(18,61,50,.20);
        animation: navPop .28s ease both;
    }
    div[role="radiogroup"] label[data-checked="true"] * { color: #fff !important; }
    @keyframes navPop {
        0% { transform: scale(.96) translateY(2px); }
        70% { transform: scale(1.025); }
        100% { transform: scale(1) translateY(0); }
    }
    [data-testid="stImage"] img { border-radius: 16px; }
    .brand-banner {
        background: #A8BFAE; width: 100vw; box-sizing: border-box; overflow: visible;
        margin-left: calc(50% - 50vw); margin-bottom: 1rem;
        padding: 1rem max(1rem, calc((100vw - 1220px) / 2));
    }
    .brand-inner { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; max-width: 1220px; min-width: 0; margin: 0 auto; overflow: visible; }
    .brand-logo { display: block; width: 96px; height: auto; max-height: none; object-fit: contain; object-position: center; flex: 0 0 auto; }
    .brand-copy { min-width: 0; }
    .brand-name { color: #123D32; font-size: clamp(1.15rem, 2.8vw, 1.9rem); font-weight: 850; line-height: 1.12; overflow-wrap: anywhere; }
    .brand-tagline { color: #294337; font-size: .9rem; margin-top: .22rem; }
    .brand-appointment { margin-left: auto; flex: 0 0 auto; background: rgba(255,255,255,.72); color: #294337; border-radius: 999px; padding: .45rem .8rem; font-size: .84rem; font-weight: 700; }
    @media (max-width: 600px) {
        .brand-banner { padding: .85rem 1rem; }
        .brand-inner { gap: .65rem; }
        .brand-logo { width: 76px; height: auto; }
        .brand-name { font-size: clamp(1rem, 5vw, 1.4rem); }
        .brand-tagline { font-size: .8rem; }
        .brand-appointment { font-size: .76rem; padding: .4rem .65rem; }
    }
    .section-kicker { color: #65743A; font-size: .78rem; font-weight: 750; letter-spacing: .12em; text-transform: uppercase; }
    .area-card {
        background: linear-gradient(145deg,#FFFFFF 0%,#F7F9F5 100%);
        border: 1px solid #E2EADD; border-radius: 20px; padding: 1.2rem;
        min-height: 100%; box-shadow: 0 7px 20px rgba(18,61,50,.055);
        transition: transform .28s ease, box-shadow .28s ease;
        animation: fadeUp .7s ease both;
    }
    .area-card:hover { transform: translateY(-7px) scale(1.01); box-shadow: 0 18px 34px rgba(18,61,50,.15); }
    .area-image-frame { width: 100%; height: 260px; overflow: hidden; border-radius: 16px; margin-bottom: 1rem; background: #EAF1E6; }
    .area-image { display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% 45%; animation: imageDrift 14s ease-in-out infinite alternate; transition: transform .6s cubic-bezier(.2,.8,.2,1); }
    .area-card:hover .area-image { transform: scale(1.08); }
    .area-card h3 { margin: .1rem 0 .7rem; font-size: 1.1rem; }
    .condition-list { list-style: none; padding: 0; margin: .65rem 0 0; }
    .condition-list li { display: flex; align-items: center; gap: .65rem; padding: .55rem 0; border-top: 1px solid #E7EADF; color: #35402E; }
    .condition-icon { display: grid; place-items: center; flex: 0 0 34px; width: 34px; height: 34px; border-radius: 11px; background: #EEF4E9; font-size: 1.2rem; }
    @keyframes imageDrift { from { object-position: 50% 42%; } to { object-position: 50% 58%; } }
    @media (max-width: 700px) { .area-image-frame { height: 220px; } }
    .doctor-panel { background: #F7F9F5; border: 1px solid #E2EADD; border-radius: 20px; padding: 1.2rem; }
    @keyframes fadeUp { from {opacity: 0; transform: translateY(16px);} to {opacity: 1; transform: translateY(0);} }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- Header and navigation ----------------
logo = find_asset("Logo.jpg", "Logo.jpeg", "logo.png", "logo.webp")
logo_markup = ""
if logo:
    image_mime = "image/png" if logo.suffix.lower() == ".png" else "image/jpeg"
    logo_data = base64.b64encode(logo.read_bytes()).decode("ascii")
    logo_markup = f'<img class="brand-logo" src="data:{image_mime};base64,{logo_data}" alt="Essence Homoeopathic Clinic logo">'

st.markdown(
    f"""
    <div class="brand-banner">
      <div class="brand-inner">
        {logo_markup}
        <div class="brand-copy">
          <div class="brand-name">ESSENCE - THE HOMEOPATHY</div>
          <div class="brand-tagline">A welcoming space for your consultation</div>
        </div>
        <div class="brand-appointment">Appointments by request</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">Explore the clinic</div>', unsafe_allow_html=True)
nav = st.radio(
    "Navigate",
    [
        "Home",
        "About the Doctor",
        "Areas of Consultation",
        "Why Essence Homeopathy?",
        "Clinic Gallery",
        "Book Appointment",
        "AI Clinic Assistant",
        "Contact",
    ],
    horizontal=True,
    label_visibility="collapsed",
)
st.divider()


# ---------------- Home ----------------
if nav == "Home":
    left, right = st.columns([1.65, 1], gap="large", vertical_alignment="center")
    with left:
        st.markdown(
            """
            <div class="hero">
              <div class="eyebrow">Welcome to Essence Homeopathy</div>
              <div class="hero-title">Care that begins<br>with listening.</div>
              <div class="hero-copy">Meet <b>Dr. Faihed Waris Saifi</b> and connect with our clinic to enquire about consultation availability.</div>
              <br><span class="pill">☀️ Morning · 10 AM – 2 PM</span>
              &nbsp; <span class="pill">🌙 Evening · 5 PM – 9 PM</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown("### A warm welcome")
        st.write(
            "Explore the clinic, learn about the doctor, and send an appointment request. "
            "For diagnosis and treatment advice, please speak directly with the doctor."
        )
    with right:
        doctor_photo = find_asset("Dr.jpg", "dr.jpg", "Doctor.jpg", "doctor.jpg")
        if doctor_photo:
            st.image(str(doctor_photo), caption="Dr. Faihed Waris Saifi", use_container_width=True)
        else:
            st.markdown(
                '<div class="doctor-panel"><div class="section-kicker">Your doctor</div>'
                '<h2>Dr. Faihed Waris Saifi</h2><p>Essence Homeopathy</p>'
                '<p class="small-note">Add the doctor portrait as assets/Dr.jpg to display it here.</p></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown("## About Essence Homeopathy")
    st.subheader("A Clinic Built Around Listening, Understanding & Care")
    st.write(
        "Essence Homoeopathy is a homeopathic clinic founded by Dr. Faihed Waris Saifi in Geeta Colony, Delhi."
    )
    st.write(
        "We believe that a meaningful consultation begins with listening carefully to the patient. "
        "Our clinic aims to provide a comfortable environment where patients can discuss their health concerns, "
        "understand their consultation process and receive appropriate guidance."
    )
    st.write(
        "Our focus is on creating a professional and welcoming healthcare experience for every visitor."
    )
    st.markdown("*Essence Homoeopathy — The Art of Subtle Healing.*")

    st.write("")
    st.markdown('<div class="section-kicker">Patient Experiences</div>', unsafe_allow_html=True)
    st.subheader("What Patients Say About Essence Homoeopathy")
    st.write("We appreciate every patient who takes the time to share their experience with our clinic.")
    st.write("Read genuine patient feedback and reviews on Google.")
    st.link_button(
        "Read Our Google Reviews",
        "https://www.google.com/maps/place/Essence-The+Homeopathic+Clinic/@28.6530365,77.2731503,17z/",
    )

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="info-card"><h3>🩺 Personal consultation</h3>'
            '<p>Connect with the doctor to discuss your concerns during a consultation.</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="info-card"><h3>📅 Appointment requests</h3>'
            '<p>Share your preferred date and time. The clinic will confirm availability.</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="info-card"><h3>🌿 Visit the clinic</h3>'
            '<p>View clinic photographs and find directions before your visit.</p></div>',
            unsafe_allow_html=True,
        )
    st.write("")
    st.info("Clinic timings: Morning 10:00 AM–2:00 PM | Evening 5:00 PM–9:00 PM")


# ---------------- About the doctor ----------------
elif nav == "About the Doctor":
    st.markdown('<div class="section-kicker">Meet your doctor</div>', unsafe_allow_html=True)
    st.title("Dr. Faihed Waris Saifi")
    photo_col, detail_col = st.columns([1, 1.7], gap="large", vertical_alignment="center")
    doctor_photo = find_asset("Dr.jpg", "dr.jpg", "Doctor.jpg", "doctor.jpg")
    with photo_col:
        if doctor_photo:
            st.image(str(doctor_photo), caption="Dr. Faihed Waris Saifi", use_container_width=True)
        else:
            st.info("Doctor profile photo not found. Place the image at assets/Dr.jpg.")
    with detail_col:
        st.markdown("### BHMS | NHMC, University of Delhi")
        st.markdown("#### Welcome to Essence Homoeopathy")
        st.write(
            "Dr. Faihed Waris Saifi is a homeopathic physician and the founder of Essence Homoeopathy, "
            "located in Geeta Colony, Delhi."
        )
        st.write(
            "With a background in homeopathic medicine from Nehru Homoeopathic Medical College, University of Delhi, "
            "he welcomes patients seeking consultation for a wide range of health concerns."
        )
        st.write(
            "At Essence Homoeopathy, the consultation process begins with understanding the patient’s concerns, "
            "medical history, symptoms and overall health experience."
        )
        st.write(
            "The aim is to provide a professional, attentive and comfortable consultation experience while helping "
            "patients make informed decisions about their healthcare."
        )
        st.markdown(
            "**Dr. Faihed Waris Saifi**  \n"
            "Founder & Homeopathic Physician  \n"
            "Essence Homoeopathy, Delhi"
        )


# ---------------- Areas of consultation ----------------
elif nav == "Areas of Consultation":
    st.title("Areas of Consultation")
    st.write("Explore the health concerns patients may discuss during an individual consultation.")

    condition_details = {
        "Allergic rhinitis": (
            "It is an immune response to airborne allergens such as pollen, dust mites or pet dander.",
            "Note possible triggers and limit exposure when practical. Seek medical advice if symptoms affect sleep or daily life, or worsen asthma.",
            "NHS: Allergic rhinitis", "https://www.nhs.uk/conditions/allergic-rhinitis/",
        ),
        "Recurrent respiratory complaints": (
            "Repeated cough, wheeze or infections can have several causes, including infections, allergies or an underlying lung condition.",
            "Arrange medical assessment for repeated or persistent symptoms. Seek urgent care for severe breathing difficulty, chest pain or coughing blood.",
            "NHS: Respiratory tract infections", "https://www.nhs.uk/conditions/respiratory-tract-infection/",
        ),
        "Sinus-related concerns": (
            "Sinus lining swelling often follows a cold or flu; allergies may also contribute.",
            "Avoid smoke and note recurring triggers. Get medical advice if episodes recur, symptoms persist or worsen, or you feel very unwell.",
            "NHS: Sinusitis", "https://www.nhs.uk/conditions/sinusitis-sinus-infection/",
        ),
        "Acne": (
            "Hair follicles can become blocked by oil and dead skin cells; hormone changes may contribute.",
            "Use gentle skin care and avoid squeezing or scrubbing spots. Seek assessment for painful, scarring or persistent acne.",
            "NHS: Acne", "https://www.nhs.uk/conditions/acne/",
        ),
        "Eczema": (
            "Atopic eczema has no single known cause; family history and skin irritants or allergens can play a role.",
            "Avoid known irritants and follow a clinician’s skin-care advice. Get prompt care if skin suddenly worsens, looks infected, or fever occurs.",
            "NHS: Atopic eczema", "https://www.nhs.uk/conditions/atopic-eczema/",
        ),
        "Psoriasis": (
            "Skin cells build up faster than usual, likely involving the immune system; the exact cause is not known.",
            "Get a medical assessment for new or worsening patches. Seek review for recurring joint pain, stiffness or swelling, and follow prescribed care.",
            "NHS: Psoriasis", "https://www.nhs.uk/conditions/psoriasis/",
        ),
        "Acidity and digestive discomfort": (
            "Acid reflux occurs when stomach contents travel back towards the throat; some foods, smoking, pregnancy or medicines may contribute.",
            "Notice personal triggers and avoid lying down soon after meals. Seek care for frequent symptoms, trouble swallowing, repeated vomiting or unexplained weight loss.",
            "NHS: Heartburn and acid reflux", "https://www.nhs.uk/conditions/heartburn-and-acid-reflux/",
        ),
        "Constipation": (
            "Possible contributors include too little fibre or fluid, low activity, routine changes, some medicines or health conditions.",
            "If suitable for you, increase fibre gradually, drink fluids and stay active. Seek medical advice for persistent symptoms, blood in stool, weight loss or abdominal pain.",
            "NHS: Constipation", "https://www.nhs.uk/conditions/constipation/",
        ),
        "Recurrent digestive complaints": (
            "Recurring digestive symptoms have many possible causes, including food-related triggers, reflux, infection or other gut conditions.",
            "Keep a brief symptom, food and medication record. Arrange assessment for repeated symptoms; seek prompt care for severe pain, blood, persistent vomiting or unexplained weight loss.",
            "NHS: Digestive health", "https://www.nhs.uk/live-well/eat-well/digestive-health/",
        ),
        "Menstrual health concerns": (
            "Periods can vary with puberty, perimenopause, pregnancy, contraception, stress, weight changes or health conditions.",
            "Track cycle dates and bleeding. Ask a clinician about new changes, very heavy or prolonged bleeding, bleeding between periods, or bleeding after menopause.",
            "NHS: Irregular periods", "https://www.nhs.uk/symptoms/irregular-periods/",
        ),
        "PCOD-related concerns": (
            "The exact cause of PCOD (also called PCOS) is unknown; hormones, insulin regulation and family history may be involved.",
            "A clinician can assess symptoms and discuss appropriate follow-up. Seek care for irregular periods or related concerns rather than self-diagnosing.",
            "NHS Wales: PCOS", "https://111.wales.nhs.uk/polycysticovarysyndrome",
        ),
        "Uterine fibroids": (
            "Fibroids are non-cancerous growths from the muscle tissue of the uterus; their exact cause is unknown.",
            "Discuss heavy bleeding, pelvic pain or pressure with a clinician. Seek prompt care for very heavy bleeding or severe pain.",
            "NHS: Fibroids", "https://www.nhs.uk/conditions/fibroids/",
        ),
        "Recurrent health complaints": (
            "This is a broad description rather than one diagnosis, so possible causes vary from person to person.",
            "Keep a symptom timeline and list of medicines or tests. Arrange an assessment if symptoms recur, persist or worsen.",
            "", "",
        ),
        "Long-standing health concerns": (
            "Long-term symptoms may relate to a chronic condition, medicine effects or more than one underlying cause.",
            "Attend follow-up reviews and do not stop prescribed medicines without medical advice. Seek review for new or worsening symptoms.",
            "", "",
        ),
        "General homeopathic consultation": (
            "A consultation is not a diagnosis; the reason for symptoms needs individual medical assessment.",
            "Bring relevant reports and a current medication list. Continue appropriate medical care and seek urgent help for severe symptoms.",
            "", "",
        ),
    }
    consultation_areas = [
        ("Respiratory & Allergic Concerns", "consultation_respiratory.png", [("🌼", "Allergic rhinitis"), ("🫁", "Recurrent respiratory complaints"), ("👃", "Sinus-related concerns")]),
        ("Skin & Dermatological Concerns", "consultation_skin.png", [("✨", "Acne"), ("🧴", "Eczema"), ("🫧", "Psoriasis")]),
        ("Digestive Health", "consultation_digestive.png", [("🔥", "Acidity and digestive discomfort"), ("🥣", "Constipation"), ("🌿", "Recurrent digestive complaints")]),
        ("Women’s Health", "consultation_womens_health.png", [("🩺", "Menstrual health concerns"), ("🧬", "PCOD-related concerns"), ("🩻", "Uterine fibroids")]),
        ("General & Chronic Health Concerns", "consultation_general.png", [("🩺", "Recurrent health complaints"), ("📋", "Long-standing health concerns"), ("👩‍⚕️", "General homeopathic consultation")]),
    ]
    for row_start in range(0, len(consultation_areas), 2):
        cols = st.columns(2, gap="medium")
        for col_offset, (col, (heading, image_filename, concerns)) in enumerate(
            zip(cols, consultation_areas[row_start:row_start + 2])
        ):
            image_path = ASSET_DIR / image_filename
            image_data = base64.b64encode(image_path.read_bytes()).decode("ascii") if image_path.is_file() else ""
            image_markup = (
                f'<div class="area-image-frame"><img class="area-image" src="data:image/png;base64,{image_data}" '
                f'alt="Illustration for {html.escape(heading)}" loading="lazy"></div>'
                if image_data
                else '<div class="area-image-frame"></div>'
            )
            delay = (row_start + col_offset) * 0.1
            with col:
                st.markdown(
                    f'<div class="area-card" style="animation-delay:{delay:.2f}s">'
                    f'{image_markup}<h3>{html.escape(heading)}</h3>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                for icon, label in concerns:
                    occurrence, precautions, source_name, source_url = condition_details[label]
                    with st.expander(f"{icon} {label}"):
                        st.markdown(f"**How it may occur:** {occurrence}")
                        st.markdown(f"**Precautions:** {precautions}")
                        if source_url:
                            st.caption(f"General information: [{source_name}]({source_url})")

# ---------------- Why Essence Homeopathy ----------------
elif nav == "Why Essence Homeopathy?":
    st.title("Why Essence Homeopathy?")
    st.subheader("A Comfortable & Professional Consultation Experience")

    why_items = [
        ("Patient-Centred Consultation", "We take time to understand your health concerns and medical history."),
        ("Professional Environment", "A welcoming and comfortable clinic environment for consultation."),
        ("Clear Communication", "We encourage patients to discuss their concerns and ask questions."),
        ("Convenient Location", "Located in Geeta Colony, Delhi, near Taj Enclave."),
        ("Appointment-Based Consultation", "Contact the clinic to enquire about consultation availability and appointments."),
    ]
    for start_idx in range(0, len(why_items), 2):
        cols = st.columns(2, gap="medium")
        for col, (heading, description) in zip(cols, why_items[start_idx:start_idx + 2]):
            with col:
                st.markdown(
                    f'<div class="info-card"><h3>{heading}</h3><p>{description}</p></div>',
                    unsafe_allow_html=True,
                )


# ---------------- Clinic gallery ----------------
elif nav == "Clinic Gallery":
    st.title("Clinic Gallery")
    st.write("A little look inside Essence Homeopathy.")
    st.caption("The photo strip moves automatically. Hover over it to pause.")

    gallery_dir = ASSET_DIR / "clinic_gallery"
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

    cards = []
    for caption, filename in gallery_images:
        image_path = gallery_dir / filename
        if image_path.is_file():
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            safe_caption = html.escape(caption)
            cards.append(
                f'<div class="gallery-card"><img src="data:image/webp;base64,{encoded}" alt="{safe_caption}">'
                f'<div class="gallery-caption">{safe_caption}</div></div>'
            )

    if cards:
        card_html = "".join(cards)
        components.html(
            f"""
            <style>
              * {{ box-sizing: border-box; }}
              .gallery-window {{ width: 100%; overflow: hidden; padding: 10px 0 18px; }}
              .gallery-track {{ display: flex; width: max-content; gap: 18px; animation: galleryScroll 48s linear infinite; }}
              .gallery-window:hover .gallery-track {{ animation-play-state: paused; }}
              .gallery-card {{ width: 290px; flex: 0 0 290px; background: #F7F9F5; border: 1px solid #E2EADD; border-radius: 17px; overflow: hidden; box-shadow: 0 7px 20px rgba(18,61,50,.08); }}
              .gallery-card img {{ display: block; width: 100%; height: 205px; object-fit: cover; }}
              .gallery-caption {{ padding: 11px 13px; color: #294337; font: 600 14px Arial,sans-serif; }}
              @keyframes galleryScroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(calc(-50% - 9px)); }} }}
              @media (prefers-reduced-motion: reduce) {{ .gallery-track {{ animation: none; }} }}
            </style>
            <div class="gallery-window"><div class="gallery-track">{card_html}{card_html}</div></div>
            """,
            height=270,
            scrolling=False,
        )
    else:
        st.warning("No gallery photos were found in assets/clinic_gallery.")

    st.subheader("Explore the clinic")
    for start_idx in range(0, len(gallery_images), 3):
        cols = st.columns(3, gap="medium")
        for col, (caption, filename) in zip(cols, gallery_images[start_idx:start_idx + 3]):
            image_path = gallery_dir / filename
            if image_path.is_file():
                with col:
                    st.image(str(image_path), caption=caption, use_container_width=True)
    st.caption("All photographs displayed here were supplied by the clinic.")


# ---------------- Appointment request: WhatsApp, no database ----------------
elif nav == "Book Appointment":
    st.markdown('<div class="section-kicker">YOUR CONSULTATION EXPERIENCE</div>', unsafe_allow_html=True)
    st.subheader("A Thoughtful Approach to Consultation")
    st.write("At Essence Homoeopathy, consultation involves:")
    st.markdown(
        "- Understanding your primary health concerns.\n"
        "- Reviewing relevant symptoms and medical history.\n"
        "- Discussing previous treatments and available medical reports.\n"
        "- Understanding your healthcare needs.\n"
        "- Providing appropriate guidance and discussing treatment options."
    )
    st.write(
        "Patients are encouraged to bring relevant prescriptions, investigation reports and details of ongoing medications."
    )

    st.markdown("### Book Your Consultation")
    st.write(
        "Share your preferred appointment details. This request opens WhatsApp "
        "so you can send it directly to the clinic. The clinic must confirm the slot."
    )

    session = st.selectbox(
        "Preferred session",
        ["Morning (10 AM – 2 PM)", "Evening (5 PM – 9 PM)"],
        key="appointment_session",
    )

    with st.form("appointment_form", clear_on_submit=False):
        name = st.text_input("Full name *")
        phone = st.text_input(
            "Your phone number *",
            max_chars=20,
            help="Enter a number the clinic can use to contact you.",
        )
        appt_date = st.date_input("Preferred date", min_value=date.today())
        if session.startswith("Morning"):
            time_options = ["10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM"]
        else:
            time_options = ["5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"]
        preferred_time = st.selectbox("Preferred time within the selected session", time_options)
        consent = st.checkbox("I agree that the clinic may contact me about this appointment request. *")
        submitted = st.form_submit_button("Continue to WhatsApp")

    if submitted:
        if not name.strip() or not phone.strip() or not consent:
            st.error("Please complete your name, phone number, and contact consent.")
        else:
            message = (
                "Hello Essence Homeopathy, I would like to request an appointment.\n"
                f"Name: {name.strip()}\n"
                f"Phone: {phone.strip()}\n"
                f"Preferred date: {appt_date.isoformat()}\n"
                f"Session: {session}\n"
                f"Preferred time: {preferred_time}\n"
                "Please confirm availability."
            )
            whatsapp_url = f"https://wa.me/{CLINIC_WHATSAPP}?text={quote(message)}"
            st.success("Your appointment details are ready. Send the WhatsApp message to complete your request.")
            st.link_button("Open WhatsApp and send request", whatsapp_url, use_container_width=True)

    st.caption(
        "Please do not include diagnosis or detailed medical history. "
        "This form does not save or submit information until you send the WhatsApp message."
    )
    st.caption("Do not use this form for emergencies. For urgent symptoms, contact local emergency services or go to the nearest emergency department.")


# ---------------- AI clinic assistant ----------------
elif nav == "AI Clinic Assistant":
    st.title("AI Clinic Assistant")
    st.write("Ask about clinic timings, the doctor, or how to request an appointment.")
    st.caption(
        "This assistant provides administrative information only. "
        "It does not diagnose, prescribe, or replace a consultation."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I’m the Essence Homeopathy clinic assistant. "
                           "I can help with clinic timings and appointment requests. How may I help?",
            }
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type your question...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        if clinic_assistant_reply:
            try:
                answer = clinic_assistant_reply(prompt)
            except Exception:
                answer = (
                    "I can help with clinic timings (10 AM–2 PM and 5 PM–9 PM) "
                    "and appointment requests. Please contact the clinic directly "
                    "for medical advice."
                )
        else:
            answer = (
                "The AI assistant is not configured right now. Clinic timings are "
                "10 AM–2 PM and 5 PM–9 PM. Please contact the clinic directly "
                "for appointment availability or medical advice."
            )
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()


# ---------------- Contact ----------------
elif nav == "Contact":
    st.title("Contact Essence Homeopathy")
    st.subheader("Dr. Faihed Waris Saifi")
    st.write("**Clinic timings**")
    st.write("☀️ Morning: 10:00 AM – 2:00 PM")
    st.write("🌙 Evening: 5:00 PM – 9:00 PM")
    st.markdown("**Phone / WhatsApp:** +91 93153 31235")
    st.markdown("[Call the clinic](tel:+919315331235) · [WhatsApp the clinic](https://wa.me/919315331235)")

    qr_path = find_asset("qr_Code.jpg", "QR_Code.jpg", "qr_code.jpg", "QR_Code.png", "qr_code.png")
    qr_col, map_col = st.columns([1, 1.6], gap="large", vertical_alignment="center")
    with qr_col:
        if qr_path:
            st.image(str(qr_path), caption="Scan to open the clinic location", width=230)
        else:
            st.info("Map QR image not found. Add qr_Code.jpg or QR_Code.png inside the assets folder.")
    with map_col:
        st.markdown("### Find the clinic")
        st.write("Scan the QR code or open the clinic location in Google Maps.")
        st.link_button(
            "Open Google Maps",
            "https://www.google.com/maps/place/Essence-The+Homeopathic+Clinic/@28.6530365,77.2731503,17z/",
        )


# ---------------- Footer ----------------
st.markdown(
    """
    <div class="footer">
      <b>Essence Homeopathy</b> · Dr. Faihed Waris Saifi<br>
      This website provides clinic and appointment information, not medical diagnosis or treatment.
      In an emergency, seek urgent medical care.
    </div>
    """,
    unsafe_allow_html=True,
)
