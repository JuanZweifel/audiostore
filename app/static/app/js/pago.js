document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("formulario").addEventListener('submit', validaciones);
});

function validaciones(evento) {
    evento.preventDefault();

    var inputTexto = document.getElementById("fname");
    var regex = /^[A-Za-z\s]+$/; // Expresión regular para solo texto (mayúsculas, minúsculas y espacios)
    if (!regex.test(inputTexto.value)) {
        alert("El nombre solo debe tener letras");
        return;
    }

    var inputTexto = document.getElementById("lname");
    var regex = /^[A-Za-z\s]+$/;
    if (!regex.test(inputTexto.value)) {
        alert("El apellido solo debe tener letras");
        return;
    }


    this.submit();

}