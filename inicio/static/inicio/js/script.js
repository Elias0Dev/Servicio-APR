function descargarBoleta(idFactura) {
    window.open(`/api/facturas/pdf/${idFactura}/`, '_blank');
}



document.getElementById("buscar").addEventListener("click", function () {
  const numeroCliente = document.getElementById("cliente").value.trim();
  if (!numeroCliente) {
    alert("Por favor, ingresa un número de cliente.");
    return;
  }

  fetch(`/api/facturas/?numero_cliente=${numeroCliente}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }

      const facturas = data.facturas;
      const resultadosDiv = document.getElementById("resultados");
      const cuerpoTabla = document.getElementById("cuerpo-tabla");
      cuerpoTabla.innerHTML = ""; // Limpiar tabla anterior

      facturas.forEach((boleta, index) => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
                    <td>${boleta.fecha}</td>
                    <td>${boleta.consumido}</td>
                    <td>${boleta.valor}</td>
                    
                `;
        cuerpoTabla.appendChild(fila);
      });

      resultadosDiv.classList.remove("hidden");
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Ocurrió un error al buscar las facturas.");
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const boton = document.getElementById('btn_buscar');
    const seccion = document.getElementById('buscar_rut');

    boton.addEventListener('click', function() {
      seccion.style.display.none();
    });
  });