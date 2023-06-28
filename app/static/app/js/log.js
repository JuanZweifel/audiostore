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

    var inputTexto = document.getElementById("apellido");
    var regex = /^[A-Za-z\s]+$/;
    if (!regex.test(inputTexto.value)) {
        alert("El apellido solo debe tener letras");
        return;
    }

    //Validar rut
    var rut = document.getElementById('rut').value;
    if (!/^[0-9]+-[0-9kK]{1}$/.test(rut)) {
        alert('Por favor ingrese un Rut válido.');
        return false;
    }
    var rutSinGuion = rut.replace('-', '');
    var rutNumeros = parseInt(rutSinGuion.slice(0, -1));
    var rutDigitoVerificador = rutSinGuion.slice(-1).toUpperCase();
    var m = 0;
    var s = 1;
    for (; rutNumeros; rutNumeros = Math.floor(rutNumeros / 10)) {
        s = (s + rutNumeros % 10 * (9 - m++ % 6)) % 11;
    }
    var digitoVerificadorCalculado = (s ? s - 1 : 'K');
    if (rutDigitoVerificador !== digitoVerificadorCalculado.toString()) {
        alert('Por favor ingrese un Rut válido.');
        return false;
    }

    this.submit();

}