from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

client = MongoClient("mongodb+srv://ocontreras:onesmile159@cluster0.ug30h2w.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.Joyeria
coleccionProductos=db['Producto'] 
coleccionTipoProducto=db['TipoProducto'] 
coleccionPiedra=db['Piedra'] 
coleccionMaterial=db['Material'] 
coleccionVentas=db['Venta']
coleccionEmpeños=db['Empeño']
coleccionEmpleados=db['Empleados']
coleccionClientes=db['Cliente']
coleccionCuentaUsuario=db['CuentaUsuario']
coleccionContrato=db['Contrato']
coleccionCargo=db['Cargo']

#PRODUCTOS
####################################################################################################################################################################
def listaProductos():
    productos = coleccionProductos.aggregate([
  {
    "$lookup": {
      "from": "TipoProducto",
      "localField": "ID_Tipo_Producto",
      "foreignField": "_id",
      "as": "tipo_producto"
    }
  },
  {
    "$lookup": {
      "from": "Material",
      "localField": "ID_Material",
      "foreignField": "_id",
      "as": "material"
    }
  },
  {
    "$lookup": {
      "from": "Piedra",
      "localField": "ID_Piedra",
      "foreignField": "_id",
      "as": "piedra"
    }
  },
  {
    "$project": {
      "_id": 1,
      "Tipo_Producto": { "$arrayElemAt": ["$tipo_producto.Tipo_Producto", 0] },
      "Material": { "$arrayElemAt": ["$material.Tipo_Material", 0] },
      "Piedra": { "$arrayElemAt": ["$piedra.Tipo_Piedra", 0] },
      "Precio": 1,
      "Stock": 1
    }
  }
])
    return productos

def registrarProducto(tipoProducto='', material='', piedra='', precio='', stock=''):

    ultimo_documento = coleccionProductos.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)
    
    resultado_insert=coleccionProductos.insert_one({"_id":nuevo_id,"ID_Tipo_Producto":tipoProducto,"ID_Material":material,"ID_Piedra":piedra,"Precio":precio,"Stock":stock})
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert

def updateProducto(id=''):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  productoEncontrado = list(e for e in listaProductos() if e['_id']  == int(id))[0] 
  return productoEncontrado

def detallesProducto(idProducto):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  productoEncontrado = list(e for e in listaProductos() if e['_id']  == idProducto)[0] 
  return productoEncontrado

def recibeActualizarProducto(idProducto,tipoProducto, material, piedra, precio, stock):
    resultado_insert=coleccionProductos.update_one({"_id":idProducto},{"$set":{"ID_Tipo_Producto":tipoProducto,"ID_Material":material,"ID_Piedra":piedra,"Precio":precio,"Stock":stock}})
    return resultado_insert.modified_count
####################################################################################################################################################################




#EMPLEADOS
####################################################################################################################################################################
def listaEmpleados():
    empleados = coleccionEmpleados.aggregate([
  {
    "$lookup": {
      "from": "CuentaUsuario",
      "localField": "ID_CuentaUsuario",
      "foreignField": "_id",
      "as": "cuenta_usuario"
    }
  },

  {
    "$project": {
      "_id": 1,
      "Cuenta_Usuario": { "$arrayElemAt": ["$cuenta_usuario.Username", 0] },
      "DNI_Empleado": 1,
      "Nombres": 1,
      "ApellidoPaterno": 1,
      "ApellidoMaterno": 1,
      "Fecha_Nacimiento": 1,
      "Telefono_Contacto": 1

    }
  }
])
    return empleados

def registrarEmpleado(username='', password='', dniEmpleado='', nombres='', apellidoPaterno='', apellidoMaterno='', fechaNacimiento='',
                      telefono='',remuneracion='',fechaInicio='',fechaFin='',duracion='',cargo=''):
    tipoCuenta=2
    ultimo_documento = coleccionCuentaUsuario.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

#INSERTANDO CUENTAUSUARIO
    coleccionCuentaUsuario.insert_one({"_id":nuevo_id,"Username":username,"Password":password,"ID_TipoCuentaUsuario":tipoCuenta})


    resultado_insert=coleccionEmpleados.insert_one({"_id":nuevo_id,"ID_CuentaUsuario":nuevo_id,"DNI_Empleado":dniEmpleado,"Nombres":nombres,
                                        "ApellidoPaterno":apellidoPaterno,"ApellidoMaterno":apellidoMaterno,"Fecha_Nacimiento":fechaNacimiento,"Telefono_Contacto":telefono})

    coleccionContrato.insert_one({"_id":nuevo_id,"Remuneracion":remuneracion,"Fecha_Inicio_Contrato":fechaInicio,"Fecha_Fin_Contrato":fechaFin,"Duracion_Jornada_Diaria":duracion,
                                    "ID_Empleado":nuevo_id,"ID_Cargo":cargo})
    
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert

