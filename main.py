from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
from app import create_app
from app.firestore_service import get_users, get_to_do, put_to_do, delete_to_do, update_to_do

import unittest

from app.forms import ToDoForm, DeleteToDoForm, UpdateToDoForm

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip']=user_ip
    
    return response
    return 'Hola'

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id

    to_do_form = ToDoForm()
    update_form = UpdateToDoForm()
    delete_form = DeleteToDoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_to_do(user_id=username),
        'username' : username,
        'to_do_form' : to_do_form,
        'update_form' : update_form,
        'delete_form' : delete_form
    }

    if to_do_form.validate_on_submit():
        put_to_do(user_id=username, description=to_do_form.description.data)

        flash('La tarea se creo con éxito')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)

@app.route('/to_dos/delete/<to_do_id>', methods={'POST'})
def delete(to_do_id):
    user_id = current_user.id
    delete_to_do(user_id=user_id, to_do_id=to_do_id)

    return redirect(url_for('hello'))

@app.route('/to_dos/update/<to_do_id>/<int:done>', methods={'POST'})
def update(to_do_id, done):
    user_id = current_user.id
    
    update_to_do(user_id=user_id, to_do_id=to_do_id, done=done)

    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(debug=True)
