let dataTable;
let dataTableIsInitialized;



const dataTableOptions = {
    columnDefs: [
        {className: "centered", targets: [0,1] },
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

    await listacategorias();

    dataTable = $("#datatable-responsive").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};



const listacategorias=async()=>{
    try {
        const response =await fetch("http://127.0.0.1:8000/lista_categorias/")
        const data=await response.json();

        let content = ``;
        data.categorias.forEach((categoria) => {
            content += `
                <tr>
                    <td>${categoria.id_cat}</td>
                    <td>${categoria.nom_cat}</td>
                    <td class="centered">
                    <a href="modificarcategoria/${categoria.id_cat}" role="button" class="btn btn-primary text-light">Modificar</a>
                    <a class="btn btn-danger" href="#" onclick="removeCategoria(${categoria.id_cat})"><i class="fas fa-trash"></i></a> </td>
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


