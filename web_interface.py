from threading import Thread
from flask import Flask
from flask import render_template
from flask import request
import sqlalchemy
from flask import redirect


app = Flask('main')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
engine = sqlalchemy.create_engine('sqlite:///config.db')

def get_info():
    data = engine.execute('SELECT * FROM config WHERE type="prod"').fetchone()
    
    return data

def set_info(covalent, graph, private, sender):
    engine.execute(f'UPDATE config SET apikey_covalent="{covalent}", apikey_graphql="{graph}", private_key="{private}", sender_address="{sender}" WHERE type="prod"')

    return 'OK'

@app.route('/', methods=['POST', 'GET'])
def control_board():
    if request.method == 'GET':
        return render_template('index.html', data=get_info()), 200
    elif request.method == 'POST':
        covalent_apikey = request.form['covalent']
        graphql_apikey = request.form['graphql']
        private_key = request.form['private']
        sender_address = request.form['sender']

        set_info(covalent_apikey, graphql_apikey, private_key, sender_address)
        
        return redirect('/')
        
def return_run_thread():
    global app

    return Thread(target=app.run, daemon=True)