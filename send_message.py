import smtplib
from email.message import EmailMessage
EMAIL_HOST = "smtp.gmail.com"
SENDER = "yusufy1403@gmail.com"



def send_email(reciever: str, password:str, content: str) -> None:
    """
        send an e-mail to the reciver

    Args:
        reciever (str): to
        password (str): sender gmail_password
        content (str):  e-mail content body
    """
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "Hava Durumu"
    msg["From"] = SENDER
    msg["to"] = reciever
    try:
        with smtplib.SMTP(host = "smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login(SENDER, password=password) # sender hesabına giriş yapılması
            smtp.send_message(msg = msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        
