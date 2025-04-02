from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import smtplib
from email.mime.text import MIMEText

# Product URLs
AMAZON_URL = "https://amzn.in/d/4QJoVqt"
FLIPKART_URL = "https://www.flipkart.com/realme-buds-t310-12-4mm-driver-46db-anc-spatial-audio-upto-40-hours-playback-bluetooth/p/itmfac7ac8f4e369?pid=ACCH2PGXGP4BV2JF&lid=LSTACCH2PGXGP4BV2JFSSXYBA&marketplace=FLIPKART&q=realme+Buds+T310+True+Wireless+in-Ear+Earbuds+with+46dB+Hybrid+ANC%2C+360%C2%B0+Spatial+Audio%2C+12.4mm+Dynamic+Bass+Driver%2C+Upto+40Hrs+Battery+and+Fast+Charging+%28Vibrant+Black%29&store=0pm%2Ffcn%2F821%2Fa7x&spotlightTagId=BestsellerId_0pm%2Ffcn%2F821%2Fa7x&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=98a0cd8a-b412-4c39-9a81-6eddd90e5f65.ACCH2PGXGP4BV2JF.SEARCH&ppt=sp&ppn=sp&ssid=9mp7j2f7wg0000001742491103502&qH=2f067443b249b986"

# Email credentials (Use App Password if 2FA is enabled)
EMAIL_SENDER = "chittiboyinasriharipranav@gmail.com"
EMAIL_PASSWORD = "ocho aaky apxy ifwk"
EMAIL_RECEIVER = "pch43451@gmail.com"

# Target price for alert
TARGET_PRICE = 2000 # Set your target price here

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

def get_price(url, site_name, selector):
    """ Fetches the product price from Amazon or Flipkart """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(url)
    time.sleep(3)

    try:
        price_text = driver.find_element(By.CSS_SELECTOR, selector).text
        price = float(price_text.replace("₹", "").replace(",", "").strip())
        driver.quit()
        return price
    except Exception as e:
        driver.quit()
        print(f"Error fetching {site_name} price:", e)
        return None

def main():
    # Send a Confirmation Email when the script starts
    send_email_alert("Price Alert Assigned ✅", 
                     f"Your price alert for ₹{TARGET_PRICE} is set successfully!\n"
                     f"You'll be notified when the price drops below your target.")
    
    amazon_price = get_price(AMAZON_URL, "Amazon", ".a-price-whole")
    flipkart_price = get_price(FLIPKART_URL, "Flipkart", "._30jeq3")

    if amazon_price and flipkart_price:
        if amazon_price < flipkart_price:
            message = f"Amazon has the cheaper price: ₹{amazon_price}\nLink: {AMAZON_URL}"
        else:
            message = f"Flipkart has the cheaper price: ₹{flipkart_price}\nLink: {FLIPKART_URL}"
        
        send_email_alert("Price Alert: Cheaper Option Available!", message)

    # Price Drop Alert System
    if amazon_price and amazon_price <= TARGET_PRICE:
        send_email_alert("🔥 Amazon Price Drop Alert!", 
                         f"Good news! Your tracked item is now ₹{amazon_price} (Below ₹{TARGET_PRICE}).\n{AMAZON_URL}")
    
    if flipkart_price and flipkart_price <= TARGET_PRICE:
        send_email_alert("🔥 Flipkart Price Drop Alert!", 
                         f"Good news! Your tracked item is now ₹{flipkart_price} (Below ₹{TARGET_PRICE}).\n{FLIPKART_URL}")

if __name__ == "__main__":
    main()