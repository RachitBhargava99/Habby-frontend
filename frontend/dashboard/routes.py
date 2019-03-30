from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, session
import requests

dash = Blueprint('dash', __name__)


@dash.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cat = request.form.getlist('cat')
        session['cat'] = [cat[0]]
        zip = request.form.get('zip') if request.form.get('zip').strip() != '' else None
        session['zip'] = zip
        session['loc_radius'] = '25mi'
        if len(cat) >= 2:
            session['cat'].append(cat[1])
            if len(cat) >= 3:
                session['cat'].append(cat[2])

        request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SEARCH_URL'],
                                         json={
                                             'cat': cat,
                                             'zip_code': zip,
                                             'loc_radius': '25mi'
                                         })

        response = request_response.json()
        events = response['events']
        pn = response['page_num']

        return render_template('courses.html', events=events, pn=pn, max=response['max'], p_list=list(
            range((pn - 2 if pn > 3 else 1), (pn + 3 if pn + 3 <= response['max'] else response['max']))))

    if request.args.get('page') is not None:
        sess = dict(session)
        print(sess)
        cat = []
        if sess.get('cat') is not None:
            cat = sess['cat']

            page_num = int(request.args['page'])
            request_response = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SEARCH_URL'],
                                             json={
                                                 'cat': cat,
                                                 'page_num': page_num,
                                                 'zip_code': sess['zip'],
                                                 'loc_radius': session['loc_radius']
                                             })

            response = request_response.json()
            events = response['events']
            pn = response['page_num']

            print(response['max'])

            return render_template('courses.html', events=events, pn=pn, max=response['max'], p_list=list(
                range((pn - 2 if pn > 3 else 1), (pn + 3 if pn + 3 <= response['max'] else response['max'] + 1))))

    request_response = requests.get(current_app.config['ENDPOINT_ROUTE'] + current_app.config['CAT_URL'])

    response = request_response.json()

    return render_template('index.html', cat=response['data'])


@dash.route('/event/<int:id>', methods=['GET'])
def show_event_details(id):
    request_response = requests.get(current_app.config['ENDPOINT_ROUTE'] + current_app.config['EVENT_URL'] + f'/{id}')
    response = request_response.json()

    if response['status'] == 0:
        flash(response['error'], 'danger')
        return redirect(url_for('dash.home'))

    event = response['event']

    return render_template('elements.html', event=event, map_key=current_app.config['GOOGLE_API_KEY'])
