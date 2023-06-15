import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
from collections.abc import Mapping

APP_PASS = input("Enter your app password: ")
SENDER = input("Enter your email: ")
RECEIVER = ("Enter the Receiver email: ")
BUY_PRICE = 200
SMPT_ADDRESS = input("Enter the SMTP Address")
# The URL of the product you want to track
url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
# Add your browser headers
header = {
    "User-Agent": "User Agent header",
    "Accept-Language": "Language header"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

title = soup.find(id="productTitle").get_text().strip()
price = soup.find(class_="a-offscreen").get_text()
# print(price)
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
# print(f"Title: {title}:\nPrice: {price_as_float}")

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(SMPT_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(SENDER, APP_PASS)
        connection.sendmail(
            from_addr=SENDER,
            to_addrs=RECEIVER,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )
