from django.db import models

# ////////////////////////////////////////////// gestor de centros ////////////////////////////////////////////////////////////////////////////
#paises
class Country(models.Model):
 id_Country = models.AutoField(primary_key =True)
 name_Country = models.CharField(max_length= 100, unique=True, null=False)

 def __str__(self):
  return self.name_Country

#departamentos
class Department(models.Model):
 id_department = models.AutoField(primary_key=True)
 id_Country = models.ForeignKey(Country, on_delete=models.CASCADE)
 name_department = models.CharField(max_length= 100,unique=True, null = False)

 def __str__(self):
  return self.name_department


#ciudad
class City(models.Model):
 id_City = models.AutoField(primary_key=True)
 id_Country = models.ForeignKey(Country, on_delete=models.CASCADE)
 id_department =models.ForeignKey(Department, on_delete=models.CASCADE)
 name_City = models.CharField(max_length= 100, unique=True, null=False)

 def __str__(self):
  return self.name_City
 
#sede
class Sede(models.Model):
 id_sede = models.AutoField(primary_key= True)
 id_City = models.ForeignKey(City, on_delete=models.CASCADE)
 name_sede = models.CharField(max_length=100, unique=True, null=False)
 direccion_sede = models.CharField(max_length= 100,unique=True, null=False)
 contact_one =models.BigIntegerField(null=True)
 contact_two = models.BigIntegerField(null=True)
 date_register = models.DateTimeField(null=False, auto_now=True)

 def __str__(self):
  return self.name_sede

#centros
class centro(models.Model):
 id_centro = models.AutoField(primary_key=True)
 id_sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
 name_centro = models.CharField(max_length =100,null=True)
 descripcion_centro = models.TextField(null=False)
 fecha_registro = models.DateTimeField(null=False, auto_now=True)

 def __str__(self):
  return self.name_centro

# ////////////////////////////////////////////////////////////////////////////////// MESA DE AYUDA //////////////////////////////////////

#roles
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name_rol = models.CharField(max_length=100, null=False,  unique=True)

    def __str__(self):
        return str(self.name_rol)
#tipo de documento  
class TypeDocument(models.Model):
    id_typeDocument = models.AutoField(primary_key=True)
    name_documento = models.CharField(max_length=100, null=False,  unique=True)
    simbols = models.CharField(max_length=100, null=False,  unique=True)

    def __str__(self):
        return self.name_documento
# estado del usuario, activo, inactivo, bloqueado 
class Statu(models.Model):
    id_status = models.AutoField(primary_key=True)
    name_status = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name_status
    
# tabla para los usuarios del sistema     
class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False)  
    last_name = models.CharField(max_length=100, null=False)  
    document = models.BigIntegerField(unique=True)  
    email = models.EmailField(max_length=100, null=False, unique=True) 
    primary_contact = models.BigIntegerField()  
    secondary_contact = models.BigIntegerField(null=True)  
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    id_type_document = models.ForeignKey(TypeDocument, on_delete=models.CASCADE) 
    id_centro = models.ForeignKey(centro, on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now=True) 
    last_login = models.DateTimeField(null=True)
    id_status = models.ForeignKey(Statu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.first_name)
    
#contraseña del usuario
class Password(models.Model):
    id_password = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=100, null=False)
    creation_date = models.DateField(null=False)
    expiration_date = models.DateField(null=False)
    def __str__(self):
        return str(self.id_user)




# /////////////////////////////////////////////// BODEGA ///////////////////////////////////////////////////////////////////////////

#ubicaciones dentro los centros
class Ubication(models.Model):
    idUbication = models.AutoField(primary_key=True)
    id_centro = models.ForeignKey(centro, on_delete=models.CASCADE)
    name_Ubication = models.CharField(max_length=100)
    description_ubication = models.TextField()
    def __str__(self):
        return str(self.name_Ubication)

#tabla para el estado de: bueno, malo, regular de objetos del inventario
class Status_inventari(models.Model):
    id_status = models.AutoField(primary_key = True)
    name_status = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name_status)