def updateEmpleado(id=''):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  productoEncontrado = list(e for e in listaEmpleados() if e['_id']  == int(id))[0] 
  return productoEncontrado

def detallesEmpleado(idEmpleado):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  productoEncontrado = list(e for e in listaEmpleados() if e['_id']  == idEmpleado)[0] 
  return productoEncontrado

def recibeActualizarEmpleado(idEmpleado, dniEmpleado, nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento,telefono):
    resultado_insert=coleccionEmpleados.update_one({"_id":idEmpleado},{"$set":{"ID_CuentaUsuario":idEmpleado,"DNI_Empleado":dniEmpleado,"Nombres":nombres,
                                        "ApellidoPaterno":apellidoPaterno,"ApellidoMaterno":apellidoMaterno,"Fecha_Nacimiento":fechaNacimiento,"Telefono_Contacto":telefono}})
    return resultado_insert.modified_count
####################################################################################################################################################################





#TIPO PRODUCTOS
def listaTipoProductos():
    tipoProductos = coleccionTipoProducto.find()
    return tipoProductos
#MATERIALES
def listaMateriales():
    materiales = coleccionMaterial.find()
    return materiales
#MATERIALES
def listaPiedras():
    piedras = coleccionPiedra.find()
    return piedras



#CLIENTES
####################################################################################################################################################################

def listaClientes():
  clientes = coleccionClientes.find()
  return clientes

def updateCliente(id=''):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  clienteEncontrado = list(e for e in listaClientes() if e['_id']  == int(id))[0] 
  return clienteEncontrado

def detallesCliente(idCliente):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  clienteEncontrado = list(e for e in listaClientes() if e['_id']  == idCliente)[0] 
  return clienteEncontrado

def recibeActualizarCliente(idCliente, dniCliente, nombres, apellidoPaterno, apellidoMaterno, correo,telefono, fechaNacimiento):
    resultado_insert=coleccionClientes.update_one({"_id":idCliente},{"$set":{"DNI_Cliente":dniCliente,"Nombres":nombres,
                                        "ApellidoPaterno":apellidoPaterno,"ApellidoMaterno":apellidoMaterno,"Correo_Electronico":correo, "Telefono_Contacto":telefono, "Fecha_Nacimiento":fechaNacimiento}})
    return resultado_insert.modified_count
####################################################################################################################################################################











#VENTAS
####################################################################################################################################################################
def listaVentas():
 
    ventas = coleccionVentas.aggregate([
  {
    "$lookup": {
      "from": "Cliente",
      "localField": "ID_Cliente",
      "foreignField": "_id",
      "as": "cliente"
    }
  },
    {
    "$lookup": {
      "from": "Empleados",
      "localField": "ID_Empleado",
      "foreignField": "_id",
      "as": "empleados"
    }
  },
  {
    "$lookup": {
      "from": "Producto",
      "localField": "ID_Producto",
      "foreignField": "_id",
      "as": "producto"
    }
  },

  {
    "$project": {
      "_id": 1,
      "Cliente": { "$arrayElemAt": ["$cliente.DNI_Cliente", 0] },
      "Empleado": { "$arrayElemAt": ["$empleados._id", 0] },
      "Producto": { "$arrayElemAt": ["$producto._id", 0] },
      "Cantidad": 1,
      "Total": 1,
      
      "Fecha_Venta": 1
    }
  }
])
    return ventas
def registrarVentaClienteRegistrado(dniCliente='', idProducto='', cantidad='',userName=''):
    ultimo_documento = coleccionVentas.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

#INSERTANDO CUENTAUSUARIO
    doc_cliente=coleccionClientes.find_one({'DNI_Cliente':dniCliente})
    doc_cuentaUsuario=coleccionCuentaUsuario.find_one({'Username':userName})
    doc_empleado=coleccionEmpleados.find_one({'_id':doc_cuentaUsuario['_id']})
    doc_producto = coleccionProductos.find_one({'_id':idProducto})

    print(doc_cliente)
    print(doc_cuentaUsuario)
    print(doc_empleado)
    print(doc_producto)
    if cantidad <= doc_producto['Stock']:
      resultado_insert=coleccionVentas.insert_one({"_id":nuevo_id,"ID_Cliente":doc_cliente['_id'],"ID_Empleado":doc_empleado['_id'],"ID_Producto":doc_producto['_id'],
                                        "Cantidad":cantidad,"Total":cantidad*doc_producto['Precio'],"Fecha_Venta":datetime.now()})

      coleccionProductos.update_one({"_id":idProducto},{"$set":{"Stock":doc_producto["Stock"]-cantidad}})

    
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert

