from flask_libros.config.mysqlconnection import connectToMySQL
from flask_libros.models import author
#se hace referencia al archivo para evitar el error de referencia circular

# modelar la clase después de la tabla Books de nuestra base de datos
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #esta propiedad va a contener una lista los authors que les gusta o tinene como favorito el libro
        self.favorites_authors = []

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de usuarioscr
        books = []
        # Iterar sobre los resultados de la base de datos y crear instancias de dojos con cls
        for book in results:
            books.append( cls(book) )
        return books

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,id):
        #armar la consulta con cadenas f
        query = f"SELECT * FROM books where id = %(id)s;"
        #armar el diccionario data con solo el campo id
        data = { 'id' : id }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        #devolver el primerl registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None


    @classmethod
    def save(cls, data):
        query = f"INSERT INTO books (title , num_of_pages, created_at, updated_at) VALUES ( %(title)s , %(num_of_pages)s , NOW() , NOW() );"
        # data es un diccionario que se pasará al método de guardar desde server.py
        book_id = connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )
        return book_id



    @classmethod
    def update(cls, data):
        query = f"UPDATE books SET title = %(title)s , num_of_pages = %(num_of_pages)s, updated_at = NOW() WHERE id = %(id)s;"
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM books WHERE id = %(id)s;"

        data = {'id': id}

        resultado = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)

        return resultado


    @classmethod
    def get_authors_with_books( cls , data ):
        query = "SELECT * FROM books b LEFT JOIN favorites f ON b.id = f.book_id LEFT JOIN authors a ON f.author_id = a.id WHERE b.id = %(book_id)s;"
        results = connectToMySQL('flask_mysql_coding_dojo').query_db( query , data )
        # los resultados serán una lista de objetos authors (autores) que se adjunta a cada fila
        book = cls( results[0] )

        for row_from_db in results:
            # ahora parseamos los datos books para crear instancias de libros y agregarlas a nuestra lista
           author_data = {
               "id" : row_from_db["a.id"],
               "name" : row_from_db["name"],
               "created_at" : row_from_db["a.created_at"],
               "updated_at" : row_from_db["a.updated_at"]
           }
           book.favorites_authors.append( author.Author( author_data ) )
        return book