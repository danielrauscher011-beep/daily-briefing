import os
import anthropic
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GMAIL_ADDRESS = "danielrauscher011@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

today = datetime.now().strftime("%B %d, %Y")

PROMPT = f"""Today is {today}. You are an advanced financial and macroeconomic analyst. 

Use your web search tool to get TODAY'S real-time market data before writing anything. Search for:
- Today's S&P 500, Nasdaq, Dow Jones, Russell 2000 closing prices and % changes
- Today's top financial news and market moving events
- Current BTC and ETH prices
- Current 10Y treasury yield
- Current oil and gold prices

Then generate a DAILY POST-MARKET FINANCIAL BRIEFING using only data from today {today}.

Structure your response exactly as follows:

1. EXECUTIVE SUMMARY (MAX 5 BULLETS)
- Key market-moving developments
- Overall market sentiment (risk-on / risk-off / mixed)
- Biggest drivers of the day

2. MARKET RECAP
- Major indices (S&P 500, Nasdaq, Dow, Russell 2000) with % changes
- Global markets (Europe, Asia) with % changes
- Bonds (10Y yield)
- Commodities (oil, gold)
- Crypto (BTC, ETH)

3. KEY NEWS & DEVELOPMENTS
A. Corporate (earnings, major announcements)
B. Macroeconomic (inflation, employment, GDP, central bank)
C. Financial system (banks, liquidity, credit)

4. GEOPOLITICAL & POLICY ANALYSIS
- Major geopolitical events affecting markets
- Central bank actions or signals
- Trade, conflict, or regulatory developments
- Explain HOW and WHY these affect markets

5. THEMES & NARRATIVES (2-5 dominant narratives)
- Why the narrative matters
- What markets are pricing in

6. FORWARD LOOK (NEXT 1-5 DAYS)
- Upcoming economic data releases
- Earnings to watch
- Potential volatility triggers

7. INVESTMENT OPPORTUNITIES (HIGH CONVICTION ONLY, 2-4 ideas)
For each: Asset, Thesis, Supporting evidence, Risk factors, Time horizon

8. RISKS & RED FLAGS
- Key downside risks
- Market fragilities
- Overextended sectors

Be direct. No fluff. High information density. Analytical not narrative-heavy."""

print("Calling Claude API with web search...")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, timeout=300.0)
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=4096,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": PROMPT}]
)

briefing = ""
for block in message.content:
    if hasattr(block, "text"):
        briefing += block.text

print("Briefing generated successfully")

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
