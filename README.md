# makersCoderbyte
API repositorio.
Option B

El api quedó creada con todos los requerimientos pedidos, para ponerla a correr solamente toca ejecutar el programa main.py
El api cuenta con una base de datos de más de 100 imagenes cada una con los campos "explanation", "hdurl", "title" y "url".

Se crearon los siguientes endpoints:

Para método DELETE:
http://127.0.0.1:5000//delete_photo/idfoto
ejemplo:
http://127.0.0.1:5000//delete_photo/1

Para el método POST
http://127.0.0.1:5000//put_photo_create/id_photo
ejemplo
http://127.0.0.1:5000//put_photo_create/1
se debe pasar el cuerpo de la petición de la siguiente forma:
{
    "explanation": "Ejemplo",
    "hdurl": "Ejemplo",
    "title": "Ejemplo",
    "url": "Ejemplo"
}
Para el método PUT
En el api se usó el método PUT para crear elementos, usando el api de la nasa directamente, en este caso, no toca pasar cuerpo en la petición, únicamente toca decir el id que desea para la foto y la fecha de la foto, el método se encargará de realizar las peticiones necesarias al api de la nasa y obtener y guardar la foto de la fecha especificada: 
http://127.0.0.1:5000//put_photo/id_photo/fecha
ejemplo
http://127.0.0.1:5000//put_photo/1/2020-11-12
Para el método PATCH se modifican los valores de las fotos, simplemente se pasan por el cuerpo de la petición los valores que desean modificarse y el id de la foto que desea modificarse.
http://127.0.0.1:5000//update_photo/id_photo
ejemplo:
http://127.0.0.1:5000//update_photo/1
{
        "explanation": "Ejemplo"
}
Finalmente el método GET se divide en 2 partes, la primera es un GET individual, donde se tiene por respuesta únicamente la foto solicitada mediante su id_photo
http://127.0.0.1:5000//get_photo/id_photo
ejemplo
http://127.0.0.1:5000//get_photo/1
Por otro lado, para obtener varios elementos se tienen varias opciones, si se desea obtener todos los elementos de la base de datos, el funcionamiento es igual a obtener solo un elemento, pero se debe usar el id_photo en 0
http://127.0.0.1:5000//get_photo/0
de esta forma, el api retornará todas las fotos de base de datos, el id=0 está reservado para esta función y ningún otro método puede acceder,crear,modificar o eliminar usando el id=0.
Finalmente, debido a que este es el único método de devuelve una lista de elementos, también tiene la función de filtrado y de paginación.
Para poder usar el filtrado se tienen 2 parámetros adicionales:
filter=acá se pone el valor del atributo sobre el cual se quiere hacer una filtración, puede ser cualquiera de estos:"explanation", "hdurl", "title", "url", "id" 
filter_value=se pone el valor que se desea que tenga el atributo previamente definido, por ejemplo podemos poner
filter=explanation
filter_value=Marte
y el api buscará todos los registros que tengan en su explicación la palabra Marte y únicamente retornará esos.
http://127.0.0.1:5000//get_photo/0?filter=ATRIBUTE&filter_value=VALUE
ejemplo
http://127.0.0.1:5000//get_photo/0?filter=explanation&filter_value=Orion

Por último de la paginación, se debe agregar el parámetro limit que define la cantidad maxima de recursos que se deben retornar, por ejemplo
limit=5
de esta forma puedo acceder a todos los registros y pedir que solo me retorne el número que el usuario desee:
http://127.0.0.1:5000//get_photo/0?&limit=numero
ejemplo
http://127.0.0.1:5000//get_photo/0?&limit=5
acá solo se retornarán 5 registros.
También se pueden combinar las filtraciones con la paginación:

ejemplo
http://127.0.0.1:5000//get_photo/0?filter=explanation&filter_value=Orion&limit=5

De esta forma, cumpliendo con todos los requisitos del reto, muchas gracias.
