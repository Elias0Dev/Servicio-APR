function descargarBoleta(idFactura) {
    window.open(`/api/facturas/pdf/${idFactura}/`, '_blank');
}



document.addEventListener('DOMContentLoaded', function() {
    const buscarBtn = document.getElementById('buscar');
    if(buscarBtn) {
        buscarBtn.addEventListener('click', fetchFacturas);
    }
});

function fetchFacturas() {
    const numeroCliente = document.getElementById('cliente').value;
    const resultadosContainer = document.getElementById('resultados');
    const cuerpoTabla = document.getElementById('cuerpo-tabla');
    const errorMessage = document.getElementById('error-message');
    const graficoContainer = document.getElementById('grafico-consumo-container');
        const nombreClienteDisplay = document.getElementById('nombre-cliente-display');

    // Ocultar todo antes de la nueva búsqueda
    resultadosContainer.classList.add('hidden');
    graficoContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');
    cuerpoTabla.innerHTML = '';

    if (!numeroCliente) {
      errorMessage.textContent = 'Por favor, ingrese un número de cliente.';
      errorMessage.classList.remove('hidden');
      return;
    }

    fetch(`/buscar_facturas/?numero_cliente=${numeroCliente}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Cliente no encontrado o error en la solicitud.');
        }
        return response.json();
      })
      .then(data => {
        if (data.error) {
          throw new Error(data.error);
        }
        if (data.nombre_cliente) {
            nombreClienteDisplay.textContent = `Historial de: ${data.nombre_cliente}`;
        }
        // --- LÓGICA PARA EL NUEVO GRÁFICO ---
        if (data.consumo_reciente) {
          const consumo = data.consumo_reciente;
          document.getElementById('consumo-periodo').textContent = `Consumo de Agua - ${consumo.periodo}`;
          document.getElementById('consumo-valor').innerHTML = `${consumo.consumo} m³`;
          document.getElementById('consumo-limite').textContent = `de ${consumo.limite} m³ disponibles como límite de referencia`;
          
          const barra = document.getElementById('progreso-barra');
          barra.style.width = `${consumo.porcentaje}%`;
          barra.setAttribute('aria-valuenow', consumo.porcentaje);
          
          document.getElementById('progreso-porcentaje').textContent = `${consumo.porcentaje}%`;
          
          graficoContainer.classList.remove('hidden');
        } else {
          graficoContainer.classList.add('hidden');
        }
        // --- FIN DE LA LÓGICA DEL GRÁFICO ---

        // Lógica para la tabla de historial
        if (data.facturas && data.facturas.length > 0) {
          data.facturas.forEach(factura => {
            let row = cuerpoTabla.insertRow();
            row.innerHTML = `
              <td>${factura.consumido}</td>
              <td>${factura.fecha}</td>
              <td>${factura.valor}</td>
              <td>
                <a href="/generar_boleta/${factura.id}/pdf/" target="_blank" class="btn btn-sm btn-outline-primary">Ver Boleta</a>
              </td>
            `;
          });
          resultadosContainer.classList.remove('hidden');
        } else {
          errorMessage.textContent = 'No se encontraron boletas para este número de cliente.';
          errorMessage.classList.remove('hidden');
        }
      })
      .catch(error => {
        errorMessage.textContent = error.message;
        errorMessage.classList.remove('hidden');
      });
}

document.addEventListener('DOMContentLoaded', function() {
    const boton = document.getElementById('btn_buscar');
    const seccion = document.getElementById('buscar_rut');

    boton.addEventListener('click', function() {
      seccion.style.display.none();
    });
  });