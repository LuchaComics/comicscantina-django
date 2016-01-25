# eCantina Production Email Configuration Instructions
## Description
This document will provide the detailed instruction set on how to setup email for the eCantina PROD server.


## Sources:
https://support.google.com/mail/answer/13287?hl=en
http://stackoverflow.com/questions/28980480/django-sending-email-smtpserverdisconnected-connection-unexpectedly-closed


## Instructions
### Gmail Configuration

1. Log into google email

2. Click Settings

3. Click "Forwarding and POP/IMAP".

4. Click "Enable IMAP"

5. Click "Save Changes"

### Google App Configuration

1. Log into google email

2. Click "Admin" in hamburger menu.

3. Click "Apps"

4. Click "Google Apps"

5. Click "Gmail"

6. Click "SMTP relay service"

7. Make sure the configuration looks like:
  ```
  Allowed senders: Only registered Apps users in my domains
  Only accept mail from the specified IP addresses: No
  Require SMTP Authentication: Yes
  Require TLS encryption: No
  ```

### Set Application Email Settings
Update your **secret_settings.py** to have the following values:

  ```
  SECRET_EMAIL_HOST = 'smtp.gmail.com'
  SECRET_EMAIL_PORT = 465                                  # 465 or 587
  SECRET_EMAIL_HOST_USER = 'support@comicscantina.com'
  SECRET_EMAIL_HOST_PASSWORD = <REDACTED>
  ```

And make sure yoyr **settings.py** look like this:
  ```
  EMAIL_USE_TLS = True
  EMAIL_HOST = SECRET_EMAIL_HOST
  EMAIL_PORT = SECRET_EMAIL_PORT
  EMAIL_HOST_USER = SECRET_EMAIL_HOST_USER
  EMAIL_HOST_PASSWORD = SECRET_EMAIL_HOST_PASSWORD
  DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
  DEFAULT_TO_EMAIL = EMAIL_HOST_USER
  SERVER_EMAIL = SECRET_EMAIL_HOST_USER

  ```

### Test Application Configuration Works
On the server, run the following code:
  ```
python3 manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'This is a test message.', 'support@comicscantina.com',['bart@mikasoftware.com'], fail_silently=False)
  ```