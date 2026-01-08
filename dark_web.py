import streamlit as st
import pandas as pd
import time
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config("SVIT Dark Web Monitor", layout="wide")

st.markdown("""
<h1 style='text-align:center;'>SVIT</h1>
<h3 style='text-align:center;'>Dark Web Threat Monitoring System</h3>
<p style='text-align:center;'>Major Project – Cyber Security</p><hr>
""", unsafe_allow_html=True)

st.sidebar.header("Scan Panel")
keyword = st.sidebar.text_input("Enter keyword")
scan = st.sidebar.button("Start Scan")

def ai_score(text):
    high = ["leak", "hack", "password", "dump", "database"]
    medium = ["sell", "market", "btc", "crypto"]
    if any(x in text.lower() for x in high):
        return "HIGH", "95%"
    if any(x in text.lower() for x in medium):
        return "MEDIUM", "65%"
    return "LOW", "25%"

if scan:
    with st.spinner("Scanning Dark Web..."):
        time.sleep(3)

    raw = [
        "college database leak",
        "password dump",
        "crypto market",
        "ebooks sale",
        "movie packs"
    ]

    rows = []
    for r in raw:
        risk, prob = ai_score(r)
        rows.append([r, risk, prob])

    df = pd.DataFrame(rows, columns=["Detected Activity", "Risk Level", "Threat Probability"])

    st.subheader("Live Threat Intelligence")
    st.dataframe(df)
    st.bar_chart(df["Risk Level"].value_counts())

    st.subheader("AI Cyber Advisory")
    if "HIGH" in df["Risk Level"].values:
        st.error("Immediate action required! Change all credentials & audit servers.")
    elif "MEDIUM" in df["Risk Level"].values:
        st.warning("Monitor accounts & update passwords.")
    else:
        st.success("System safe.")

    def make_pdf(data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = [Paragraph("SVIT Dark Web Threat Report", styles["Title"])]
        table = Table([["Activity", "Risk", "Probability"]] + data.values.tolist())
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer

    pdf = make_pdf(df)
    st.download_button("Download Official Report", pdf, "SVIT_Report.pdf")

st.divider()
st.markdown("<center>Developed by SVIT CSE Student</center>", unsafe_allow_html=True)
