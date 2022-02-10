from unicodedata import category
from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import current_user, login_required
from .. import db,photos
from .forms import UpdateProfile, PitchForm
from ..models import Pitch, User, PhotoProfile
from datetime import datetime

import markdown2


@main.route('/')
@login_required
def index():
  '''
  view for root page that returns the index page and its data
  '''

  title = 'Home - Welcome to PitchPal'
  user = current_user.username

  form = PitchForm()

  if form.validate_on_submit():
    pitch = Pitch(title=form.title.data, category=form.title.data, posted=datetime.now, user_id=user.id)
    pitch.save_pitch()
    return redirect(url_for(main.index))

  return render_template('index.html', title=title, user=user, pitch_form=form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
