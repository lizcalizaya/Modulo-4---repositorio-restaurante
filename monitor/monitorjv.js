// 🔄 Botón "Actualizar"
document.addEventListener("DOMContentLoaded", () => {
  const btnActualizar = document.getElementById("btn-actualizar");
  if (btnActualizar) {
    btnActualizar.addEventListener("click", () => {
      location.reload(); 
    });
  }

  // Filtros_por_estado
  const botones = document.querySelectorAll(".barra-estados button[data-filtro]");
  const tarjetas = document.querySelectorAll(".tarjeta");

  botones.forEach(boton => {
    boton.addEventListener("click", () => {
      const filtro = boton.getAttribute("data-filtro");

      tarjetas.forEach(tarjeta => {
        const estado = tarjeta.getAttribute("data-estado");
        if (filtro === "todos" || estado === filtro) {
          tarjeta.style.display = "flex";
        } else {
          tarjeta.style.display = "none";
        }
      });
    });
  });
});
