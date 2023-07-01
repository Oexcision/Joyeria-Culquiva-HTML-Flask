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
tipo_cuenta=0

#################################################################################################################
@app.route('/')
def home():
    if 'username' in session:
        global tipo_cuenta
        nombre= list(e for e in listaCuentaUsuarios()  if e['Username']  == session['username'])[0] 
        tipo_cuenta=nombre['ID_TipoCuentaUsuario']
        return render_template('public/home.html', name=nombre, tipo_cuenta=tipo_cuenta)
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
    return render_template('public/productos.html', productos = listaProductos(), tipo_cuenta=tipo_cuenta)

#RUTAS
@app.route('/registrar-producto', methods=['GET','POST'])
def addProducto():
    return render_template('public/acciones/addProducto.html',tipoProductos=listaTipoProductos(),materiales=listaMateriales(),piedras=listaPiedras() , tipo_cuenta=tipo_cuenta)

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
            return render_template('public/productos.html', productos = listaProductos(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/productos.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   
        

@app.route('/form-update-producto/<string:id>', methods=['GET','POST'])
def formViewUpdateProducto(id):
    if request.method == 'GET':
        resultData = updateProducto(id)
        if resultData:
            return render_template('public/acciones/updateProducto.html',  dataInfo = resultData, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/productos.html', productos = listaProductos(), msg='No existe el producto', tipo= 1, tipo_cuenta=tipo_cuenta)
    else:
        return render_template('public/productos.html', productos = listaProductos(), msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)          
 

@app.route('/ver-detalles-del-producto/<int:idProducto>', methods=['GET', 'POST'])
def viewDetalleProducto(idProducto):
    msg =''
    if request.method == 'GET':
        resultData = detallesProducto(idProducto) #Funcion que almacena los detalles del producto
        
        if resultData:
            return render_template('public/acciones/viewProducto.html', infoProducto = resultData, msg='Detalles del Producto', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/acciones/productos.html', msg='No existe el Producto', tipo=1, tipo_cuenta=tipo_cuenta)
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
            return render_template('public/productos.html', productos = listaProductos(), msg='Datos del producto actualizados', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/productos.html', productos = listaProductos(), msg = 'No se pudo actualizar', tipo=1, tipo_cuenta=tipo_cuenta) 

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
    return render_template('public/empleados.html', empleados = listaEmpleados(), tipo_cuenta=tipo_cuenta)

#RUTAS
@app.route('/registrar-empleado', methods=['GET','POST'])
def addEmpleado():
    return render_template('public/acciones/addEmpleado.html', tipo_cuenta=tipo_cuenta)

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

        remuneracion     = request.form['remuneracion']
        fechaInicio      = request.form['fechaInicio']
        fechaFin         = request.form['fechaFin']
        duracion         = request.form['duracion']

        cargo            = request.form['cargo']

        print(fechaNacimiento,fechaInicio,fechaFin)

        fechaNacimiento=datetime.strptime(str(fechaNacimiento), '%Y-%m-%d')
        fechaInicio=datetime.strptime(str(fechaInicio), '%Y-%m-%d')
        fechaFin=datetime.strptime(str(fechaFin), '%Y-%m-%d')

        if cargo ==  "Vendedor":
            cargo = 1
        elif cargo   ==  "Orfebre":
            cargo = 2
        elif cargo   ==  "Experto Prestamista":
            cargo = 3
        
        print(cargo,type(cargo))
        
        resultData = registrarEmpleado(username, password, int(dniEmpleado), nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento,int(telefono), int(remuneracion),fechaInicio,fechaFin,int(duracion),int(cargo))
        if(resultData ==1):
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/empleados.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   



@app.route('/form-update-empleado/<string:id>', methods=['GET','POST'])
def formViewUpdateEmpleado(id):
    if request.method == 'GET':
        resultData = updateEmpleado(id)
        resultDataContrato = updateContrato(id)
        if resultData:
            return render_template('public/acciones/updateEmpleado.html',  dataInfo = resultData, dataInfoContrato=resultDataContrato, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='No existe el empleado', tipo= 1, tipo_cuenta=tipo_cuenta)
    else:
        return render_template('public/empleados.html', empleados = listaEmpleados(), msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)      


@app.route('/ver-detalles-del-empleado/<int:idEmpleado>', methods=['GET', 'POST'])
def viewDetalleEmpleado(idEmpleado):
    msg =''
    if request.method == 'GET':
        resultData = detallesEmpleado(idEmpleado) #Funcion que almacena los detalles del producto
        resultDataContrato = detallesContrato(idEmpleado)
        
        if resultData:
            return render_template('public/acciones/viewEmpleado.html', infoEmpleado = resultData, infoContrato = resultDataContrato, msg='Detalles del Empleado', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/acciones/empleados.html', msg='No existe el Empleado', tipo=1, tipo_cuenta=tipo_cuenta)
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

        remuneracion     = request.form['remuneracion']
        fechaInicio      = request.form['fechaInicio']
        fechaFin         = request.form['fechaFin']
        duracion         = request.form['duracion']

        cargo            = request.form['cargo']
        
        if cargo ==  "Vendedor":
            cargo = 1
        elif cargo   ==  "Orfebre":
            cargo = 2
        elif cargo   ==  "Experto Prestamista":
            cargo = 3
        fechaInicio=datetime.strptime(fechaInicio, '%Y-%m-%d %H:%M:%S')
        fechaFin=datetime.strptime(fechaFin, '%Y-%m-%d %H:%M:%S')
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarEmpleado(int(idEmpleado),int(dniEmpleado), nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento,int(telefono),
                                            int(remuneracion), fechaInicio, fechaFin,int(duracion),int(cargo))
        if(resultData ==1):
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg='Datos del empleado actualizados', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/empleados.html', empleados = listaEmpleados(), msg = 'No se pudo actualizar', tipo=1, tipo_cuenta=tipo_cuenta)

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
    return render_template('public/clientes.html', clientes = listaClientes(), tipo_cuenta=tipo_cuenta)

@app.route('/form-update-cliente/<string:id>', methods=['GET','POST'])
def formViewUpdateCliente(id):
    if request.method == 'GET':
        resultData = updateCliente(id)
        if resultData:
            return render_template('public/acciones/updateCliente.html',  dataInfo = resultData, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/clientes.html', clientes = listaClientes(), msg='No existe el cliente', tipo= 1, tipo_cuenta=tipo_cuenta)
    else:
        return render_template('public/clientes.html', clientes = listaClientes(), msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   

@app.route('/ver-detalles-del-cliente/<int:idCliente>', methods=['GET', 'POST'])
def viewDetalleCliente(idCliente):
    msg =''
    if request.method == 'GET':
        resultData = detallesCliente(idCliente) #Funcion que almacena los detalles del producto
        
        if resultData:
            return render_template('public/acciones/viewCliente.html', infoCliente = resultData, msg='Detalles del Cliente', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/acciones/clientes.html', msg='No existe el Cliente', tipo=1, tipo_cuenta=tipo_cuenta)
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
            return render_template('public/clientes.html', clientes = listaClientes(), msg='Datos del cliente actualizados', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/clientes.html', clientes = listaClientes(), msg = 'No se pudo actualizar', tipo=1, tipo_cuenta=tipo_cuenta)


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
existe=None
@app.route("/consultar_cliente", methods=["POST"])
def consultar_cliente():
    global existe
    dniCliente = request.json["dniCliente"]
    print(dniCliente)
    # Realizar la consulta en MongoDB
    documento = coleccionClientes.find_one({"DNI_Cliente": int(dniCliente)})
    print(documento)
    existe = documento is not None
    if existe:
      return jsonify({"existe": existe,"ID_Cliente": documento['_id']})
    else:
      return jsonify({"existe": existe})
    # Enviar la respuesta al cliente
    
@app.route('/ventas')
def ventas():
    return render_template('public/ventas.html', ventas = listaVentas(), tipo_cuenta=tipo_cuenta)

@app.route('/registrar-venta', methods=['GET','POST'])
def addVenta():
    return render_template('public/acciones/addVenta.html',ventas=listaVentas(),clientes=listaClientes(), tipo_cuenta=tipo_cuenta)


#Registrando nuevo Venta
@app.route('/venta', methods=['POST'])
def formAddVenta():
    if request.method == 'POST':

        dniCliente          = request.form['dniCliente']
        nombres             = request.form['nombres']
        apellidoPaterno     = request.form['apellidoPaterno']
        apellidoMaterno     = request.form['apellidoMaterno']
        correo              = request.form['correo']
        telefono            = request.form['telefono']
        fechaNacimiento     = request.form['fechaNacimiento']
        idProducto          = request.form['idProducto']
        cantidad            = request.form['cantidad']
        if fechaNacimiento!='':
            fechaNacimiento=datetime.strptime(str(fechaNacimiento), '%Y-%m-%d')
        print(existe)
        print(session['username'])
        if existe==True:
            resultData = registrarVentaClienteRegistrado(int(dniCliente), int(idProducto), int(cantidad), session['username'])
            if(resultData ==1):
                return render_template('public/ventas.html', ventas = listaVentas(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
            else:
                return render_template('public/ventas.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   
           
        else:
            resultData = registrarVentaClienteSinRegistrar(int(dniCliente),nombres,apellidoPaterno,apellidoMaterno,correo,int(telefono),fechaNacimiento, int(idProducto), int(cantidad), session['username'])
            if(resultData ==1):
                return render_template('public/ventas.html', ventas = listaVentas(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
            else:
                return render_template('public/ventas.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   
        






@app.route('/form-update-venta/<string:id>', methods=['GET','POST'])
def formViewUpdateVenta(id):
    if request.method == 'GET':
        resultData = updateVenta(id)
        if resultData:
            return render_template('public/acciones/updateVenta.html',  dataInfo = resultData, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/ventas.html', ventas = listaVentas(), msg='No existe la Venta', tipo= 1, tipo_cuenta=tipo_cuenta)
    else:
        return render_template('public/ventas.html', ventas = listaVentas(), msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)      

@app.route('/ver-detalles-del-venta/<int:idVenta>', methods=['GET', 'POST'])
def viewDetalleVenta(idVenta):
    msg =''
    if request.method == 'GET':
        resultData = detallesVenta(idVenta) #Funcion que almacena los detalles del venta
        
        if resultData:
            return render_template('public/acciones/viewVenta.html', infoVenta = resultData, msg='Detalles del Venta', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/acciones/ventas.html', msg='No existe la Venta', tipo=1, tipo_cuenta=tipo_cuenta)
    return redirect(url_for('inicio'))

@app.route('/actualizar-venta/<string:idVenta>', methods=['POST'])
def  formActualizarVenta(idVenta):
    if request.method == 'POST':
        dniCliente  = request.form['dniCliente']
        empleado    = request.form['empleado']
        producto    = request.form['producto']
        cantidad    = request.form['cantidad']
        total       = request.form['total']
        fechaVenta  = request.form['fechaVenta']
        

        fechaVenta=datetime.now()
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarVenta(int(idVenta),int(dniCliente),int(empleado), int(producto), int(cantidad), int(total), fechaVenta)
        if(resultData ==1):
            return render_template('public/ventas.html', ventas = listaVentas(), msg='Datos de la Venta actualizados', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/ventas.html', ventas = listaVentas(), msg = 'No se pudo actualizar', tipo=1, tipo_cuenta=tipo_cuenta)


#Eliminar venta
@app.route('/borrar-venta', methods=['GET', 'POST'])
def formViewBorrarVenta():
    if request.method == 'POST':
        idVenta       = request.form['id']
        resultData      = eliminarVenta(idVenta)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarVenta(idVenta):
    print(idVenta)
    venta_eliminado=coleccionVentas.delete_one({'_id': int(idVenta)})
    resultado_eliminar=venta_eliminado.deleted_count
    print(resultado_eliminar)
    return resultado_eliminar
####################################################################################################################################################################

#EMPEÑOS 
####################################################################################################################################################################
@app.route('/empeños')
def empeños():
    return render_template('public/empeños.html', empeños = listaEmpeños(), tipo_cuenta=tipo_cuenta)
#################################################################################################################
@app.route('/registrar-empeño', methods=['GET','POST'])
def addEmpeño():
    return render_template('public/acciones/addEmpeño.html',empeños=listaEmpeños(),clientes=listaClientes(), tipoProductos=listaTipoProductos(),materiales=listaMateriales(),piedras=listaPiedras(), tipo_cuenta=tipo_cuenta)


#Registrando nuevo Venta
@app.route('/empeño', methods=['POST'])
def formAddEmpeño():
    if request.method == 'POST':

        dniCliente          = request.form['dniCliente']
        nombres             = request.form['nombres']
        apellidoPaterno     = request.form['apellidoPaterno']
        apellidoMaterno     = request.form['apellidoMaterno']
        correo              = request.form['correo']
        telefono            = request.form['telefono']
        fechaNacimiento     = request.form['fechaNacimiento']

        tipoProducto        = request.form['tipoProducto']
        material            = request.form['material']
        piedra              = request.form['piedra']
        precio              = request.form['precio']
        cantidad            = request.form['cantidad']

        fechafinalEmpeño    = request.form['fechafinalEmpeño']

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

        if fechaNacimiento!='':
            fechaNacimiento=datetime.strptime(str(fechaNacimiento), '%Y-%m-%d')
        fechaEmpeño=datetime.now()
        fechafinalEmpeño=datetime.strptime(str(fechafinalEmpeño), '%Y-%m-%d')

        print(existe)
        print(session['username'])
        if existe==True:
            resultData = registrarEmpeñoClienteRegistrado(int(dniCliente), int(tipoProducto),int(material),int(piedra),int(precio), int(cantidad),
                                                            fechaEmpeño,fechafinalEmpeño, session['username'])
            if(resultData ==1):
                return render_template('public/empeños.html', empeños = listaEmpeños(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
            else:
                return render_template('public/empeños.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   
           
        else:
            resultData = registrarEmpeñoClienteSinRegistrar(int(dniCliente),nombres,apellidoPaterno,apellidoMaterno,correo,int(telefono),
                                                            fechaNacimiento, int(tipoProducto),int(material),int(piedra),int(precio), int(cantidad),
                                                            fechaEmpeño,fechafinalEmpeño, session['username'])
            if(resultData ==1):
                return render_template('public/empeños.html', empeños = listaEmpeños(), msg='El Registro fue un éxito', tipo=1, tipo_cuenta=tipo_cuenta)
            else:
                return render_template('public/empeños.html', msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)   
        
#################################################################################################################


@app.route('/form-update-empeño/<string:id>', methods=['GET','POST'])
def formViewUpdateEmpeño(id):
    if request.method == 'GET':
        resultData = updateEmpeño(id)
        if resultData:
            return render_template('public/acciones/updateEmpeño.html',  dataInfo = resultData, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/empeños.html', empeños = listaEmpeños(), msg='No existe el Empeño', tipo= 1, tipo_cuenta=tipo_cuenta)
    else:
        return render_template('public/empeños.html', empeños = listaEmpeños(), msg = 'Metodo HTTP incorrecto', tipo=1, tipo_cuenta=tipo_cuenta)      

@app.route('/ver-detalles-del-empeño/<int:idEmpeno>', methods=['GET', 'POST'])
def viewDetalleEmpeño(idEmpeno):
    msg =''
    if request.method == 'GET':
        resultData = detallesEmpeño(idEmpeno) #Funcion que almacena los detalles del empeño
        
        if resultData:
            return render_template('public/acciones/viewEmpeño.html', infoEmpeño = resultData, msg='Detalles del Empeño', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            return render_template('public/acciones/empeños.html', msg='No existe el Empeño', tipo=1, tipo_cuenta=tipo_cuenta)
    return redirect(url_for('inicio'))

@app.route('/actualizar-empeño/<string:idEmpeno>', methods=['POST'])
def  formActualizarEmpeño(idEmpeno):
    if request.method == 'POST':
        dniCliente          = request.form['dniCliente']
        empleado            = request.form['empleado']
        producto            = request.form['producto']
        fechaEmpeño         = request.form['fechaEmpeño']
        fechaVencimiento    = request.form['fechaVencimiento']
        cantidad            = request.form['cantidad']
        precioUnitario      = request.form['precioUnitario']
        estado              = request.form['estado']
        total               = request.form['total']
        
        
        fechaEmpeño=datetime.now()
        fechaVencimiento=datetime.strptime(fechaVencimiento, '%Y-%m-%d %H:%M:%S')
        #Script para recibir el archivo (foto)
        resultData = recibeActualizarEmpeño(int(idEmpeno),int(dniCliente),int(empleado), int(producto), fechaEmpeño, fechaVencimiento, int(cantidad), int(precioUnitario), estado, int(total))
        if(resultData ==1):
            return render_template('public/empeños.html', empeños = listaEmpeños(), msg='Datos del Empeños actualizados', tipo=1, tipo_cuenta=tipo_cuenta)
        else:
            msg ='No se actualizo el registro'
            return render_template('public/empeños.html', empeños = listaEmpeños(), msg = 'No se pudo actualizar', tipo=1, tipo_cuenta=tipo_cuenta)


#Eliminar venta
@app.route('/borrar-empeño', methods=['GET', 'POST'])
def formViewBorrarEmpeño():
    if request.method == 'POST':
        idEmpeno       = request.form['id']
        resultData      = eliminarEmpeño(idEmpeno)

        if resultData ==1:
            #Nota: retorno solo un json y no una vista para evitar refescar la vista
            return jsonify([1])
            #return jsonify(["respuesta", 1])
        else: 
            return jsonify([0])


def eliminarEmpeño(idEmpeno):
    print(idEmpeno)
    empeño_eliminado=coleccionEmpeños.delete_one({'_id': int(idEmpeno)})
    resultado_eliminar=empeño_eliminado.deleted_count
    print(resultado_eliminar)
    return resultado_eliminar

####################################################################################################################################################################


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('productos'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)