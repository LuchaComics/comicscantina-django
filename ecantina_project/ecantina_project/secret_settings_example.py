import sys

#---------------------------------------------------------------------------#
# Generic                                                                   #
#---------------------------------------------------------------------------#
SECRET_DEBUG = True
SECRET_SECRET_KEY = '^0#kc^_(25gi!94s9^=oydo=#nmv@j^@z9f8=7un*c#_d-36$$'
SECRET_ALLOWED_HOSTS = []


#---------------------------------------------------------------------------#
# Database                                                                  #
#---------------------------------------------------------------------------#
SECRET_DB_USER = "django"
SECRET_DB_PASSWORD = "123password"
SECRET_DB_HOST = "localhost"
SECRET_DB_PORT = "5432"


#---------------------------------------------------------------------------#
# Email                                                                     #
#---------------------------------------------------------------------------#
SECRET_EMAIL_HOST = ''
SECRET_EMAIL_PORT = 587
SECRET_EMAIL_HOST_USER = ''
SECRET_EMAIL_HOST_PASSWORD = ''


#---------------------------------------------------------------------------#
# PayPal Settings                                                           #
#---------------------------------------------------------------------------#
SECRET_PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"
SECRET_PAYPAL_TEST = True # Note: If True, be sure to use your test email.

#---------------------------------------------------------------------------#
# Google Analytics Settings                                                 #
#---------------------------------------------------------------------------#
#Note: Leaving it blank turns of analytics in the store.
SECRET_GOOGLE_ANALYTICS_KEY = "UA-70664917-2"


#---------------------------------------------------------------------------#
# Domain Settings                                                           #
#---------------------------------------------------------------------------#
#Note: Leaving it blank turns of analytics in the store.
SECRET_DOMAIN = "consolebits.com"
SECRET_HTTP_PROTOCOL = "http://"