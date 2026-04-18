import anthropic
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

ANTHROPIC_API_KEY = "REPLACE_API_KEY"
GMAIL_ADDRESS = "danielrauscher011@gmail.com"
GMAIL_APP_PASSWORD = "REPLACE_APP_PASSWORD"

PROMPT = """You are an advanced financial and macroeconomic analyst. Generate a DAILY POST-MARKET FINANCIAL BRIEFING. Structure: 1) Executive Summary 2) Market Recap with % changes for S&P500/Nasdaq/Dow/Russell/Europe/Asia/Bonds/Oil/Gold/Crypto 3) Key News - Corporate/Macro/Financial System 4) Geopolitical & Policy Analysis 5) Themes & Narratives 6) Forward Look 7) Investment Opportunities 8) Risks & Red Flags. Be direct, data-driven, high density, no fluff."""

def generate_briefing():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(model="claude-opus-4-5", max_tokens=4096, messages=[{"role": "user", "content": PROMPT}])
    return message.content[0].text

def send_email(text):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    today = datetime.now().strftime("%B %d, %Y")
    msg = MIMEMultipart()
    msg["Subject"] = f"Daily Financial Briefing - {today}"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg.attach(MIMEText(text, "plain"))
    import smtplib
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        s.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())
    print("Email sent")

def run():
    print(f"Generating briefing...")
    try:
        send_email(generate_briefing())
    except Exception as e:
        print(f"Error: {e}")

schedule.every().day.at("17:00").do(run)
print("Scheduler running - waiting for 17:00 CET")
while True:
    schedule.run_pending()
    time.sleep(60)
