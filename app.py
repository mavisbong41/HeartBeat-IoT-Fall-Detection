import streamlit as st
import speech_recognition as sr
import pyttsx3
import base64
import os
import time
import threading

def speak_async(text):
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except: pass
    threading.Thread(target=run, daemon=True).start()

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def listen_and_get_text_quick():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.1)
            audio = r.listen(source, timeout=1, phrase_time_limit=1.5)
            return r.recognize_google(audio).lower()
        except: return None
st.set_page_config(page_title="HeartBeat AI", page_icon="❤️", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; max-width: 500px !important; margin: auto; }
    .monitor-card img { max-height: 300px; width: auto; border-radius: 20px; display: block; margin: 0 auto 20px auto; }
    .emergency-box { border: 2px solid #ff4b4b; background-color: #fffbfa; border-radius: 15px; padding: 25px; text-align: center; }
    .protocol-box { background: #fffbe6; padding: 25px; border-radius: 15px; border: 1px solid #ffe58f; text-align: center; margin-top: 10px; }
    
    .voice-visualizer {
        display: flex; justify-content: space-around; align-items: center; 
        height: 60px; width: 100%; margin: 20px 0;
    }
    .visual-bar {
        width: 8px; background: #ff4b4b; border-radius: 10px;
        animation: expand 0.8s infinite alternate ease-in-out;
    }
    @keyframes expand { 0% { height: 10px; opacity: 0.3; } 100% { height: 60px; opacity: 1; } }
    .visual-bar:nth-child(1) { animation-delay: 0.0s; }
    .visual-bar:nth-child(2) { animation-delay: 0.2s; }
    .visual-bar:nth-child(3) { animation-delay: 0.4s; }
    .visual-bar:nth-child(4) { animation-delay: 0.1s; }
    .visual-bar:nth-child(5) { animation-delay: 0.3s; }
    .visual-bar:nth-child(6) { animation-delay: 0.5s; }
    .visual-bar:nth-child(7) { animation-delay: 0.2s; }

    .detected-label { background: #f0f0f0; border-radius: 20px; padding: 4px 15px; font-size: 0.8rem; color: #ff4b4b; font-weight: bold; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if 'status' not in st.session_state: st.session_state.status = "SAFE"
if 'start_t' not in st.session_state: st.session_state.start_t = None
if 'rescue_start_t' not in st.session_state: st.session_state.rescue_start_t = None
if 'has_spoken_rescue' not in st.session_state: st.session_state.has_spoken_rescue = False
if 'has_spoken_ambulance' not in st.session_state: st.session_state.has_spoken_ambulance = False
if 'last_word' not in st.session_state: st.session_state.last_word = "Listening..."


st.markdown("<h1 style='text-align: center;'>❤️ HeartBeat AI</h1>", unsafe_allow_html=True)

placeholder = st.empty()

with placeholder.container():
    # --- A. SAFE ---
    if st.session_state.status == "SAFE":
        img_b64 = get_image_base64("skeleton.png")
        if img_b64:
            st.markdown(f'<div class="monitor-card"><img src="data:image/png;base64,{img_b64}"></div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #2ecc71; font-weight: bold;'>🟢 Monitoring Status: SECURE</p>", unsafe_allow_html=True)
        if st.button("🚨 Simulate Fall Incident"):
            st.session_state.status = "FALLEN"
            st.session_state.start_t = time.time()
            st.session_state.has_spoken_rescue = False
            st.session_state.has_spoken_ambulance = False
            st.session_state.last_word = "Listening..."
            st.rerun()

    # --- B. FALLEN ---
    elif st.session_state.status == "FALLEN":
        rem = max(0, 60 - int(time.time() - st.session_state.start_t))

        st.markdown(f"""<div class="emergency-box">
                    <h2 style="color: #ff4b4b; margin: 0;">⚠️ CRITICAL FALL</h2>
                    <h1 style="font-size: 4rem; color: #ff4b4b; margin: 0;">{rem}s</h1>
                    <div class="voice-visualizer">
                        <div class="visual-bar"></div><div class="visual-bar"></div><div class="visual-bar"></div>
                        <div class="visual-bar"></div><div class="visual-bar"></div><div class="visual-bar"></div>
                        <div class="visual-bar"></div><div class="visual-bar"></div><div class="visual-bar"></div>
                    </div>
                    <span class="detected-label">AI Detected: "{st.session_state.last_word}"</span>
                    </div>""", unsafe_allow_html=True)

        if rem == 60 and not st.session_state.has_spoken_rescue:
            speak_async("Fall detected. Are you okay? Say 'OK' to confirm safety or 'Help' to request assistance.")
            st.session_state.has_spoken_rescue = True

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ I'M SAFE"):
                speak_async("I am glad you are safe.")
                st.session_state.status = "SAFE"
                st.rerun()
        with c2:
            if st.button("🚑 REQUEST HELP"): 
                st.session_state.status = "RESCUE"; st.session_state.rescue_start_t = time.time()
                st.session_state.has_spoken_rescue = False; st.rerun()

        voice_in = listen_and_get_text_quick()
        if voice_in:
            st.session_state.last_word = voice_in
            if "ok" in voice_in: 
                speak_async("I am glad you are safe.")
                st.session_state.status = "SAFE"
                st.rerun()
            if "help" in voice_in: 
                st.session_state.status = "RESCUE"; st.session_state.rescue_start_t = time.time()
                st.session_state.has_spoken_rescue = False; st.rerun()

        if rem <= 0:
            st.session_state.status = "RESCUE"; st.session_state.rescue_start_t = time.time(); st.rerun()

        time.sleep(0.1)
        st.rerun()

    # --- C. RESCUE ---
    elif st.session_state.status == "RESCUE":
        res_rem = max(0, 60 - int(time.time() - st.session_state.rescue_start_t))
        st.error("🚨 EMERGENCY ALERT DISPATCHED")
        
        st.markdown(f"""
            <div class="protocol-box">
                <p style="margin: 0; font-size: 1.1em;"><b>Protocol:</b> Caregivers (Son) notified via SMS.</p>
                <hr style="border: 0.5px solid #ffe58f;">
                <p style="margin: 5px 0; color: #ff4b4b; font-size: 1.6em; font-weight: bold;">
                    🚑 Ambulance auto-call in: {res_rem}s
                </p>
                <p style="font-size: 1rem; color: #d35400; font-weight: bold;">
                    {"SOS TRIGGERED: DISPATCHING NOW" if res_rem <= 0 else "If not viewed within 1 minute, SOS will trigger."}
                </p>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.has_spoken_rescue:
            speak_async("Caregivers notified. If not viewed within 1 minute, SOS will trigger.")
            st.session_state.has_spoken_rescue = True

        if res_rem <= 0 and not st.session_state.has_spoken_ambulance:
            speak_async("Time expired. Ambulance called.")
            st.session_state.has_spoken_ambulance = True

        if st.button("🔄 Reset Demo Session"):
            st.session_state.status = "SAFE"
            st.rerun()
        
        time.sleep(1)
        st.rerun()