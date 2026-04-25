import os
import anthropic
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GMAIL_ADDRESS = "danielrauscher011@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

PROMPT = """You are an advanced financial and macroeconomic analyst. Generate a DAILY POST-MARKET FINANCIAL BRIEFING that is accurate, data-driven, concise but high-density, focused only on relevant high-impact information.

Structure your response exactly as follows:

1. EXECUTIVE SUMMARY (MAX 5 BULLETS)
2. MARKET RECAP - Major indices (S&P 500, Nasdaq, Dow, Russell 2000) with % changes, Global markets (Europe, Asia), Bonds (10Y yield), Commodities (oil, gold), Crypto (BTC, ETH)
3. KEY NEWS & DEVELOPMENTS - A. Corporate B. Macroeconomic C. Financial system
4. GEOPOLITICAL & POLICY ANALYSIS
5. THEMES & NARRATIVES (2-5 dominant narratives)
6. FORWARD LOOK (NEXT 1-5 DAYS)
7. INVESTMENT OPPORTUNITIES (HIGH CONVICTION ONLY, 2-4 ideas)
8. RISKS & RED FLAGS

Be direct. No fluff. High information density. Analytical not narrative-heavy."""

print("Calling Claude API...")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=120.0)
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=4096,
    messages=[{"role": "user", "content": PROMPT}]
)
briefing = message.content[0].text
print("Briefing generated successfully")

today = datetime.now().strftime("%B %d, %Y")
msg = MIMEMultipart()
msg["Subject"] = f"Daily Financial Briefing - {today}"
msg["From"] = GMAIL_ADDRESS
msg["To"] = GMAIL_ADDRESS
msg.attach(MIMEText(briefing, "plain"))

print("Sending email...")
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    s.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())

print("Email sent successfully")
