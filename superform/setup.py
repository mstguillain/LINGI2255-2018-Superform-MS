
from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python3-saml', 'sqlalchemy',
        'flask-sqlalchemy', 'facebook-sdk', 'python-twitter',
        'google-api-python-client', 'oauth2client'
    ],
)
