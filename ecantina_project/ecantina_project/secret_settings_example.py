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


#---------------------------------------------------------------------------#
# Email                                                                     #
#---------------------------------------------------------------------------#
SECRET_EMAIL_HOST = ''
SECRET_EMAIL_PORT = 587
SECRET_EMAIL_HOST_USER = ''
SECRET_EMAIL_HOST_PASSWORD = ''


#---------------------------------------------------------------------------#
# Application Specific Settings                                             #
#---------------------------------------------------------------------------#
SECRET_PAYPAL_RECEIVER_EMAIL = "yourpaypalemail@example.com"
SECRET_PAYPAL_TEST = True # Note: If True, be sure to use your test email.