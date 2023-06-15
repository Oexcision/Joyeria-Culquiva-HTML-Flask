from flask import Flask, render_template, request, redirect, session, url_for,jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from controller.controller import *


client = MongoClient("mongodb+srv://ocontreras:onesmile159@cluster0.ug30h2w.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.Joyeria

app = Flask(__name__)
app.secret_key = 'clave-secreta'
msg  =''
tipo =''

#################################################################################################################
@app.route('/')
def home():
    if 'username' in session:
        nombre= list(e for e in listaCuentaUsuarios()  if e['Username']  == session['username'])[0] 
        return render_template('public/home.html', name=nombre)
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Busqueda de cuenta
        
        result = coleccionCuentaUsuario.find_one({"Username": username, "Password": password})
        # Validar credenciales
        if result:
            session['username'] = username
            usuario=username

            return redirect('/')
        else:
            return render_template('public/login.html', error='Credenciales incorrectas')
    else:
        return render_template('public/login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/login')
######################################################################################################################################################

#                                                           PRODUCTO
######################################################################################################################################################
#Creando mi decorador para el home, el cual retornara la Lista de Productos
@app.route('/productos')
def productos():
    return render_template('public/productos.html', productos = listaProductos())

#RUTAS
@app.route('/registrar-producto', methods=['GET','POST'])
def addProducto():
    return render_template('public/acciones/addProducto.html',tipoProductos=listaTipoProductos(),materiales=listaMateriales(),piedras=listaPiedras())

#Registrando nuevo Producto
@app.route('/producto', methods=['POST'])
def formAddProducto():
    if request.method == 'POST':
        tipoProducto     = request.form['tipoProducto']
        material         = request.form['material']
        piedra           = request.form['piedra']
        precio           = request.form['precio']
        stock            = request.form['stock']
        
        if tipoProducto ==  "Anillo":
            tipoProducto = 1
        elif tipoProducto   ==  "Collar":
            tipoProducto = 2
        elif tipoProducto   ==  "Pulsera":
            tipoProducto = 3
        elif tipoProducto   ==  "Aretes":
            tipoProducto = 4

        if material ==  "Oro":
            material=1
        elif material== "Plata":
            material=2

        if piedra == "Ninguna":
            piedra=1
        elif piedra == "Diamante":
            piedra=2
        elif piedra == "Esmeralda":
            piedra=3
        elif piedra == "Perlas":
            piedra=4
        elif piedra == "Rubí":
            piedra=5
        elif piedra == "Fantasía":
            piedra=6
        elif piedra == "Amatista":
            piedra=7


        resultData = registrarProducto(tipoProducto, material, piedra, int(precio), int(stock))
        if(resultData ==1):
            return render_template('public/productos.html', productos = listaProductos(), msg='El Registro fue un éxito', tipo=1)
        else:
            return render_template('public/productos.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        

@app.route('/form-update-producto/<string:id>', methods=['GET','POST'])
def formViewUpdateProducto(id):
    if request.method == 'GET':
        resultData = updateProducto(id)
        if resultData:
            return render_template('public/acciones/updateProducto.html',  dataInfo = resultData)
        else:
            return render_template('public/productos.html', productos = listaProductos(), msg='No existe el producto', tipo= 1)
    else:
        return render_template('public/productos.html', productos = listaProductos(), msg = 'Metodo HTTP incorrecto', tipo=1)          
 

@app.route('/ver-detalles-del-producto/<int:idProducto>', methods=['GET', 'POST'])
def viewDetalleProducto(idProducto):
    msg =''
    if request.method == 'GET':
        resultData = detallesProducto(idProducto) #Funcion que almacena los detalles del producto
        
        if resultData:
            return render_template('public/acciones/viewProducto.html', infoProducto = resultData, msg='Detalles del Producto', tipo=1)
        else:
            return render_template('public/acciones/productos.html', msg='No existe el Producto', tipo=1)
    return redirect(url_for('inicio'))
    
@app.route('/actualizar-producto/<string:idProducto>', methods=['POST'])
def  formActualizarProducto(idProducto):
    if request.method == 'POST':
        tipoProducto     = request.form['tipoProducto']
        material         = request.form['material']
        piedra           = request.form['piedra']
        precio           = request.form['precio']
        stock            = request.form['stock']
        
        if tipoProducto ==  "Anillo":
            tipoProducto = 1
        elif tipoProducto   ==  "Collar":
            tipoProducto = 2
        elif tipoProducto   ==  "Pulsera":
            tipoProducto = 3
        elif tipoProducto   ==  "Aretes":
            tipoProducto = 4

        if material ==  "Oro":
            material=1
        elif material== "Plata":
            material=2

        if piedra == "Ninguna":
            piedra=1
        elif piedra == "Diamante":
            piedra=2
        elif piedra == "Esmeralda":
            piedra=3
        elif piedra == "Perlas":
            piedra=4
        elif piedra == "Rubí":
            piedra=5
        elif piedra == "Fantasía":
            piedra=6
        elif piedra == "Amatista":
            piedra=7
        
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarProducto(int(idProducto), int(tipoProducto), int(material), int(piedra), int(precio), int(stock))
        if(resultData ==1):
            return render_template('public/productos.html', productos = listaProductos(), msg='Datos del producto actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/productos.html', productos = listaProductos(), msg = 'No se pudo actualizar', tipo=1) 

#Eliminar producto
@app.route('/borrar-producto', methods=['GET', 'POST'])
def formViewBorrarProducto():
    if request.method == 'POST':
        idProducto        = request.form['id']
        resultData      = eliminarProducto(idProducto)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarProducto(idProducto):
    print(idProducto)
    producto_eliminado=coleccionProductos.delete_one({'_id': int(idProducto)})
    resultado_eliminar=producto_eliminado.deleted_count
    print(resultado_eliminar)
    return resultado_eliminar






#####################################################################################################################################################################



#                                                                         EMPLEADO
#####################################################################################################################################################################
@app.route('/empleados')
def empleados():
    return render_template('public/empleados.html', empleados = listaEmpleados())

#RUTAS
@app.route('/registrar-empleado', methods=['GET','POST'])
def addEmpleado():
    return render_template('public/acciones/addEmpleado.html')

#Registrando nuevo Empleado
@app.route('/empleado', methods=['POST'])
def formAddEmpleado():
    if request.method == 'POST':
        username         = request.form['username']
        password         = request.form['password']
        dniEmpleado      = request.form['dniEmpleado']
        nombres          = request.form['nombres']
        apellidoPaterno  = request.form['apellidoPaterno']
        apellidoMaterno  = request.form['apellidoMaterno']
        fechaNacimiento  = request.form['fechaNacimiento']
        telefono         = request.form['telefono']
        
        
        resultData = registrarEmpleado(username, password, int(dniEmpleado), nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento,int(telefono))
        if(resultData ==1):
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='El Registro fue un éxito', tipo=1)
        else:
            return render_template('public/empleados.html', msg = 'Metodo HTTP incorrecto', tipo=1)   



@app.route('/form-update-empleado/<string:id>', methods=['GET','POST'])
def formViewUpdateEmpleado(id):
    if request.method == 'GET':
        resultData = updateEmpleado(id)
        if resultData:
            return render_template('public/acciones/updateEmpleado.html',  dataInfo = resultData)
        else:
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='No existe el empleado', tipo= 1)
    else:
        return render_template('public/empleados.html', empleados = listaEmpleados(), msg = 'Metodo HTTP incorrecto', tipo=1)      


