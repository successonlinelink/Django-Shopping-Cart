from pathlib import Path
import os 


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&@7goa)46q5l9c1x+59@qtpzsib&o-y75)0v%29o^0jk_3tita'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # for humanize filter like intcomma
    
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'cart.context.default', # custom context processor
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom Admin Settings
JAZZMIN_SETTINGS = {
    "site_title": "FastCart Ecommerce",
    "site_header": "FastCart Ecommerce",
    "site_brand": "FastCart Ecommerce ",
    # "site_icon": "images/favicon.ico",
    # "site_logo": "images/logos/logo.jpg",
    "welcome_sign": "Welcome To Prime",
    "copyright": "Prime",
    "user_avatar": "images/photos/logo.jpg",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "store",
        "store.product",
        "store.cartorder",
        "store.cartorderitem",
        "store.cart",
        "store.category",
        "store.brand",
        "store.productfaq",
        "store.review",
        "vendor.Coupon",
        "vendor.DeliveryCouriers",
        "userauths",
        "userauths.user",
        "userauths.profile",
        "donations",
        "blog",
        'newsfeed',
        "contacts",
        "addon",
    ],
    "icons": {
        "admin.LogEntry": "fas fa-file",

        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",

        "userauths.User": "fas fa-user",
        "userauths.Profile":"fas fa-address-card",

        "donations.Donation": "fas fa-hand-holding-usd",
        "donations.Payment": "fas fa-credit-card",

        "newsfeed.Newsletter": "fas fa-envelope",
        "newsfeed.SubscribedUser": "fas fa-at",

        "newsfeed.SubscribedUser": "fas fa-at",

        "contacts.Inquiry": "fas fa-phone",
        "addon.BasicAddon": "fas fa-cog",

        "store.Product": "fas fa-th",
        "store.CartOrder":"fas fa-shopping-cart",
        "store.Cart":"fas fa-cart-plus",
        "store.CartOrderItem":"fas fa-shopping-basket",
        "store.Brand":"fas fa-check-circle",
        "store.productfaq":"fas fa-question",
        "store.Review":"fas fa-star fa-beat",
        "store.Category":"fas fa-tag",
        "store.Tag":"fas fa-tag",
        "store.Notification":"fas fa-bell",
        
        "customer.Address":"fas fa-location-arrow",
        "customer.Wishlist":"fas fa-heart",

        "vendor.DeliveryCouriers":"fas fa-truck",
        "vendor.Coupon":"fas fa-percentage",
        "vendor.Vendor":"fas fa-store",
        "vendor.Notification":"fas fa-bell",
        "vendor.PayoutTracker":"fas fa-wallet",
        "vendor.ChatMessage":"fas fa-envelope",

        "addons.BecomeAVendor":"fas fa-user-plus",
        "addons.AboutUS":"fas fa-users",
        "addons.Company":"fas fa-university",
        "addons.BasicAddon":"fas fa-cog",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    "related_modal_active": False,
    
    "custom_js": None,
    "show_ui_builder": True,
    
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}


customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]


