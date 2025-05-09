import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.example.com"  # Replace with your SMTP server
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"  # Replace with your email
SMTP_PASSWORD = "your-email-password"  # Replace with your email password
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
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
