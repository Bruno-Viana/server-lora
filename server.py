import json
import sqlite3
from flask import Flask, render_template, request
import datetime;
import time
 

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        dados = conn.execute('SELECT * FROM dados').fetchall()
    except:
        with open('schema.sql') as f:
            conn.executescript(f.read())
    conn.close()
    return render_template('index.html', dados=dados)
    
@app.route('/rawdata', methods=['GET','POST'])
def handleRequest():
    conn = get_db_connection()
    if request.method == 'GET':
        try:
            dados_raw = conn.execute('SELECT * FROM dados').fetchall()
        except:
            with open('schema.sql') as f:
                conn.executescript(f.read())
            dados_raw = conn.execute('SELECT * FROM dados').fetchall()
        conn.close()
        dados_raw_tuple = [tuple(row) for row in dados_raw]
        json_string = json.dumps(dados_raw_tuple)
        return json_string
    elif request.method == 'POST':
        data = request.json
        received_value = data.get('received_value')
        timestamp_collected = data.get('timestamp_collected')
        if not received_value:
            return "Valor não informado"
        elif not timestamp_collected:
             return "Timestamp de coleta não informada"
        else:
            conn = get_db_connection()
            ct = datetime.datetime.now()
            ts = ct.timestamp()
            conn.execute('INSERT INTO dados (received_value, timestamp_collected, timestamp_sync) VALUES (?, ?, ?)',
                         (received_value, timestamp_collected, float(str(ts).split('.')[0])))
            conn.commit()
            conn.close()
        return f'Dado inserido com sucesso => received_value:{received_value} , timestamp_collected: {timestamp_collected}, timestamp_sync:{ts};'
    else:
        return "Request não permitida"
    


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date=int(date)
    dt_object = datetime.datetime.fromtimestamp(date)
    dt_brasil = dt_object.strftime("%d/%m/%Y %H:%M:%S")
    strfinal = f"{dt_brasil}"
    return strfinal

@app.template_filter('strftime2')
def _jinja2_filter_datetime(date, fmt=None):
    date=int(date)
    dt_object = datetime.datetime.fromtimestamp(date)
    dt_brasil = dt_object.strftime("%d/%m/%Y %H:%M:%S")
    strfinal = f"{dt_brasil}"
    return strfinal

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')