from flask import Flask, jsonify
from threading import Thread
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

# Product URLs
AMAZON_URL = "https://amzn.in/d/9ECNlSK"
FLIPKART_URL = "https://www.flipkart.com/puma-softride-seave-slip-men-casual/p/itm996da8d863f57?pid=SNDGPYF4WABAUCFA"

# Email credentials (Use App Password if 2FA is enabled)
EMAIL_SENDER = "chittiboyinasriharipranav@gmail.com"
EMAIL_PASSWORD = "ocho aaky apxy ifwk"
EMAIL_RECEIVER = "pch43451@gmail.com"

# Target price for alert
TARGET_PRICE = 3000 # Set your target price here

def send_email_alert(subject, message):
    """ Sends an email notification """
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"Email Sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_price(url, site_name, selector, retries=3):
    """ Fetches the product price from Amazon or Flipkart """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    for attempt in range(retries):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            time.sleep(3 + attempt)  # Wait longer on retries
            price_text = driver.find_element(By.CSS_SELECTOR, selector).text
            driver.quit()
            return float(price_text.replace("₹", "").replace(",", "").strip())
        except Exception as e:
            print(f"Retry {attempt + 1}/{retries} for {site_name} - Error: {e}")
            driver.quit()
    return None

def price_checker():
    """ Continuously checks the price every 1 hour """

    # Send a confirmation email when the script starts
    send_email_alert("✅ Price Alert Service Started!", 
                     "Your price alert service is running successfully. "
                     "You'll be notified when the price drops below your target.")

    while True:
        print("Checking prices...")
        amazon_price = get_price(AMAZON_URL, "Amazon", ".a-price-whole")
        flipkart_price = get_price(FLIPKART_URL, "Flipkart", "._30jeq3")

        if amazon_price and amazon_price <= TARGET_PRICE:
            send_email_alert("🔥 Amazon Price Drop Alert!", 
                             f"Good news! Your tracked item is now ₹{amazon_price} (Below ₹{TARGET_PRICE}).\n{AMAZON_URL}")
        
        if flipkart_price and flipkart_price <= TARGET_PRICE:
            send_email_alert("🔥 Flipkart Price Drop Alert!", 
                             f"Good news! Your tracked item is now ₹{flipkart_price} (Below ₹{TARGET_PRICE}).\n{FLIPKART_URL}")

        print("Sleeping for 1 hour...")
        time.sleep(3600)  # Sleep for 1 hour

@app.route("/")
def home():
    return jsonify({"status": "Price Alert Service is running!"})

if __name__ == "__main__":
    # Start the price checker in a separate thread
    Thread(target=price_checker, daemon=True).start()
    app.run(host="0.0.0.0",port=10000)