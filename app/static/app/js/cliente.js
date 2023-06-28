let dataTable;
let dataTableIsInitialized;



const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0,1,2,3,4,5,6] },
        {orderable:false, targets:[6]},
        {searchable:false,targets:[1,6]},
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

    await listaclientes();

    dataTable = $("#datatable-responsive").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};



const listaclientes=async()=>{
    try {
        const response =await fetch("http://127.0.0.1:8000/lista_clientes/")
        const data=await response.json();

        let content = ``;
        data.clientes.forEach((cliente) => {
            content += `
                <tr>
                    <td>${cliente.run}</td>
                    <td>${cliente.primer_nombre}</td>
                    <td>${cliente.segundo_nombre}</td>
                    <td>${cliente.apellido_paterno}</td>
                    <td>${cliente.apellido_materno}</td>
                    <td>${cliente.correo}</td>
                    <td>
                    <a href="modificar_cliente/ ${cliente.run}" role="button" class="btn btn-primary text-light">Modificar</a>
                    <a href="eliminar_cliente/ ${cliente.run}" role="button" class="btn btn-danger text-light">Eliminar</a> </td>
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
