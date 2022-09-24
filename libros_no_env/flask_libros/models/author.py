from flask_libros.config.mysqlconnection import connectToMySQL
from flask_libros.models import book
#se hace referencia al archivo para evitar el error de referencia circular

# modelar la clase después de la tabla authors de nuestra base de datos
class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #esta propiedad va a contener una lista los libros favoritos de cada autor
        self.favorites_books = []

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de authors
        authors = []
        # Iterar sobre los resultados de la base de datos y crear instancias de authors con cls
        for author in results:
            authors.append( cls(author) )
        return authors

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,id):
        #armar la consulta con cadenas f
        query = f"SELECT * FROM authors where id = %(id)s;"
        #armar el diccionario data con solo el campo id
        data = { 'id' : id }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        #devolver el primer registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None




    @classmethod
    def save(cls, data):
        query = f"INSERT INTO authors (name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        # data es un diccionario que se pasará al método de guardar desde server.py
        author_id = connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )
        return author_id



    @classmethod
    def update(cls, data):
        query = f"UPDATE authors SET name = %(name)s , updated_at = NOW() WHERE id = %(id)s;"
        resultado = connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )
        result = None
        if resultado == None:
            result = cls.get_by_id(data['id'])
        # data es un diccionario que se pasará al método de guardar desde server.py
        return result


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM authors WHERE id = %(id)s;"
        data = {'id': id}

        print("ejecutando consulta de borrado",end='\n\n')
        print(query)

        resultado = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)

        return resultado

    @classmethod
    def get_books_with_authors( cls , data ):
        query = "SELECT * FROM authors a LEFT JOIN favorites f ON a.id = f.author_id LEFT JOIN books b ON f.book_id = b.id WHERE a.id = %(author_id)s;"
        results = connectToMySQL('flask_mysql_coding_dojo').query_db( query , data )
        
        # los resultados serán una lista de objetos books (libros) que se adjunta a cada fila
        author = cls( results[0] )

        for row_from_db in results:
            # ahora parseamos los datos books para crear instancias de libros y agregarlas a nuestra lista
           book_data = {
               "id" : row_from_db["b.id"],
               "title" : row_from_db["title"],
               "num_of_pages" : row_from_db["num_of_pages"],
               "created_at" : row_from_db["b.created_at"],
               "updated_at" : row_from_db["b.updated_at"]
           }

           author.favorites_books.append( book.Book( book_data ) )

        return author