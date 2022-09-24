-- booksse pone en uso la base de datos
use flask_mysql_coding_dojo;

-- ejemplo de muchos a muchos db sql

-- tabla de autores
create table authors(
id int not null auto_increment primary key,
name varchar(100) not null,
created_at datetime,
updated_at datetime
);
-- tabla de libros
create table books(
id int not null auto_increment primary key,
title varchar(100) not null,
num_of_pages int not null,
created_at datetime,
updated_at datetime
);

-- tabla de asociacion o tabla pivote
create table favorites(
author_id int not null,
book_id int not null,
constraint pk_favorites primary key(author_id, book_id),
constraint fk_authors foreign key (author_id) references authors(id) on delete cascade on update cascade,
constraint fk_books foreign key (book_id) references books(id) on delete cascade on update cascade
);