@app.route('/ver-detalles-del-empleado/<int:idEmpleado>', methods=['GET', 'POST'])
def viewDetalleEmpleado(idEmpleado):
    msg =''
    if request.method == 'GET':
        resultData = detallesEmpleado(idEmpleado) #Funcion que almacena los detalles del producto
        
        if resultData:
            return render_template('public/acciones/viewEmpleado.html', infoEmpleado = resultData, msg='Detalles del Empleado', tipo=1)
        else:
            return render_template('public/acciones/empleados.html', msg='No existe el Empleado', tipo=1)
    return redirect(url_for('inicio'))


@app.route('/actualizar-empleado/<string:idEmpleado>', methods=['POST'])
def  formActualizarEmpleado(idEmpleado):
    if request.method == 'POST':
        dniEmpleado      = request.form['dniEmpleado']
        nombres          = request.form['nombres']
        apellidoPaterno  = request.form['apellidoPaterno']
        apellidoMaterno  = request.form['apellidoMaterno']
        fechaNacimiento  = request.form['fechaNacimiento']
        telefono         = request.form['telefono']
        

        
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarEmpleado(int(idEmpleado),int(dniEmpleado), nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento,int(telefono))
        if(resultData ==1):
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='Datos del empleado actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg = 'No se pudo actualizar', tipo=1)

