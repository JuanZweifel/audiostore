document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("formulario").addEventListener('submit', validaciones);
});

function validaciones(evento) {
    evento.preventDefault();

    //Validar rut
    var rut = document.getElementById('id_run').value;
    if (!/^[0-9]+-[0-9kK]{1}$/.test(rut)) {
        Swal.fire({
            "title":"Error!!!",
            "text":"El run ingresado no es valido",
            "icon":"error",
    })
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
        Swal.fire({
                "title":"Error!!!",
                "text":"El run ingresado no es valido",
                "icon":"error",
        })
        return false;
    }

    this.submit();

}