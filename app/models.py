# third-party imports
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# local imports
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class RegionModel(db.Model, UserMixin):
    """ Create an User table """
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(40), unique=True, nullable=False)
    users = db.relationship('UserModel', backref='region')

    def __repr__(self):
        return f"<Region: {self.name}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    

class UserModel(db.Model, UserMixin):
    """ Create an User table """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    login_time = db.Column(db.DateTime) 
    ip_address =db.Column(db.String(15), nullable=True, default='0.0.0.0')
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    def __repr__(self):
        return f"<User: '{self.username}' '{self.email}' '{self.image_file}'>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def get_reset_token(self, expire_secs=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'], expire_secs)
        try:
            user_id = s.loads(token)['user_id']
        except SignatureExpired:
            return None
        return UserModel.query.get(user_id)
