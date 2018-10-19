from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python3-saml', 'sqlalchemy', 'python-twitter'
    ],
)
# flask_sqlalchemy missing
