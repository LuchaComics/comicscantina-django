# Custom Constants
#
EMPLOYEE_OWNER_ROLE = 0
EMPLOYEE_MANAGER_ROLE = 1
EMPLOYEE_WORKER_ROLE = 2

# Product Types
COMIC_PRODUCT_TYPE = 1
FURNITURE_PRODUCT_TYPE = 2
COIN_PRODUCT_TYPE = 3
GENERAL_PRODUCT_TYPE = 4

#-----------#
# DROPDOWNS #
#-----------#


ROLE_CHOICES = (
    (EMPLOYEE_OWNER_ROLE, 'Owner'),
    (EMPLOYEE_MANAGER_ROLE, 'Manager'),
    (EMPLOYEE_WORKER_ROLE, 'Worker'),
)


PRODUCT_TYPE_OPTIONS = (
    (COMIC_PRODUCT_TYPE, 'Comic'),
    (FURNITURE_PRODUCT_TYPE, 'Furniture'),
    (COIN_PRODUCT_TYPE, 'Coin'),
    #(settings.GENERAL_PRODUCT_TYPE, 'General'),
)


PAYMENT_METHOD_CHOICES = (
    (1, 'Cash'),
    (2, 'Debit Card'),
    (3, 'Credit Card'),
    (4, 'Gift Card'),
    (5, 'Store Points'),
    (6, 'Cheque'),
    (7, 'PayPal'),
    (8, 'Invoice'),
    (9, 'Other'),
)


STATUS_CHOICES = (
    (1, 'New Order'),
    (2, 'Picked'),
    (3, 'Shipped'),
    (4, 'Received'),
    (5, 'In-Store Sale'),
    (6, 'Online Sale'),
)


PRODUCT_DISCOUNT_TYPE_OPTIONS = (
    (1, '%'),
    (2, '$'),
)


# Note: https://en.wikipedia.org/wiki/ISO_4217
ISO_4217_CURRENCY_OPTIONS = (
    (124, 'CAD'),
    (840, 'USD'),
)


# Note: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
ISO_639_1_LANGUAGE_OPTIONS = (
    ('EN', 'English'),
)


STORE_HOUR_OPTIONS = (
    ('08:00', '08:00'),
    ('08:30', '08:30'),
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
    ('18:00', '18:00'),
    ('18:30', '18:30'),
    ('19:00', '19:00'),
    ('19:30', '19:30'),
    ('20:00', '20:00'),
    ('20:30', '20:30'),
    ('21:00', '21:00'),
    ('21:30', '21:30'),
    ('22:00', '22:00'),
    ('22:30', '22:30'),
)


CGC_RATING_OPTIONS = (
    (10.0, 'Gem Mint'),
    (9.9, 'Mint'),
    (9.8, 'Near Mint/Mintt'),
    (9.6, 'Near Mint +'),
    (9.4, 'Near Mint'),
    (9.2, 'Near Mint -'),
    (9.0, 'Very Fine/Near Mint'),
    (8.5, 'Very Fine +'),
    (8.0, 'Very Fine'),
    (7.5, 'Very Fine -'),
    (7.0, 'Fine/Very Fine'),
    (6.5, 'Fine +'),
    (6.0, 'Fine'),
    (5.5, 'Fine -'),
    (5.0, 'Very Good/Fine'),
    (4.5, 'Very Good +'),
    (4.0, 'Very Good'),
    (3.5, 'Very Good -'),
    (3.0, 'Good/Very Good'),
    (2.5, 'Good +'),
    (2.0, 'Good'),
    (1.8, 'Good -'),
    (1.5, 'Fair/Good'),
    (1.0, 'Fair'),
    (.5, 'Poor'),
)


