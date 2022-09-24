#la idea de esta clase es poder grabar los favoritos
from flask_libros.config.mysqlconnection import connectToMySQL

# modelar la clase después de la tabla authors de nuestra base de datos
class Favorite:
    def __init__( self , data ):
        self.id = data['author_id']
        self.name = data['book_id']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query)
        # crear una lista vacía para agregar nuestras instancias de authors
        favorites = []
        # Iterar sobre los resultados de la base de datos y crear instancias de authors con cls
        for favorite in results:
            favorites.append( cls(favorite) )
        return favorites

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,author_id,book_id):
        #armar la consulta con cadenas f
        query = f"SELECT * FROM favorites where author_id = %(author_id)s and book_id = %(book_id)s;"
        #armar el diccionario data con solo el campo id
        data = {
                'author_id' : author_id ,
                'book_id' : book_id
                }
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)
        #devolver el primerl registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None




    @classmethod
    def save(cls, data):
        query = f"INSERT INTO favorites (author_id , book_id ) VALUES ( %(author_id)s, %(book_id)s );"
        # data es un diccionario que se pasará al método de guardar desde server.py
        author_id = connectToMySQL('flask_mysql_coding_dojo').query_db( query, data )
        return data


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM favorites WHERE author_id = %(author_id)s and book_id = %(book_id)s;"

        resultado = connectToMySQL('flask_mysql_coding_dojo').query_db(query, data)

        return resultado

