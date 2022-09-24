
function updatePostName(id,elemento) {

    //button[del this] -> td[1] -> tr[del this] -> td[0] -> a[0]
    var hypervinculo = elemento.parentNode.parentNode.getElementsByTagName('td')[0].getElementsByTagName('a')[0];
    var name = hypervinculo.innerText;


    var name = prompt('Introduzca el nombre del Autor:',name);

        if(name != null && name != "")
        {
         if (confirm("Desea actualizar el nombre del Autor?")){

            var fecha = new Date()
            //se envia la informacion del prompt via ajax usando fetch
            //se arma una variable json
            let data = {
                "id": id,
                "name": name,
                "updated_at":fecha
            }
            //se ejecuta el fetch de tipo POST y la promesa
            fetch("/actualizarautor", {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body":  JSON.stringify(data),
           }).then(function(response){
                 return response.json()
             })
             .then(function(data){
                 hypervinculo.innerText = data['nombre_autor_json'];
                 return console.log(data);
             });
        }
    }
}