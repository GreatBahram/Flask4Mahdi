"""Script for initializaing your database.
Note that dropping your existing tables is an opt-in operation.
If you want to drop tables before you create tables, set an environment-
variable called "DROPDB" to be "True".
This script do the following things:
    * Drop all the database tables if you set anything in DROPDB variable.
    * Create all the tables.
    * Configure administrator user.
"""
# build-in imports
import os
import logging
import getpass

# local imports
from app import db, create_app
#from pyaccounting.models import Person

# instantiate and config the logger
logger = logging.getLogger(__name__)
logformat = '%(asctime)-12s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
        format=logformat,
        datefmt='%y/%m/%d %H-%M',
        level=logging.INFO
        )

# check the FLASK_CONFIG environment variable
logger.info('Getting the FLASK_CONFIG value...')
config_name = os.environ.get('FLASK_CONFIG', 'development')

# create the Flask app
logger.info('Creating the FLASK app...')
app = create_app(config_name)

db.app = app

db.init_app(app)

if bool(os.environ.get('DROPDB', '')):

    logger.info('Dropping all tables...')
    db.drop_all()

# create the tables
logger.info('Creating all tables...')
db.create_all()

## Administrator User
#admin_forename = input("What's your first-name? ")
#admin_surname = input("What's your last-name? ")
#admin_username = input('Enter a username for administrator, please: ')
#admin_password = getpass.getpass(prompt='Enter a password for administrator, please: ')
#admin_email = input('Enter an email for administrator, please: ')
#
#admin = Person(
#        forename=admin_forename.capitalize(),
#        surname=admin_surname.capitalize(),
#        username=admin_username,
#        email=admin_email,
#        password=admin_password,
#        is_admin=True,
#        )
#
## save admin user to the database
#logger.info('Adding admin user to database...')
#db.session.add(admin)
#db.session.commit()
