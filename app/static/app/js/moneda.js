
function dolar(res) {

    $.getJSON('https://mindicador.cl/api', function (data) {
        let dolar;
        dolar = data.dolar.valor;

        // let casilla = parseInt(document.getElementById("precio").textContent);
        resul = (parseInt(res) / dolar).toFixed(2);

        $("#precio").text('$' + resul)

    }).fail(function () {
        console.log('Error al consumir la API!');
    });
}


function euro() {
    $.getJSON('https://mindicador.cl/api', function (data) {
        let euro;
        euro = data.euro.valor;

        // let casilla = parseInt(document.getElementById("precio").textContent);
        resul = (parseInt(res) / euro).toFixed(2);

        $("#precio").text('€' + resul)

    }).fail(function () {
        console.log('Error al consumir la API!');
    });
}

function bitcoin() {
    $.getJSON('https://mindicador.cl/api', function (data) {
        let bit;
        bit = data.bitcoin.valor;

        // let casilla = parseInt(document.getElementById("precio").textContent);
        resul = (parseInt(res) / bit).toFixed(2);

        $("#precio").text('₿ ' + resul)

    }).fail(function () {
        console.log('Error al consumir la API!');
    });
}

function clp(peso){
    $("#precio").text(peso)
}