LABEL_COLOUR_OPTIONS = (
    ('Purple', 'Purple'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Yellow', 'Yellow'),
)


CONDITION_RATING_RATING_OPTIONS = (
    (10, 'Near Mint'),
    (8, 'Very Fine'),
    (6, 'Fine'),
    (4, 'Very Good'),
    (2, 'Good'),
    (1, 'Fair'),
    (0, 'Poor'),
)


AGE_OPTIONS = (
    (1, 'Gold'),
    (2, 'Silver'),
    (3, 'Bronze'),
    (4, 'Copper'),
)


HELP_REQUEST_SUBJECT_CHOICES = (
    (1, 'Feedback'),
    (2, 'Error'),
    (3, 'Checkout'),
    (4, 'Inventory'),
    (5, 'Pull List'),
    (6, 'Sales'),
    (7, 'Emailing List'),
    (8, 'Store Settings / Users'),
    (9, 'Dashboard'),
)


TAX_PERCENT_OPTIONS = (
    (0.00, '0 %'),
    (0.01, '1 %'),
    (0.02, '2 %'),
    (0.03, '3 %'),
    (0.04, '4 %'),
    (0.05, '5 %'),
    (0.06, '6 %'),
    (0.07, '7 %'),
    (0.08, '8 %'),
    (0.09, '9 %'),
    (0.10, '10 %'),
    (0.11, '11 %'),
    (0.12, '12 %'),
    (0.13, '13 %'),
    (0.14, '14 %'),
    (0.15, '15 %'),
    (0.16, '16 %'),
    (0.17, '17 %'),
    (0.18, '18 %'),
    (0.19, '19 %'),
    (0.20, '20 %'),
    (0.21, '21 %'),
    (0.22, '22 %'),
    (0.23, '23 %'),
    (0.24, '24 %'),
    (0.25, '25 %'),
    (0.26, '26 %'),
    (0.27, '27 %'),
    (0.28, '28 %'),
    (0.29, '29 %'),
    (0.30, '30 %'),
    (0.31, '31 %'),
    (0.32, '32 %'),
    (0.33, '33 %'),
    (0.34, '34 %'),
    (0.35, '35 %'),
    (0.36, '36 %'),
    (0.37, '37 %'),
    (0.38, '38 %'),
    (0.39, '39 %'),
    (0.40, '40 %'),
)

PROVINCE_CHOICES = (
    ('Alberta', 'Alberta'),
    ('British Columbia', 'British Columbia'),
    ('Manitoba', 'Manitoba'),
    ('New Brunswick', 'New Brunswick'),
    ('Newfoundland and Labrador', 'Newfoundland and Labrador'),
    ('Nova Scotia', 'Nova Scotia'),
    ('Ontario', 'Ontario'),
    ('Prince Edward Island', 'Prince Edward Island'),
    ('Quebec', 'Quebec'),
    ('Saskatchewan', 'Saskatchewan'),
    ('Northwest Territories', 'Northwest Territories'),
    ('Nunavut', 'Nunavut'),
    ('Yukon', 'Yukon'),
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming'),
    ('Other', 'Other'),
)

COUNTRY_CHOICES = (
    ('Canada', 'Canada'),
    ('United States', 'United States'),
    ('Mexico', 'Mexico'),
    ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Aruba', 'Aruba'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas, The', 'Bahamas, The'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burma', 'Burma'),
    ('Burundi', 'Burundi'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Cape Verde', 'Cape Verde'),
    ('Central African Republic', 'Central African Republic'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo, Democratic Republic of the', 'Congo, Democratic Republic of the'),
    ('Congo, Republic of the', 'Congo, Republic of the'),
    ('Costa Rica', 'Costa Rica'),
    ('Cote d\'Ivoire', 'Cote d\'Ivoire'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Curacao', 'Curacao'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('East Timor', 'East Timor'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Ethiopia', 'Ethiopia'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('Gabon', 'Gabon'),
    ('Gambia, The', 'Gambia, The'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Greece', 'Greece'),
    ('Grenada', 'Grenada'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Holy See', 'Holy See'),
    ('Honduras', 'Honduras'),
    ('Hong Kong', 'Hong Kong'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran', 'Iran'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Korea, North', 'Korea, North'),
    ('Korea, South', 'Korea, South'),
    ('Kosovo', 'Kosovo'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Laos', 'Laos'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libya', 'Libya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Macau', 'Macau'),
    ('Macedonia', 'Macedonia'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mexico', 'Mexico'),
    ('Micronesia', 'Micronesia'),
    ('Moldova', 'Moldova'),
    ('Monaco', 'Monaco'),
    ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('Netherlands Antilles', 'Netherlands Antilles'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('North Korea', 'North Korea'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Palestinian Territories', 'Palestinian Territories'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Qatar', 'Qatar'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Rwanda', 'Rwanda'),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
    ('Saint Lucia', 'Saint Lucia'),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tome and Principe', 'Sao Tome and Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', 'Senegal'),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Sint Maarten', 'Sint Maarten'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Korea', 'South Korea'),
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Swaziland', 'Swaziland'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syria', 'Syria'),
    ('Taiwan', 'Taiwan'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania', 'Tanzania'),
    ('Thailand', 'Thailand'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tonga', 'Tonga'),
    ('Trinidad and Tobago', 'Trinidad and Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe'),
    ('Other', 'Other'),
)