#Eliminar empleado
@app.route('/borrar-empleado', methods=['GET', 'POST'])
def formViewBorrarEmpleado():
    if request.method == 'POST':
        idEmpleado       = request.form['id']
        resultData      = eliminarEmpleado(idEmpleado)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarEmpleado(idEmpleado):
    print(idEmpleado)
    empleado_eliminado=coleccionEmpleados.delete_one({'_id': int(idEmpleado)})
    resultado_eliminar=empleado_eliminado.deleted_count
    print(resultado_eliminar)
    return resultado_eliminar
####################################################################################################################################################################

#CLIENTES
####################################################################################################################################################################

@app.route('/clientes')
def clientes():
    return render_template('public/clientes.html', clientes = listaClientes())

@app.route('/form-update-cliente/<string:id>', methods=['GET','POST'])
def formViewUpdateCliente(id):
    if request.method == 'GET':
        resultData = updateCliente(id)
        if resultData:
            return render_template('public/acciones/updateCliente.html',  dataInfo = resultData)
        else:
            return render_template('public/clientes.html', clientes = listaClients(), msg='No existe el empleado', tipo= 1)
    else:
        return render_template('public/clientes.html', clientes = listaClientes(), msg = 'Metodo HTTP incorrecto', tipo=1)      

@app.route('/ver-detalles-del-cliente/<int:idCliente>', methods=['GET', 'POST'])
def viewDetalleCliente(idCliente):
    msg =''
    if request.method == 'GET':
        resultData = detallesCliente(idCliente) #Funcion que almacena los detalles del producto
        
        if resultData:
            return render_template('public/acciones/viewCliente.html', infoCliente = resultData, msg='Detalles del Cliente', tipo=1)
        else:
            return render_template('public/acciones/clientes.html', msg='No existe el Cliente', tipo=1)
    return redirect(url_for('inicio'))

@app.route('/actualizar-cliente/<string:idCliente>', methods=['POST'])
def  formActualizarCliente(idCliente):
    if request.method == 'POST':
        dniCliente      = request.form['dniCliente']
        nombres          = request.form['nombres']
        apellidoPaterno  = request.form['apellidoPaterno']
        apellidoMaterno  = request.form['apellidoMaterno']
        correo           = request.form['correo']
        telefono         = request.form['telefono']
        fechaNacimiento  = request.form['fechaNacimiento']
        

        
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarCliente(int(idCliente),int(dniCliente), nombres, apellidoPaterno, apellidoMaterno, correo,int(telefono),fechaNacimiento)
        if(resultData ==1):
            return render_template('public/clientes.html', clientes = listaClientes(), msg='Datos del cliente actualizados', tipo=1)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/clientes.html', clientes = listaClientes(), msg = 'No se pudo actualizar', tipo=1)


#Eliminar cliente
@app.route('/borrar-cliente', methods=['GET', 'POST'])
def formViewBorrarCliente():
    if request.method == 'POST':
        idCliente       = request.form['id']
        resultData      = eliminarCliente(idCliente)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarCliente(idCliente):
    print(idCliente)
    cliente_eliminado=coleccionClientes.delete_one({'_id': int(idCliente)})
    resultado_eliminar=cliente_eliminado.deleted_count
    print(resultado_eliminar)
    return resultado_eliminar
####################################################################################################################################################################

#VENTAS 
####################################################################################################################################################################
@app.route('/ventas')
def ventas():
    return render_template('public/ventas.html', ventas = listaVentas())


####################################################################################################################################################################




@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('productos'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)