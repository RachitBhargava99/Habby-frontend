from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, session
from flask_login import current_user, login_required
import requests
from PIL import Image
from io import BytesIO
from frontend.dashboard.utils import sorted_search
import asyncio
from datetime import datetime
from frontend.dashboard.forms import AddHabitForm
import json

dash = Blueprint('dash', __name__)


# View Function - Homepage / Search Results
@login_required
@dash.route('/add_habit', methods=['GET'])
def add_habit():
    if not current_user.is_authenticated:
        return json.dumps({'status': 0, 'error': "The user is not logged in."})
        return redirect(url_for('dash.dashboard'))
    form = AddHabitForm()
    if form.validate_on_submit():
        request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_HABIT_URL'], json={
            'auth_token': current_user.auth_token,
            'text': form.habit.data
        })
        data = request_data.json()
        return json.dumps({'data': data})
    return render_template('add_habit.html', form=form)
