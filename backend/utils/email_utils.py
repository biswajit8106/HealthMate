import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure your SMTP server details here
SMTP_SERVER = 'smtp.mailersend.net'
SMTP_PORT = 587
SMTP_USERNAME = 'MS_yKVIfM@test-3m5jgroow8mgdpyo.mlsender.net'
SMTP_PASSWORD = 'mssp.ArW97oZ.pr9084z6kyelw63d.j8DiHw6'
FROM_EMAIL = SMTP_USERNAME

def send_email(to_email, subject, body):
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
