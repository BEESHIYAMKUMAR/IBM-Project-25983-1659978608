import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key='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')
from_email = Email("maaz19121.it@rmkec.ac.in")
to_email = To("maazhussain43@gmail.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "Look how beautifully the mail is being sent.. Hehehehe")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)
