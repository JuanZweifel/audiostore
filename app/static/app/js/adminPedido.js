let dataTable;
let dataTableIsInitialized;



const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0,1,2,3] },
        {orderable:false, targets:[3]},
        {searchable:false,targets:[3]},
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
        const response =await fetch("http://127.0.0.1:8000/lista_pedidos")
        const data=await response.json();

        let content = ``;
        data.pedidos.forEach((pedido) => {
            content += `
                <tr>
                    <td>${pedido.id}</td>
                    <td>${pedido.usuario_id}</td>
                    <td>${pedido.estado}</td>
                    <td>
                    
                    <a class="btn btn-primary" href="#" onclick="updatePedido(${pedido.id})">Cambiar Estado</a>
                    <a class="btn btn-success" href="adminPedidoDetalle/${pedido.id}">Ver detalle</a>
                    <a class="btn btn-danger" href="#" onclick="removePedido(${pedido.id})"><i class="fas fa-trash"></i></a>
                    </td>
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


