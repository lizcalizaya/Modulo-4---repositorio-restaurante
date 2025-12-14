// ============================
// Monitor de Pedidos - Frontend
// ============================

let temporizadoresUrgencia = {};

// --------- Utilidades ---------

function estadoLegible(estadoBackend) {
  switch (estadoBackend) {
    case "CREADO":
      return "Nuevo";
    case "EN_PREPARACION":
      return "En preparación";
    case "LISTO":
      return "Listo";
    case "ENTREGADO":
      return "Entregado";
    case "URGENTE":
      return "Urgente";
    default:
      return estadoBackend;
  }
}

function colorTarjeta(estadoUI) {
  switch (estadoUI) {
    case "En preparación":
      return "naranja";
    case "Listo":
      return "verde";
    case "Entregado":
      return "azul";
    case "Urgente":
      return "rojo";
    default:
      return "gris";
  }
}

function formatearHora(fechaISO) {
  if (!fechaISO) return "--:--";
  const f = new Date(fechaISO);
  if (isNaN(f)) return "--:--";
  return f.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function calcularTiempo(fechaInicioISO, fechaFinISO) {
  const inicio = new Date(fechaInicioISO);
  const fin = fechaFinISO ? new Date(fechaFinISO) : new Date();
  if (isNaN(inicio) || isNaN(fin)) return "";
  const diffMs = fin - inicio;
  const totalSeg = Math.floor(diffMs / 1000);
  const min = Math.floor(totalSeg / 60);
  const seg = totalSeg % 60;
  return `${min} min ${seg} s`;
}

// --------- Contadores de estados ---------

function actualizarContadores(pedidos) {
  const totales = {
    todos: pedidos.length,
    enPreparacion: 0,
    listo: 0,
    entregado: 0,
    urgente: 0,
  };

  pedidos.forEach((p) => {
    switch (p.estado) {
      case "EN_PREPARACION":
        totales.enPreparacion++;
        break;
      case "LISTO":
        totales.listo++;
        break;
      case "ENTREGADO":
        totales.entregado++;
        break;
      case "URGENTE":
        totales.urgente++;
        break;
    }
  });

  const elTodos = document.getElementById("filtro-todos");
  const elPrep = document.getElementById("filtro-preparacion");
  const elListo = document.getElementById("filtro-listo");
  const elEnt = document.getElementById("filtro-entregado");
  const elUrg = document.getElementById("filtro-urgente");

  if (elTodos) elTodos.textContent = `Todos (${totales.todos})`;
  if (elPrep) elPrep.textContent = `En preparación (${totales.enPreparacion})`;
  if (elListo) elListo.textContent = `Listo (${totales.listo})`;
  if (elEnt) elEnt.textContent = `Entregado (${totales.entregado})`;
  if (elUrg) elUrg.textContent = `Urgente (${totales.urgente})`;
}

// --------- Notificación cuando pasa a LISTO ---------

function mostrarNotificacion(id, mesa, descripcion) {
  const cont = document.getElementById("notificaciones");
  if (!cont) return;

  const caja = document.createElement("div");
  caja.className = "notificacion";

  caja.innerHTML = `
    <button class="boton-cerrar">&times;</button>
    <strong>La orden con ID: ${id} para la mesa Nº${mesa} se encuentra lista para ser entregada.</strong>
    <p>Detalle: "${descripcion || "Sin descripción"}"</p>
  `;

  const btnCerrar = caja.querySelector(".boton-cerrar");
  btnCerrar.onclick = () => cont.removeChild(caja);

  cont.appendChild(caja);

  setTimeout(() => {
    if (cont.contains(caja)) cont.removeChild(caja);
  }, 7000);
}

// --------- Modal de detalle ---------

async function mostrarDetalleEnModal(id) {
  try {
    const res = await fetch(`/api/pedidos/${id}/`);
    if (!res.ok) throw new Error("Error HTTP " + res.status);
    const p = await res.json();

    const horaIngreso = p.fecha_creacion
      ? new Date(p.fecha_creacion).toLocaleString()
      : "Sin dato";

    const horaSalida =
      p.estado === "ENTREGADO" && p.fecha_actualizacion
        ? new Date(p.fecha_actualizacion).toLocaleString()
        : "Pendiente";

    const tiempoCocina = calcularTiempo(p.fecha_creacion, p.fecha_actualizacion);

    const body = document.getElementById("modal-detalle-body");
    if (!body) return;

    body.innerHTML = `
      <h2>Detalle del Pedido</h2>
      <p><strong>ID de pedido:</strong> ${p.id}</p>
      <p><strong>Número de pedido:</strong> ${p.id}</p>
      <p><strong>Mesa:</strong> ${p.mesa}</p>
      <p><strong>Nombre de cliente:</strong> ${p.cliente || "Sin nombre"}</p>
      <p><strong>Orden:</strong> ${p.descripcion || "Sin descripción"}</p>
      <p><strong>Estado actual:</strong> ${estadoLegible(p.estado)}</p>
      <p><strong>Hora de ingreso:</strong> ${horaIngreso}</p>
      <p><strong>Tiempo en cocina:</strong> ${tiempoCocina}</p>
      <p><strong>Hora de salida:</strong> ${horaSalida}</p>
    `;

    const modal = document.getElementById("modal-detalle");
    if (modal) modal.classList.add("activo");
  } catch (e) {
    console.error("Error cargando detalle:", e);
  }
}

function configurarCierreModal() {
  const modal = document.getElementById("modal-detalle");
  const btnCerrar = modal ? modal.querySelector(".modal-cerrar") : null;

  if (!modal || !btnCerrar) return;

  btnCerrar.onclick = () => modal.classList.remove("activo");

  modal.onclick = (e) => {
    if (e.target === modal) modal.classList.remove("activo");
  };
}

// --------- Carga principal de pedidos ---------

async function cargarPedidos() {
  const contenedor = document.getElementById("contenedor-pedidos");
  if (!contenedor) return;

  contenedor.innerHTML = "";

  try {
    const res = await fetch("/api/pedidos/");
    const pedidos = await res.json();

    actualizarContadores(pedidos);

    pedidos.forEach((p) => {
      const estadoUI = estadoLegible(p.estado);
      const color = colorTarjeta(estadoUI);

      const tarjeta = document.createElement("div");
      tarjeta.className = `tarjeta estado-${color}`;
      tarjeta.dataset.estado = estadoUI;

      // Temporizador urgencia (10s en CREADO)
      if (p.estado === "CREADO" && !temporizadoresUrgencia[p.id]) {
        temporizadoresUrgencia[p.id] = true;

        setTimeout(async () => {
          try {
            const checkRes = await fetch(`/api/pedidos/${p.id}/`);
            const checkData = await checkRes.json();
            if (checkData.estado === "CREADO") {
              // PATCH URGENTE DESACTIVADO (endpoint no existe)
              // await fetch(`/api/pedidos/${p.id}/`, {
              //   method: "PATCH",
              //   headers: { "Content-Type": "application/json" },
              //   body: JSON.stringify({ estado: "URGENTE" }),
              // });
              cargarPedidos();
            }
          } catch (err) {
            console.error("Error en temporizador de urgencia:", err);
          }
        }, 10000);
      }

      let botonHTML = "";
      if (p.estado === "CREADO" || p.estado === "URGENTE") {
        botonHTML = `<button class="btn-accion btn-verde" data-id="${p.id}" data-next="EN_PREPARACION">INICIAR</button>`;
      } else if (p.estado === "EN_PREPARACION") {
        botonHTML = `<button class="btn-accion btn-rojo" data-id="${p.id}" data-next="LISTO">TERMINAR</button>`;
      } else if (p.estado === "LISTO") {
        botonHTML = `<button class="btn-accion btn-azul" data-id="${p.id}" data-next="ENTREGADO">ENTREGADO</button>`;
      }

      const botonDetalle = `<button class="btn-detalle" data-id="${p.id}">Detalle</button>`;

      tarjeta.dataset.mesa = p.mesa;
      tarjeta.dataset.cliente = (p.cliente || "").toLowerCase();
      tarjeta.dataset.fecha = p.fecha_creacion;

      tarjeta.innerHTML = `
        <div class="encabezado">
          <h3 class="mesa">MESA ${p.mesa}</h3>
          <p class="hora">[${formatearHora(p.fecha_creacion)}]</p>
        </div>
        <div class="contenido">
          <p>PEDIDO #${p.id}</p>
          <p class="linea-cliente">Cliente: ${p.cliente || "Sin cliente"}</p>
          <p>Orden: ${p.descripcion || "Sin descripción"}</p>
        </div>
        ${botonHTML}
        ${botonDetalle}
      `;

      contenedor.appendChild(tarjeta);
    });

    activarBotonesAccion();
    activarBotonesDetalle();
    activarFiltros();
    if (window.aplicarFiltrosYOrden) window.aplicarFiltrosYOrden();
    actualizarHora();
  } catch (error) {
    contenedor.innerHTML = "<p style='color:red'>Error al conectar con la API</p>";
    console.error(error);
  }
}

// --------- Botones de acción ---------

function activarBotonesAccion() {
  const botones = document.querySelectorAll(".btn-accion");
  botones.forEach((btn) => {
    btn.onclick = async () => {
      const id = btn.dataset.id;
      const siguiente = btn.dataset.next;

      let url = "";

      if (siguiente === "EN_PREPARACION") {
        url = `/api/pedidos/${id}/confirmar/`;
      } else if (siguiente === "LISTO") {
        url = `/api/pedidos/${id}/listo/`;
      } else if (siguiente === "ENTREGADO") {
        url = `/api/pedidos/${id}/entregar/`;
      }

      try {
        await fetch(url, { method: "PATCH" });

        if (siguiente === "LISTO") {
          const r = await fetch(`/api/pedidos/${id}/`);
          const p = await r.json();
          mostrarNotificacion(p.id, p.mesa, p.descripcion);
        }

        cargarPedidos();
      } catch (err) {
        console.error("Error actualizando estado:", err);
      }
    };
  });
}

// --------- Botones Detalle ---------

function activarBotonesDetalle() {
  document.querySelectorAll(".btn-detalle").forEach((btn) => {
    btn.onclick = () => mostrarDetalleEnModal(btn.dataset.id);
  });
}

// --------- Filtros ---------

function activarFiltros() {
  const tarjetas = document.querySelectorAll(".tarjeta");
  const btnVolver = document.getElementById("btn-volver");

  function aplicarFiltro(estadoFiltro) {
    tarjetas.forEach((t) => {
      const estado = t.dataset.estado;
      t.style.display =
        !estadoFiltro || estadoFiltro === "todos" || estado === estadoFiltro
          ? "flex"
          : "none";
    });
  }

  document.querySelectorAll("#filtros-superiores button").forEach((boton) => {
    boton.onclick = () => {
      const filtro = boton.getAttribute("data-filtro");
      aplicarFiltro(filtro);
      if (btnVolver) btnVolver.style.display = filtro === "todos" ? "none" : "inline-block";
    };
  });

  if (btnVolver) {
    btnVolver.onclick = () => {
      aplicarFiltro("todos");
      btnVolver.style.display = "none";
    };
  }
}

// --------- Hora ---------

function actualizarHora() {
  const el = document.getElementById("ultima-actualizacion");
  if (el) {
    el.textContent = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }
}

// --------- Init ---------

function initMonitor() {
  const btnActualizar = document.getElementById("btn-actualizar");
  if (btnActualizar) btnActualizar.onclick = cargarPedidos;

  configurarCierreModal();
  cargarPedidos();
}

document.addEventListener("DOMContentLoaded", initMonitor);
