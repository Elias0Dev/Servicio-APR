document.getElementById('buscar').addEventListener('click', function() {
    const numeroCliente = document.getElementById('cliente').value.trim();
    if (!numeroCliente) {
        alert('Por favor, ingresa un número de cliente.');
        return;
    }

    fetch(`/inicio/api/facturas/?numero_cliente=${numeroCliente}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const facturas = data.facturas;
            const resultadosDiv = document.getElementById('resultados');
            const cuerpoTabla = document.getElementById('cuerpo-tabla');
            cuerpoTabla.innerHTML = ''; // Limpiar tabla anterior

            facturas.forEach((boleta, index) => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${boleta.consumido}</td>
                    <td>${boleta.fecha}</td>
                    <td>${boleta.valor}</td>
                    <td><button onclick="descargarBoleta(${index}, '${boleta.consumido}', '${boleta.fecha}', '${boleta.valor}')">Descargar</button></td>
                `;
                cuerpoTabla.appendChild(fila);
            });

            resultadosDiv.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al buscar las facturas.');
        });
});

// Función para descargar boleta con datos reales
function descargarBoleta(index, consumido, fecha, valor) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text(`Detalle de Boleta ${index + 1}`, 10, 10);
    doc.text(`Lo Consumido: ${consumido}`, 10, 30);
    doc.text(`Fecha: ${fecha}`, 10, 40);
    doc.text(`Valor: ${valor}`, 10, 50);
    
    doc.save(`boleta_${index + 1}.pdf`);
}
