from os import environ

SESSION_CONFIGS = [
    dict(
        name='try',
        display_name='個人操業とプール制の漁業実験',
        app_sequence=['try'],
        num_demo_participants=12,
        real_world_currency_per_point=1.00,
        participation_fee=0.00,
        doc='Fishery experiment with 4 practice rounds and 42 formal rounds',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

# persist role assignment
PARTICIPANT_FIELDS = ['is_highliner']

SESSION_FIELDS = []

# oTree settings
LANGUAGE_CODE = 'ja'
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 2
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0

INSTALLED_APPS = ['otree', 'try']

# security
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'test-fishery-secret-xyz123')
