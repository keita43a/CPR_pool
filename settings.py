from os import environ

SESSION_CONFIGS = [
    dict(
        name='CPR_pool_game',
        display_name='個人操業とプール制の漁業実験',
        app_sequence=['try','questionaire'],
        num_demo_participants=12,
        real_world_currency_per_point=1.00,
        participation_fee=0.00,
        doc='4つの練習ラウンドと42回の本番ラウンドから成る漁業の操業を模した実験です。',
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
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'sakailab0526'

INSTALLED_APPS = ['otree', 'try','questionaire']

# security
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'test-fishery-secret-xyz123')
