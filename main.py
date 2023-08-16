# hotel price bot for deploy in Replit, use the command "poetry add selenium@4.10.x" in the shell
# from Keep_Alive import keep_alive
import Keep_Alive
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email(subject, body):
  sender_email = "hotelbot12@outlook.com"
  my_secret = os.environ['pass']
  sender_password = my_secret
  receiver_email = "yuvalamar15@gmail.com"

  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject

  message.attach(MIMEText(body, "plain"))

  try:
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("Email sent successfully!")
  except Exception as e:
    print("Error sending email:", str(e))


def check_price():
  URL = "https://www.fattal.co.il/BE_Rooms.aspx?Lang=heb&In=2023-08-31&Out=2023-09-03&Hotel=10039_1&Region=2&PromoCode=%d7%94%d7%96%d7%9f+%d7%a7%d7%95%d7%93&Rooms=1&Ad1=2&Ch1=0&Inf1=0&ud=bfd84054c5"

  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  wd = webdriver.Chrome(options=chrome_options)
  wd.maximize_window()
  wd.implicitly_wait(10)
  wd.get(URL)
  time.sleep(4)

  fullpinsion = wd.find_element(
    By.XPATH,
    '//*[@id="rooms-with-results"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]/span[3]/span[1]'
  )

  # Scroll the element into view
  wd.execute_script("arguments[0].scrollIntoView(true);", fullpinsion)

  fullpinsion.click()

  shamaimprice = wd.find_element(
    By.XPATH,
    '//*[@id="rooms-with-results"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/table/tbody/tr/td[5]/div[2]'
  )
  new_price = shamaimprice.text

  wd.quit()
  return new_price

# keep_alive()
Keep_Alive.keep_alive()
current_price = check_price()
print("hoo : ", current_price)
while True:
  time.sleep(50)  # 20 minutes (20 minutes x 60 seconds)
  new_price = check_price()
  print("ccc : ", current_price)
  print("new : ", new_price)
  if new_price != current_price:
    subject = "Price Change Alert"
    body = f"The price has changed! New price: {new_price}"
    send_email(subject, body)
    current_price = new_price
