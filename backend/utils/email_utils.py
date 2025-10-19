import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import Config

# Configure your SMTP server details here
SMTP_SERVER = Config.SMTP_SERVER
SMTP_PORT = Config.SMTP_PORT
SMTP_USERNAME = Config.SMTP_USERNAME
SMTP_PASSWORD = Config.SMTP_PASSWORD
FROM_EMAIL = Config.FROM_EMAIL

def send_email(to_email, subject, body):
    if not SMTP_USERNAME or not SMTP_PASSWORD or not FROM_EMAIL:
        logging.error("SMTP credentials not configured. Cannot send email.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        logging.info(f"Email sent to {to_email} with subject '{subject}'")
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")