#tabla para el estado del lugar ya sea operando, bodega, prestado, mantenimiento   
class Place(models.Model):
    id_Place = models.AutoField(primary_key=True)
    name_place = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return str(self.name_place)

#tabla para el tipo de tecnologia, Monitor, portatil, CPU, tablets, etc
class Type_technologi(models.Model):
    idType_technologi = models.AutoField(primary_key = True)
    name_technologi = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name_technologi)

#tabla para las marcas de tecnologia
class Markes(models.Model):
    idMarke = models.AutoField(primary_key=True)
    name_marke =  models.CharField(max_length=100)
    def __str__(self):
        return str(self.name_marke)

#tabla para la informacion de elementos tecnologicos
class Tecnology(models.Model):
    idTecnology = models.AutoField(primary_key=True)
    idType_technologi = models.ForeignKey(Type_technologi, on_delete=models.CASCADE)
    caracteristics = models.TextField()
    idMarke = models.ForeignKey(Markes, on_delete=models.CASCADE)
    series_Manufactures =models.TextField()
    series_sena = models.TextField()
    idUbication = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    id_Place = models.ForeignKey(Place, on_delete=models.CASCADE)
    ID_status = models.ForeignKey(Status_inventari, on_delete=models.CASCADE, default=1)
    date_register = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.idTecnology)
    
#tabla para la informacion de otros elementos
class Material_Didactico(models.Model):
    idMaterial_didactico = models.AutoField(primary_key = True)
    name_material= models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    series_Manufactures =models.TextField()
    series_sena = models.TextField()
    idUbication = models.ForeignKey(Ubication, on_delete=models.CASCADE,default=6)
    id_Place = models.ForeignKey(Place, on_delete=models.CASCADE)
    ID_status = models.ForeignKey(Status_inventari, on_delete=models.CASCADE, default=1)
    date_creation = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.idMaterial_didactico)
    
#tabla para prestamos de tecnologia y material didactico
class Lend(models.Model):
    idLend = models.AutoField(primary_key=True)
    idTecnology = models.ForeignKey(Tecnology, on_delete=models.CASCADE, null=True)
    idMaterial_didactico = models.ForeignKey(Material_Didactico, on_delete=models.CASCADE, null=True)
    date_lend = models.DateTimeField(auto_now=True)
    observation = models.TextField()
    date_return = models.DateTimeField(null=True, default=None)
    def __str__(self):
        return str(self.idLend)
    

# /////////////////////////////////////////////// REPORTES ///////////////////////////////////////////////////////////////////////////

#tabla para los tipos de reportes: fallas en equipo, instalacion, bloqueos, etc

class Type_report(models.Model):
    id_type_report = models.AutoField(primary_key=True)
    name_type_report = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return str(self.name_type_report)

#tabla para el estado de los reportes: abierto, cerrado, en proceso
class Status_report(models.Model):
    id_status_report = models.AutoField(primary_key=True)
    name_status_report = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return str(self.name_status_report)
    
#prioridad del reporte: alta, media, baja
class Priority_report(models.Model):
    id_priority_report = models.AutoField(primary_key=True)
    name_priority_report = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return str(self.name_priority_report)
    
#tabla para el guardo de reportes de tecnologia y material didactico
class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_centro = models.ForeignKey(centro, on_delete=models.CASCADE)
    id_ubication = models.ForeignKey(Ubication, on_delete=models.CASCADE)
    idTecnology = models.ForeignKey(Tecnology, on_delete=models.CASCADE, null=True)
    idMaterial_didactico = models.ForeignKey(Material_Didactico, on_delete=models.CASCADE, null=True)
    id_status_report = models.ForeignKey(Status_report, on_delete=models.CASCADE)
    observation = models.TextField()
    id_priority_report = models.ForeignKey(Priority_report, on_delete=models.CASCADE)
    date_report = models.DateTimeField(auto_now=True)
    id_type_report = models.ForeignKey('Type_report', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id_report)