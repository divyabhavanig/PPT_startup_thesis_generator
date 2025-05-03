python
import sys
import os
import subprocess
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
#EMAIL_ADDRESS = os.getenv("EMAIL_USER")
#EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""

# Read command-line arguments
ppt_path = sys.argv[1]
email_to = sys.argv[2]

# Get output directory
output_dir = os.path.dirname(ppt_path)

# Convert PPT to PDF using LibreOffice
try:
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', ppt_path, '--outdir', output_dir], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during conversion: {e}")
    sys.exit(1)

# Locate the converted PDF file
base_name = os.path.splitext(os.path.basename(ppt_path))[0]
pdf_path = os.path.join(output_dir, base_name + '.pdf')

# Compose email
msg = EmailMessage()
msg['Subject'] = 'Your Converted PDF'
msg['From'] = EMAIL_ADDRESS
msg['To'] = email_to
msg.set_content('Here is your converted PDF.')

# Attach PDF
with open(pdf_path, 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='converted.pdf')

# Send Email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("✅ Email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    sys.exit(1)