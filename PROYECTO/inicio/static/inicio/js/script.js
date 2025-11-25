function descargarBoleta(idFactura) {
    window.open(`/detalle_boletas/facturas/pdf/${idFactura}/`, '_blank');
}
function mostrarDatos(cliente, facturasCliente) {
    const resultadosContainer = document.getElementById('resultados');
    const cuerpoTabla = document.getElementById('cuerpo-tabla');
    const errorMessage = document.getElementById('error-message');
    const graficoContainer = document.getElementById('grafico-consumo-container');
    const nombreClienteDisplay = document.getElementById('nombre-cliente-display');

    // Reset visual
    resultadosContainer.classList.add('hidden');
    graficoContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');
    cuerpoTabla.innerHTML = '';

    if (!cliente || facturasCliente.length === 0) {
        errorMessage.textContent = "No hay datos para mostrar.";
        errorMessage.classList.remove("hidden");
        return;
    }

    // Mostrar nombre del cliente
    nombreClienteDisplay.textContent = `Historial de: ${cliente.nombre}`;

    // Ordenar facturas por fecha descendente
    facturasCliente.sort((a, b) => new Date(b.fecha_emision) - new Date(a.fecha_emision));

    // Mostrar tabla
    facturasCliente.forEach(f => {
        let row = cuerpoTabla.insertRow();
        row.innerHTML = `
            <td>${f.consumo}</td>
            <td>${new Date(f.fecha_emision).toLocaleDateString('es-CL')}</td>
            <td>$${Number(f.total_pagar).toLocaleString('es-CL')}</td>
            <td>
                <a href="/generar_boleta/${f.id_factura}/pdf/" target="_blank" class="btn btn-sm btn-outline-primary">Ver Boleta</a>
            </td>
        `;
    });
    resultadosContainer.classList.remove('hidden');

    // Mostrar gráfico de consumo (solo la factura más reciente)
    const facturaReciente = facturasCliente[0];
    const LIMITE_MENSUAL = 35;
    const porcentaje = Math.round((facturaReciente.consumo / LIMITE_MENSUAL) * 100);
    const fecha = new Date(facturaReciente.fecha_emision);
    const periodo = fecha.toLocaleDateString('es-CL', { month: 'long', year: 'numeric' });

    document.getElementById('consumo-periodo').textContent = `Consumo de Agua - ${periodo.charAt(0).toUpperCase() + periodo.slice(1)}`;
    document.getElementById('consumo-valor').textContent = `${facturaReciente.consumo} m³`;
    document.getElementById('consumo-limite').textContent = `de ${LIMITE_MENSUAL} m³ disponibles como límite de referencia`;

    const barra = document.getElementById('progreso-barra');
    barra.style.width = `${Math.min(porcentaje, 100)}%`;
    barra.setAttribute('aria-valuenow', porcentaje);
    document.getElementById('progreso-porcentaje').textContent = `${porcentaje}%`;

    graficoContainer.classList.remove('hidden');
}



async function buscarFacturasJS(numeroCliente) {
    const resultadosContainer = document.getElementById('resultados');
    const cuerpoTabla = document.getElementById('cuerpo-tabla');
    const errorMessage = document.getElementById('error-message');
    const graficoContainer = document.getElementById('grafico-consumo-container');
    const nombreClienteDisplay = document.getElementById('nombre-cliente-display');

    // Reset visual
    resultadosContainer.classList.add('hidden');
    graficoContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');
    cuerpoTabla.innerHTML = '';

    if (!numeroCliente) {
        errorMessage.textContent = 'Por favor, ingrese un número de cliente.';
        errorMessage.classList.remove('hidden');
        return;
    }

    // Si estamos offline, usamos IndexedDB directamente
    if (!navigator.onLine) {
        console.warn("Modo offline — usando datos guardados");

        const cliente = await obtenerClienteOffline(numeroCliente);
        console.log("Cliente offline:", cliente);

        const facturasCliente = await obtenerFacturasOffline(numeroCliente);
        console.log("Facturas offline:", facturasCliente);

        if (!cliente || facturasCliente.length === 0) {
            errorMessage.textContent = "No hay datos guardados para este cliente.";
            errorMessage.classList.remove("hidden");
            return;
        }

        return mostrarDatos(cliente, facturasCliente);
    }

    // Si estamos online, intentamos fetch dentro de try/catch
    try {
        // Buscar cliente
        const responseCliente = await fetch(`/api/clientes/${numeroCliente}`);
        if (!responseCliente.ok) throw new Error("Cliente no encontrado");
        const clienteData = await responseCliente.json();

        if (!clienteData || !clienteData.nombre) throw new Error("Cliente inválido");

        const cliente = clienteData;

        // Guardar cliente offline
        await guardarClienteOffline(cliente);

        // Obtener facturas del cliente
        const responseFacturas = await fetch(`/api/facturas/?id_cliente=${numeroCliente}`);
        if (!responseFacturas.ok) throw new Error("Facturas no encontradas");
        const facturasCliente = await responseFacturas.json();

        // Guardar facturas offline
        await guardarFacturasOffline(facturasCliente);

        return mostrarDatos(cliente, facturasCliente);

    } catch (err) {
        console.warn("Fetch online falló, usando datos offline si existen:", err);

        // Fallback a datos offline
        const cliente = await obtenerClienteOffline(numeroCliente);
        const facturasCliente = await obtenerFacturasOffline(numeroCliente);

        if (!cliente || facturasCliente.length === 0) {
            errorMessage.textContent = "No hay datos guardados para este cliente.";
            errorMessage.classList.remove("hidden");
            return;
        }

        return mostrarDatos(cliente, facturasCliente);
    }
}


// Evento del botón
document.addEventListener('DOMContentLoaded', () => {
    const buscarBtn = document.getElementById('buscar');
    buscarBtn?.addEventListener('click', () => {
        const numeroCliente = document.getElementById('cliente').value;
        buscarFacturasJS(numeroCliente);
    });
});