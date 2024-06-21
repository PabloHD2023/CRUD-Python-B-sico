from flask import Flask, render_template, request, redirect, url_for
import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')

app = Flask(__name__, template_folder= template_dir)

#Rutas de la aplicacion
@app.route('/')
def index():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertimos los datos obtenidos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close
    
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd.
@app.route('/user', methods=['POST'])
def addUser():
    user_name = request.form['user_name']
    name = request.form['name']
    password = request.form['password']

    #Condicion: Si tenemos todos los datos hacemos la consulta a la base de datos.
    if user_name and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (user_name, name, password) VALUES (%s, %s, %s)" #consulta INSERT a la BDD
        data = (user_name, name, password) #Guardamos los datos en DATA
        cursor.execute(sql, data) 
        db.database.commit() #commit a la base de datos
        
        return redirect(url_for('index')) #"REDIRECT y URL:FOR" vienen de flask y se importan.

#Ruta para eliminar datos.
@app.route('/delete/<int:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    
    return redirect(url_for('index'))

#Ruta para editar datos.
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    username = request.form['user_name']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET user_name = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
        
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
