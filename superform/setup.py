from setuptools import setup

setup(

    name = 'superform',
    packages = ['superform'],
    include_package_data = True,
    install_requires = [
        'flask',
        'python3-saml',
        'sqlalchemy', 'feedparser',
        'flask-sqlalchemy', 'python3-linkedin', 'facebook-sdk',
        'python-twitter', 'rfeed', 'reportlab',
        'pyopenssl','google-api-python-client', 'oauth2client', 'google_auth_oauthlib'

    ],
)