def registrarVentaClienteSinRegistrar(dniCliente='',nombres='',apellidoPaterno='',apellidoMaterno='',correo='',telefono='',fechaNacimiento='', idProducto='', cantidad='',userName=''):
    ultimo_documento = coleccionClientes.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

    coleccionClientes.insert_one({'_id':nuevo_id, 'DNI_Cliente':dniCliente,'Nombres':nombres,'ApellidoPaterno':apellidoPaterno,'ApellidoMaterno':apellidoMaterno,
                            'Correo_Electronico':correo,'Telefono_Contacto':telefono,'Fecha_Nacimiento':fechaNacimiento})
    
    
    
    ultimo_documento = coleccionVentas.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

#INSERTANDO CUENTAUSUARIO
    doc_cliente=coleccionClientes.find_one({'DNI_Cliente':dniCliente})
    doc_cuentaUsuario=coleccionCuentaUsuario.find_one({'Username':userName})
    doc_empleado=coleccionEmpleados.find_one({'_id':doc_cuentaUsuario['_id']})
    doc_producto = coleccionProductos.find_one({'_id':idProducto})

    print(doc_cliente)
    print(doc_cuentaUsuario)
    print(doc_empleado)
    print(doc_producto)
    if cantidad <= doc_producto['Stock']:
      resultado_insert=coleccionVentas.insert_one({"_id":nuevo_id,"ID_Cliente":doc_cliente['_id'],"ID_Empleado":doc_empleado['_id'],"ID_Producto":doc_producto['_id'],
                                        "Cantidad":cantidad,"Total":cantidad*doc_producto['Precio'],"Fecha_Venta":datetime.now()})

      coleccionProductos.update_one({"_id":idProducto},{"$set":{"Stock":doc_producto["Stock"]-cantidad}})

    
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert

def updateVenta(id=''):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  ventaEncontrado = list(e for e in listaVentas() if e['_id']  == int(id))[0] 
  return ventaEncontrado

def detallesVenta(idVenta):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  ventaEncontrado = list(e for e in listaVentas() if e['_id']  == idVenta)[0] 
  return ventaEncontrado

def recibeActualizarVenta(idVenta, dniCliente, idEmpleado, producto, cantidad, total, fechaVenta):
    resultado_insert=coleccionVentas.update_one({"_id":idVenta},{"$set":{"ID_Empleado":idEmpleado,"ID_Producto":producto,
                              "Cantidad":cantidad,"Total":total,  "Fecha_Venta":fechaVenta}})
    return resultado_insert.modified_count

####################################################################################################################################################################

def listaEmpeños():
 
    empeños = coleccionEmpeños.aggregate([
  {
    "$lookup": {
      "from": "Cliente",
      "localField": "ID_Cliente",
      "foreignField": "_id",
      "as": "cliente"
    }
  },
    {
    "$lookup": {
      "from": "Empleados",
      "localField": "ID_Empleado",
      "foreignField": "_id",
      "as": "empleados"
    }
  },
  {
    "$lookup": {
      "from": "Producto",
      "localField": "ID_Producto",
      "foreignField": "_id",
      "as": "producto"
    }
  },

  {
    "$project": {
      "_id": 1,
      "Cliente": { "$arrayElemAt": ["$cliente.DNI_Cliente", 0] },
      "Empleado": { "$arrayElemAt": ["$empleados._id", 0] },
      "Producto": { "$arrayElemAt": ["$producto._id", 0] },
      "Fecha_Empeño": 1,
      "Fecha_Vencimiento": 1,
      "Cantidad": 1,
      "Precio_Unitario": 1,
      "Estado": 1,
      "Total": 1,
      
      
    }
  }
])
    return empeños
#################################################################################################################
#AÑADIR ADDEMPEÑO
def registrarEmpeñoClienteRegistrado(dniCliente='', tipoProducto='',material='',piedra='',precio='', cantidad='',
                                                            fechaEmpeño='',fechafinalEmpeño='', userName=''):


