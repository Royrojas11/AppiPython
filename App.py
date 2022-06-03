############# importar librerias o recursos#####
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'citas'
mysql = MySQL(app)
# settings A partir de ese momento Flask utilizará esta clave para poder cifrar la información de la cookie
app.secret_key = "mysecretkey"

# ruta para consultar todos los Usuarios
@app.route('/getUsuarios', methods=['GET'])
def getUsuarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idusuario': result[0], 'nombre': result[1], 'apellido': result[2],
            'user': result[3],'pass': result[4], 'idperfil': result[5]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

# ruta para consultar todos los Login
@app.route('/getLogin', methods=['POST'])
def getLogin():
    try:
        if request.method == 'POST':
            User = request.json['user']
            Pass = request.json['pass']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuarios WHERE user =%s AND pass=%s',
            (User,Pass))
            rv = cur.fetchall()
            return  jsonify(rv[0])
        
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
# ruta para consultar por parametro

@app.route('/getAllById/<id>',methods=['GET'])
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE idusuario = %s', (id))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idusuario': result[0], 'nombre': result[1], 'iddocumento': result[2],
            'numdocu': result[3],'user': result[4], 'pass': result[5], 'estado': result[6],
            'idperfil': result[7]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/getPerfil', methods=['GET'])
def getPerfil():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM perfil')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idperfil': result[0], 'nombre': result[1], 'estado': result [2]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})       


@app.route('/getSql2', methods=['GET'])
def getSql2():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM perfil order by estado')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idperfil': result[0], 'nombre': result[1], 'estado': result [2]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/getSql1', methods=['GET'])
def getSql1():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios order by nombre')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idusuario': result[0], 'nombre': result[1], 'apellido': result[2],'user': result[3], 'pass': result[4], 'idperfil': result[5]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE idusuario = %s', (id))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'idusuario': result[0], 'nombre': result[1], 'iddocumento': result[2], 'numdocu': result[3], 'user': result[4], 'pass': result[5],
            'estado': result[6], 'idperfil': result[7]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
    

#### ruta para crear un registro########
@app.route('/add_Perfil', methods=['POST'])
def add_Perfil():
    try:
        if request.method == 'POST':
            Nombre = request.json['nombre']
            estado = request.json['estado']            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO perfil (nombre,estado) VALUES (%s,%s)", (Nombre,estado))
            mysql.connection.commit()
            return jsonify({"informacion":"Registro exitoso"})
        
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


@app.route('/add_Usuarios', methods=['POST'])
def add_Usuarios():
    try:
        if request.method == 'POST':
            Nombre = request.json['nombre']
            Apellido = request.json['apellido']
            User = request.json['user']
            Pass = request.json['pass']
            Perfil = request.json['idperfil']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre,apellido,user,pass,idperfil) VALUES(%s,%s,%s,%s,%s)",
            (Nombre,Apellido,User,Pass,Perfil))
            mysql.connection.commit()
            return jsonify({"informacion":"Registro exitoso"})
        
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


######### ruta para actualizar################

@app.route('/update_Perfil/<id>', methods=['PUT'])
def update_Perfil(id):
    try:
        Nombre = request.json['nombre']
        estado = request.json['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE perfil
        SET nombre = %s,
        estado= %s,
        WHERE idperfil = %s
        """, (Nombre, estado, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


@app.route('/update_Usuarios/<id>', methods=['PUT'])
def update_Usuarios(id):
    try:
        idperfil = request.json['idperfil']
        Nombre = request.json['nombre']
        Apellido = request.json['apellido']
        user = request.json['user']
        password = request.json['pass']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios
        SET nombre = %s, apellido = %s, user = %s, pass = %s,idperfil = %s WHERE 
        idusuario = %s""", (Nombre, Apellido, user, password, idperfil, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/update_Reservas/<id>', methods=['PUT'])
def update_Reservas(id):
    try:
        idusuario = request.json['idusuario']
        fecha_reserva = request.json['fecha']
        hora_reserva = request.json['hora']
        estado = request.json['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE reservas
        SET idusuario = %s,
            fecha = %s,
            hora = %s,
            estado = %s,
        WHERE idreserva = %s
        """, (idusuario, fecha_reserva, hora_reserva, estado, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/update_Empleados/<id>', methods=['PUT'])
def update_Empleados(id):
    try:
        idusuario = request.json['idusuario']
        Nombre = request.json['nombre']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE empleados
        SET idusuario = %s,
            nombre = %s,
        WHERE idempleado = %s
        """, (idusuario, Nombre, id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


@app.route('/update_Detalle/<id>', methods=['PUT'])
def update_Detalle(id):
    try:
        Reserva = request.json['idreserva']
        Respuesta = request.json['respuesta']
        Estado =request.json['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE detalle
        SET idreserva = %s,
            respuesta = %s,
            estado = %s,
        WHERE iddetalle = %s
        """, (Reserva, Respuesta,Estado,id))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


##################### Ruta Eliminar ############################
@app.route('/delete_Perfil/<id>', methods = ['DELETE'])
def delete_Perfil(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM perfil WHERE idperfil = %s', (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/delete_Documentos/<id>', methods = ['DELETE'])
def delete_Documentos(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM documentos WHERE iddocuento = %s', (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/delete_Usuarios/<id>', methods = ['DELETE'])
def delete_Usuarios(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE usuarios.idusuario = %s", (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})
        

@app.route('/delete_Empleados/<id>', methods = ['DELETE'])
def delete_empleados(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM empleados WHERE empleados.idempleado = %s", (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/delete_Reservas/<id>', methods = ['DELETE'])
def delete_Reservas(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM reservas WHERE idreserva = %s', (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/delete_Detalle/<id>', methods = ['DELETE'])
def delete_Detalle(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM detalle WHERE iddetalle = %s', (id,))
        mysql.connection.commit()
        return jsonify({"informacion":"Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
