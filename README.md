# Libros_noenv


Este proyecto no ha uso de archivo .env

Hace uso de fetch para la modificacion del nombre del autor

Hace uso de mvc

Hace uso de una relacion de base de datos de muchos a muchos en los archivos de modelos de clase python

se emplean 3 clases: books, authors y favorites

las clases books y authors se enlazan por archivo para evitar error de referencia circular entre importaciones

tanto la clase author como books tienen un atributo que almacena una lista de objetos de la otra clase segun se consulte, cumpliendo la relacion de muchos a muchos

En la carpeta static/db estan los archivos de base de datos