#INSERTANDO CUENTAUSUARIO
    doc_cliente=coleccionClientes.find_one({'DNI_Cliente':dniCliente})
    doc_cuentaUsuario=coleccionCuentaUsuario.find_one({'Username':userName})
    doc_empleado=coleccionEmpleados.find_one({'_id':doc_cuentaUsuario['_id']})

    print(doc_cliente)

    ultimo_documento = coleccionProductos.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

    coleccionProductos.insert_one({"_id":nuevo_id,"ID_Tipo_Producto":tipoProducto,"ID_Material":material,"ID_Piedra":piedra,
                                  "Precio":precio,"Stock":cantidad})
    doc_producto=coleccionProductos.find_one({'_id':nuevo_id})



    ultimo_documento = coleccionEmpeños.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

    resultado_insert=coleccionEmpeños.insert_one({"_id":nuevo_id,"ID_Cliente":doc_cliente['_id'],"ID_Empleado":doc_empleado['_id'],"ID_Producto":doc_producto['_id'],
                                      "Fecha_Empeño":fechaEmpeño,"Fecha_Vencimiento":fechafinalEmpeño,"Cantidad":doc_producto['Stock'],"Precio_Unitario":precio,
                                      "Estado":fechaEmpeño<fechafinalEmpeño,"Total":cantidad*doc_producto['Precio']})

    

    
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert

def registrarEmpeñoClienteSinRegistrar(dniCliente='',nombres='',apellidoPaterno='',apellidoMaterno='',correo='',telefono='',fechaNacimiento='', idProducto='', cantidad='',userName=''):
    ultimo_documento = coleccionClientes.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

    coleccionClientes.insert_one({'_id':nuevo_id, 'DNI_Cliente':dniCliente,'Nombres':nombres,'ApellidoPaterno':apellidoPaterno,'ApellidoMaterno':apellidoMaterno,
                            'Correo_Electronico':correo,'Telefono_Contacto':telefono,'Fecha_Nacimiento':fechaNacimiento})
    
    
    
    ultimo_documento = coleccionVentas.find_one(sort=[('_id', -1)])
    ultimo_id = ultimo_documento['_id']
    nuevo_id = int(int(ultimo_id) + 1)

#INSERTANDO CUENTAUSUARIO
    doc_cliente=coleccionClientes.find_one({'DNI_Cliente':dniCliente})
    doc_cuentaUsuario=coleccionCuentaUsuario.find_one({'Username':userName})
    doc_empleado=coleccionEmpleados.find_one({'_id':doc_cuentaUsuario['_id']})
    doc_producto = coleccionProductos.find_one({'_id':idProducto})

    print(doc_cliente)
    print(doc_cuentaUsuario)
    print(doc_empleado)
    print(doc_producto)
    if cantidad <= doc_producto['Stock']:
      resultado_insert=coleccionVentas.insert_one({"_id":nuevo_id,"ID_Cliente":doc_cliente['_id'],"ID_Empleado":doc_empleado['_id'],"ID_Producto":doc_producto['_id'],
                                        "Cantidad":cantidad,"Total":cantidad*doc_producto['Precio'],"Fecha_Venta":datetime.now()})

      coleccionProductos.update_one({"_id":idProducto},{"$set":{"Stock":doc_producto["Stock"]-cantidad}})

    
    if resultado_insert.acknowledged == True:
        resultado_insert = 1
    else:
        resultado_insert = 0
    return resultado_insert








#################################################################################################################
def updateEmpeño(id=''):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  empeñoEncontrado = list(e for e in listaEmpeños() if e['_id']  == int(id))[0] 
  return empeñoEncontrado

def detallesEmpeño(idEmpeño):
  #productoEncontrado=coleccionProductos.find_one({"_id":id})
  empeñoEncontrado = list(e for e in listaEmpeños() if e['_id']  == idEmpeño)[0] 
  return empeñoEncontrado

def recibeActualizarEmpeño(idEmpeño, dniCliente, idEmpleado, producto, fechaEmpeño, fechaVencimiento, cantidad, precioUnitario, estado, total):
    resultado_insert=coleccionEmpeños.update_one({"_id":idEmpeño},{"$set":{"Fecha_Vencimiento":fechaVencimiento, "Cantidad":cantidad,"Precio_Unitario":precioUnitario,"Total":total}})
    return resultado_insert.modified_count








#EMPEÑOS
####################################################################################################################################################################

####################################################################################################################################################################


#CUENTA USUARIO
####################################################################################################################################################################
def listaCuentaUsuarios():
    cuentaUsuarios = coleccionCuentaUsuario.aggregate([
  {
    "$lookup": {
      "from": "Empleados",
      "localField": "_id",
      "foreignField": "_id",
      "as": "empleado"
    }
  },

  {
    "$project": {
      "_id": 1,
      "Nombres": { "$arrayElemAt": ["$empleado.Nombres", 0] },
      "ApellidoPaterno": { "$arrayElemAt": ["$empleado.ApellidoPaterno", 0] },
      "ApellidoMaterno": { "$arrayElemAt": ["$empleado.ApellidoMaterno", 0] },
      "Username": 1,
      "Password": 1,
      "ID_TipoCuentaUsuario": 1

    }
  }
])
    return cuentaUsuarios
####################################################################################################################################################################









