from flask import g, Flask, render_template, url_for
import sqlite3

app = Flask(__name__)
PATH = '../db/jobs.sqlite'

def open_connection():
    connection = getattr(g._connection, default=None)

    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    
    connection.row_factory = sqlite3.Row

    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)

    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single == True else cursor.fetchall()
    
    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)

    if connection != None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()