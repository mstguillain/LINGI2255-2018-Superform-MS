
from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python3-saml',
        'sqlalchemy','feedparser',
        'flask-sqlalchemy', 'python3-linkedin', 'facebook-sdk', 'python-twitter'
    ],
)
