# Standard imports
from datetime import datetime

# third-party imports
from flask import render_template, request
from flask_login import current_user, login_required

# local import
from . import home
from app.models import UserModel

@home.route('/')
@home.route('/home')
def homepage():
    """ Render the homepage template on the / and /home route """
    return render_template('home/index.html', title="Welcome")

@home.route('/about')
def about_page():
    """ Render the about template on the /about route """
    return render_template('home/about.html', title="About")

@login_required
@home.route('/dashboard')
def dashboard_page():
    """ Render the dashboard template on the /dashboard route """
    ip_address = request.remote_addr
    traffic_usage = '2Mb'
    now = datetime.now()
    time = now - current_user.login_time

    return render_template(
            'home/dashboard.html',
            title="About",
            time=time,
            address=ip_address,
            usage=traffic_usage,
            )

@login_required
@home.route('/admin_dashboard')
def admin_dashboard_page():
    """ Render the dashboard template on the /admin_dashboard route """
    users = UserModel.query.filter_by(is_admin=False).all()
    return render_template('home/admin_dashboard.html', title="Admin", users=users)
