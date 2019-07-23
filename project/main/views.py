# project/main/views.py


#################
#### imports ####
#################
# from flask_bootstrap import Bootstrap
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project.models import User,Event
# from project.email import send_email
from project import db, bcrypt, app
# from .forms import LoginForm, RegisterForm, ChangePasswordForm


################
#### config ####
################
# bootstrap = Bootstrap(app)
main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
@login_required
def home():
    return render_template('main/index.html')


@main_blueprint.route("/events/",methods=['GET','POST'])
@login_required
def events():
    # userid = User.get_id
    if request.form:
        event = Event(desc=request.form.get("desc"),want=request.form.get("want"),
        likelihood=request.form.get("likelihood"),happened=request.form.get("happened"),author=current_user._get_current_object())
        db.session.add(event)
        db.session.commit()
        flash('The event has been created.')

        events = Event.query.all()

        # db_file = "data-dev.sqlite"
        # con = sqlite3.connect(db_file)
        # cur = con.cursor()
        # cur.execute("SELECT * FROM Events WHERE user_id =?", current_user._get_current_object(),))
        # events = cur.fetchall()

        events = Event.query.filter_by(user_id = current_user.id)
        # events = Event.query.filter_by(user_id=current_user._get_current_object()) #db.ForeignKey('users.id')

        # events = users.query.join(event, users.id==event.user_id)
        #.add_columns(users.userId, users.name, users.email, friends.userId, friendId).
        #filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
        return render_template('main/events.html',events=events)

    event = Event(desc=request.form.get("desc"))
    # events = Event.query.all()
    events = Event.query.filter_by(user_id = current_user.id)
    # events = Event.query.filter_by(user_id=db.ForeignKey('users.id'))
    # events = Event.query.filter_by(user_id=current_user._get_current_object())
    return render_template('main/events.html',events=events)


@main_blueprint.route("/events/update/", methods=["POST"])
def update():
    newdesc = request.form.get("newdesc")
    olddesc = request.form.get("olddesc")
    newhappened = request.form.get("newhappened")
    oldhappened = request.form.get("oldhappened")
    event = Event.query.filter_by(desc=olddesc).first()
    event.happened = newhappened
    db.session.commit()
    flash('The event has been updated.')
    return redirect("events")


@main_blueprint.route("/events/delete", methods=["POST"])
def delete():
    desc = request.form.get("desc")
    event = Event.query.filter_by(desc=desc).first()
    db.session.delete(event)
    db.session.commit()
    return redirect("events")