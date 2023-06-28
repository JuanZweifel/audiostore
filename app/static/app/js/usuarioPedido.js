let dataTable;
let dataTableIsInitialized;



const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0,1,2,3,4] },
        {orderable:false, targets:[4]},
        {searchable:false,targets:[]},
    ],
    pageLength: 4,
    destroy: true,
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    }
};


const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listaPedidos();

    dataTable = $("#datatable-responsive").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};



const listaPedidos=async()=>{
    try {
        const response =await fetch("http://127.0.0.1:8000/lista_pedidos_usuario")
        const data=await response.json();

        let content = ``;
        data.pedidos.forEach((pedido) => {
            content += `
                <tr>
                    <td>${pedido.id}</td>
                    <td>${pedido.producto}</td>
                    <td>${pedido.precio}</td>
                    <td>${pedido.cantidad}</td>
                    <td>${pedido.estado}</td>
                </tr>`;
        });
        table_body_pedidos.innerHTML = content;
        
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async()=>{
    await initDataTable();
});

