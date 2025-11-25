// Abrimos la base de datos IndexedDB
let db;
let request = indexedDB.open("OfflineDB", 1);

request.onupgradeneeded = function(event) {
    db = event.target.result;
    db.createObjectStore("clientes", { keyPath: "id_cliente" });
    db.createObjectStore("facturas", { keyPath: "id_factura" });
    db.createObjectStore("tarifas", { keyPath: "id_tarifa" });
    db.createObjectStore("cargos", { keyPath: "id_cargo" });
    db.createObjectStore("subsidios", { keyPath: "id_subsidio" });
};


request.onsuccess = function(event) {
    db = event.target.result;
    document.getElementById('buscar').disabled = false;

    fetchData("clientes", "/api/clientes/");
    fetchData("tarifas", "/api/tarifas/");
    fetchData("cargos", "/api/cargos/");
    fetchData("subsidios", "/api/subsidios/");
};



request.onerror = function(event) {
    console.error("Error al abrir IndexedDB:", event.target.error);
};

function fetchData(storeName, apiUrl) {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            let transaction = db.transaction([storeName], "readwrite");
            let store = transaction.objectStore(storeName);

            data.forEach(item => store.put(item));

            transaction.oncomplete = () => {
                console.log(`${storeName} guardados en IndexedDB`);
            };

            transaction.onerror = (event) => {
                console.error(`Error al guardar ${storeName}:`, event.target.error);
            };
        })
        .catch(err => {
            console.log(`No hay conexión, usando datos offline para ${storeName}`);
        });
}







function guardarClienteOffline(cliente) {
    return new Promise((resolve, reject) => {
        // Forzar que el id_cliente sea número
        cliente.id_cliente = Number(cliente.id_cliente);

        const tx = db.transaction("clientes", "readwrite");
        const store = tx.objectStore("clientes");
        store.put(cliente);
        tx.oncomplete = () => {
            console.log("Cliente guardado offline:", cliente.id_cliente);
            resolve();
        };
        tx.onerror = (e) => reject(e);
    });
}


function guardarFacturasOffline(facturas) {
    return new Promise((resolve, reject) => {
        const tx = db.transaction("facturas", "readwrite");
        const store = tx.objectStore("facturas");
        facturas.forEach(f => store.put(f));
        tx.oncomplete = () => {
            console.log("Facturas guardadas offline:", facturas.length);
            resolve();
        };
        tx.onerror = (e) => reject(e);
    });
}


function obtenerClienteOffline(idCliente) {
    return new Promise(resolve => {
        const tx = db.transaction("clientes", "readonly");
        const store = tx.objectStore("clientes");

        // Forzar que la búsqueda sea con número
        const req = store.get(Number(idCliente));

        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null); // por si falla
    });
}


function obtenerFacturasOffline(idCliente) {
    return new Promise(resolve => {
        const tx = db.transaction("facturas", "readonly");
        const store = tx.objectStore("facturas");
        const req = store.getAll();
        req.onsuccess = () => {
            const facturasCliente = req.result.filter(f => f.id_cliente.toString() === idCliente.toString());
            resolve(facturasCliente);
        };
        req.onerror = () => resolve([]);
    });
}
