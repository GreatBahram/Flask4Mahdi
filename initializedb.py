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
from app.models import UserModel, RegionModel

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
admin_username = input('Enter a username for administrator, please: ')
admin_password = getpass.getpass(prompt='Enter a password for administrator, please: ')
admin_email = input('Enter an email for administrator, please: ')
#
region = RegionModel(name='Region A')
admin = UserModel(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        is_admin=True,
        region=region,
        )
#
logger.info('Adding admin user to database...')
admin.save_to_db()

user1 = UserModel(username='user1', email='user1@gmail.com', password='a', region=region,)
user2 = UserModel(username='user2', email='user2@gmail.com', password='a', region=region,)

user1.save_to_db()
user2.save_to_db()
