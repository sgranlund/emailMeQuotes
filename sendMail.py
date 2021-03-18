import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
senderEmail = "homeassistant1231@gmail.com"
recvEmail="sebastiangranlund@icloud.com"
message = "sup bro"

smtpServer = "smtp.gmail.com"
port = 587  # For starttls
# Create a secure SSL context
context = ssl.create_default_context()

subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
message = MIMEMultipart()
message["From"] = senderEmail
message["To"] = recvEmail
message["Subject"] = subject
message["Bcc"] = recvEmail  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))
text = message.as_string()
# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtpServer,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(senderEmail, password)
    server.sendmail(senderEmail,recvEmail,text)
    print("Email sent to ", recvEmail)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
