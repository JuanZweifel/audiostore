let dataTable;
let dataTableIsInitialized;



const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0,1,2,3,4,5,6] },
        {orderable:false, targets:[2,3,6]},
        {searchable:false,targets:[2,3,6]},
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

    await listaproductos();

    dataTable = $("#datatable-responsive").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};



const listaproductos=async()=>{
    try {
        const response =await fetch("http://127.0.0.1:8000/lista_productos/")
        const data=await response.json();

        let content = ``;
        data.productos.forEach((producto) => {
            content += `
                <tr>
                    <td>${producto.id_producto}</td>
                    <td>${producto.nom_producto}</td>
                    <td>${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.categoria_id}</td>
                    <td>${producto.marca_id}</td>
                    <td>
                    <a href="modificarproducto/${producto.id_producto}" role="button" class="btn btn-primary text-light">Modificar</a>
                    <a href="eliminarproducto/${producto.id_producto}" role="button" class="btn btn-danger text-light">Eliminar</a> </td>
                    </td>
                </tr>`;
        });
        table_body_clientes.innerHTML = content;
        
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async()=>{
    await initDataTable();
});


