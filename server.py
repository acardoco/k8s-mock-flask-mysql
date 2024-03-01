from flask import Flask, request, render_template
import logging
import mysql.connector
import os

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'mysql-service',#'mysql-service', con os.environ en docker compose no funcion
    'user': 'root',
    'password': 'word@press',
    'database': 'wordbookdb'
}

@app.route('/')
def index():
    """
    Renders the index.html template.

    Returns:
        str: The rendered HTML template.
    """
    return render_template('index.html')

@app.route('/save_word', methods=['POST'])
def save_word():
    """
    Saves a word to the MySQL database.

    Returns:
        str: A success message if the word is saved successfully, or an error message if there is an error.
    """
    if request.method == 'POST':
        word = request.form['word']
        logging.info(f'Word to save: {word}')
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO words (word) VALUES (%s)", (word,))
            connection.commit()
            return f'The word "{word}" has been saved successfully!'
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            if 'connection' in locals():
                connection.close()

'''
Desde kind hay que hacer port-forwarding 
--> kubectl port-forward flask-server-7d77649954-jw5cj <puerto_random_al_que_conectarse>:<puerto_contendor>
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
