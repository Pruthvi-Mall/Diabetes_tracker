import streamlit as st
import joblib, os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent_src.health_ai_engine import lifestyle_advice, diet_plan, emergency_alert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "artifacts", "diabetes_model.pkl"))

st.title("🛡 AI Community Health Guardian by Pruthvi Mall")

labels = ["Pregnancies","Glucose","BloodPressure","SkinThickness",
          "Insulin","BMI","DiabetesPedigreeFunction","Age"]
data = [st.number_input(l,0.0) for l in labels]

if st.button("Analyze Health"):
    risk = model.predict([data])[0]

    st.subheader("ML Risk Result")
    st.write("Diabetes Risk:", "YES" if risk==1 else "NO")

    st.subheader("AI Lifestyle Advice")
    for tip in lifestyle_advice(risk, data[5], data[1], data[7]):
        st.write("•", tip)

    st.subheader("AI Diet Plan")
    for d in diet_plan(risk):
        st.write("•", d)

    st.subheader("Emergency Alert")
    st.write(emergency_alert(data[1]))

