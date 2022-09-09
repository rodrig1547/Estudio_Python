class Producto:
    def __init__(self, codigo, nombre, precio):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self,valor):
        self.__codigo = valor


    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor
         
    @property
    def precio(self):
        return self.__precio

    @codigo.setter
    def precio(self, valor):
        self.__precio = valor

    def __str__(self): ##Para Mostrar en un print lo siguiente.
        return 'Codigo' + str(self.__codigo) + ',nombre'+str() + str(self.__nombre) + ' ,precio' + str(self.__precio)

p1 = Producto(1 , 'Producto 2', 5)
p2 = Producto(2 , 'Producto 3', 5)
p3 = Producto(3 , 'Producto 4', 5)

print (p1)
print (p2)
print (p3)


