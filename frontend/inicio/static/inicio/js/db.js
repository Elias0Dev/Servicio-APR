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
};



request.onerror = function(event) {
    console.error("Error al abrir IndexedDB:", event.target.error);
};

function fetchData(storeName, apiUrl) {
    if (!navigator.onLine) {
        console.log(`Offline: no se puede refrescar ${storeName}`);
        return;
    }

    console.log(`🔄 Iniciando fetch para ${storeName} desde ${apiUrl}`);

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error(`Error al obtener ${storeName} del servidor`);
            return response.json();
        })
        .then(data => {
            if (!db) throw new Error("IndexedDB no inicializada");
            console.log(`📡 Datos recibidos del servidor para ${storeName}:`, data);

            const tx = db.transaction(storeName, "readwrite");
            const store = tx.objectStore(storeName);

            const idFieldMap = {
                "clientes": "id_cliente",
                "facturas": "id_factura",
                "tarifas": "id_tarifa",
                "cargos": "id_cargo",
                "subsidios": "id_subsidio"
            };

            const idField = idFieldMap[storeName];
            if (!idField) throw new Error(`StoreName inválido: ${storeName}`);

            const getAllRequest = store.getAll();
            getAllRequest.onsuccess = (event) => {
                const localData = event.target.result;
                console.log(`📂 Registros locales en ${storeName}:`, localData);

                const localIds = localData.map(item => item[idField]);
                const serverData = Array.isArray(data) ? data : [data]; // convierte objeto en array
                const serverIds = serverData.map(item => item[idField]);
                console.log(`IDs locales:`, localIds);
                console.log(`IDs del servidor:`, serverIds);

                // Borrar registros locales que no existen en el servidor
                const deletePromises = localIds
                    .filter(id => !serverIds.includes(id))
                    .map(id => new Promise((resolve, reject) => {
                        console.log(`🗑 Intentando borrar ID: ${id}`);
                        const delReq = store.delete(id);
                        delReq.onsuccess = () => {
                            console.log(`✅ Borrado ID: ${id}`);
                            resolve(id);
                        };
                        delReq.onerror = () => {
                            console.error(`❌ Error borrando ID: ${id}`);
                            reject(id);
                        };
                    }));

                // Insertar o actualizar registros del servidor
                const putPromises = serverData.map(item => new Promise((resolve, reject) => {
                    console.log(`💾 Insertando/actualizando ID: ${item[idField]}`);
                    const putReq = store.put(item);
                    putReq.onsuccess = () => {
                        console.log(`✅ Insertado/actualizado ID: ${item[idField]}`);
                        resolve(item[idField]);
                    };
                    putReq.onerror = () => {
                        console.error(`❌ Error insertando/actualizando ID: ${item[idField]}`);
                        reject(item[idField]);
                    };
                }));

                // Esperar a que todas las operaciones terminen
                Promise.all([...deletePromises, ...putPromises])
                    .then(() => console.log(`🎉 ${storeName} sincronizado correctamente`))
                    .catch(err => console.error(`❌ Error sincronizando ${storeName}:`, err));
            };

            getAllRequest.onerror = (event) => console.error(`❌ Error al obtener registros locales de ${storeName}:`, event.target.error);

            tx.oncomplete = () => console.log(`✅ Transacción finalizada para ${storeName}`);
            tx.onerror = (event) => console.error(`❌ Error en transacción de ${storeName}:`, event.target.error);
        })
        .catch(err => console.error(`❌ No se pudo sincronizar ${storeName}:`, err));
}











async function guardarClienteOffline(cliente) {
    return new Promise((resolve, reject) => {
        cliente.id_cliente = Number(cliente.id_cliente);

        const tx = db.transaction("clientes", "readwrite");
        const store = tx.objectStore("clientes");
        store.put(cliente);

        tx.oncomplete = async () => {
            console.log("Cliente guardado offline:", cliente.id_cliente);
            // 🔄 Sincronizar con el servidor solo este cliente
            await fetchData("clientes", `/api/clientes/${cliente.id_cliente}`);
            resolve();
        };
        tx.onerror = (e) => reject(e);
    });
}

async function guardarFacturasOffline(facturas) {
    return new Promise((resolve, reject) => {
        const tx = db.transaction("facturas", "readwrite");
        const store = tx.objectStore("facturas");
        facturas.forEach(f => store.put(f));

        tx.oncomplete = async () => {
            console.log("Facturas guardadas offline:", facturas.length);
            // 🔄 Sincronizar con el servidor solo estas facturas
            if (facturas.length > 0) {
                const idCliente = facturas[0].id_cliente;
                await fetchData("facturas", `/api/facturas/?id_cliente=${idCliente}`);
            }
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
