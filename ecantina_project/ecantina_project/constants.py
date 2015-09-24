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
