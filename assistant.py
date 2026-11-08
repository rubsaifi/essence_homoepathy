import os

SYSTEM_GUARDRAIL = (
    "You are an administrative assistant for Essence Homeopathy. "
    "You may answer only clinic-related administrative questions using the verified "
    "facts in this prompt. Do not diagnose, triage beyond basic emergency direction, "
    "recommend or name medicines, interpret symptoms, promise cures, or provide treatment "
    "plans. If asked a medical question, explain that the doctor must assess it in a "
    "consultation. For severe or urgent symptoms, advise seeking urgent medical care."
)

def clinic_assistant_reply(question: str) -> str:
    """Uses OpenAI if OPENAI_API_KEY is configured; otherwise safe local FAQ fallback."""
    q = question.lower().strip()

    # Emergency guardrail is handled before any optional model call.
    emergency_terms = ["chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
                       "unconscious", "severe bleeding", "stroke", "suicidal"]
    if any(term in q for term in emergency_terms):
        return ("This chat is not an emergency service. Please contact local emergency services "
                "or go to the nearest emergency department immediately.")

    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    try:
        import streamlit as st
        api_key = api_key or st.secrets.get("OPENAI_API_KEY", "")
        model_name = st.secrets.get("OPENAI_MODEL", model_name)
    except Exception:
        pass
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_GUARDRAIL + "\nVerified clinic facts: "
                     "Name: Essence Homeopathy. Doctor: Dr Faihad Waris Saifi. "
                     "Morning timings: 10 AM to 2 PM. Evening timings: 5 PM to 9 PM. "
                     "Appointment requests can be submitted through the website. "
                     "Address and phone number have not been provided."},
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
                max_tokens=220,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    if any(w in q for w in ["timing", "time", "open", "opening", "close", "hours"]):
        return ("Essence Homeopathy is open in two sessions: morning 10:00 AM–2:00 PM "
                "and evening 5:00 PM–9:00 PM.")
    if any(w in q for w in ["appointment", "book", "booking", "slot", "visit"]):
        return ("You can use the **Book Appointment** section on this website to send a request. "
                "The clinic will contact you to confirm the appointment; submitting a request "
                "does not guarantee a slot.")
    if any(w in q for w in ["doctor", "name", "who"]):
        return "The doctor at Essence Homeopathy is Dr Faihad Waris Saifi."
    if any(w in q for w in ["address", "location", "where", "map", "phone", "contact", "whatsapp"]):
        return ("The clinic address and phone number have not yet been added to this website. "
                "Please ask the clinic directly for verified contact details.")
    medical_terms = ["medicine", "medication", "dose", "dosage", "cure", "treatment",
                     "symptom", "pain", "fever", "disease", "diagnose", "prescribe",
                     "pregnant", "child", "infection", "diabetes", "blood pressure"]
    if any(w in q for w in medical_terms):
        return ("I can help with clinic information, but I can't assess symptoms, diagnose, "
                "recommend medicines, or advise on treatment. Please consult Dr Faihad Waris Saifi "
                "or another qualified healthcare professional. For urgent or severe symptoms, "
                "seek urgent medical care.")
    return ("I can help with clinic timings, the doctor's name, contact information, and "
            "appointment requests. What would you like to know?")
