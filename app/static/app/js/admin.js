document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("formulario").addEventListener('submit', validaciones);
});

function validaciones(evento) {
    evento.preventDefault();

    var inputTexto = document.getElementById("nombre");
    var regex = /^[A-Za-z\s]+$/; // Expresión regular para solo texto (mayúsculas, minúsculas y espacios)
    if (!regex.test(inputTexto.value)) {
        alert("El nombre solo debe tener letras");
        return;
    }

    var inputTexto = document.getElementById("marca");
    var regex = /^[A-Za-z\s]+$/;
    if (!regex.test(inputTexto.value)) {
        alert("La marca solo debe tener letras");
        return;
    }

    var inputTexto = document.getElementById("categoria");
    var regex = /^[A-Za-z\s]+$/;
    if (!regex.test(inputTexto.value)) {
        alert("La categoria solo debe tener letras");
        return;
    }
    //Validar rut

    this.submit();

}