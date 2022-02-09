from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import current_user, login_required
from .. import db

import markdown2


@main.route('/')
def index():
  '''
  view for root page that returns the index page and its data
  '''

  title = 'Home - Welcome to PitchPal'

  return render_template('index.html', title=title)
