<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", () => {
const contenedor = document.getElementById("contenedor-pedidos");
const btnActualizar = document.getElementById("btn-actualizar");
const btnVolver = document.getElementById("btn-volver");
const ultimaAct = document.getElementById("ultima-actualizacion");


let temporizadoresUrgencia = {};


const actualizarHora = () => {
    ultimaAct.textContent = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
    });
};

// Traducción API → Monitor visual
const estadoLegible = (estadoAPI) => {
    switch (estadoAPI) {
    case "URGENTE": return "Urgente";
    case "CREADO": return "Nuevo";               // Color gris + botón INICIAR
    case "EN_PREPARACION": return "En preparación";
    case "LISTO": return "Listo";
    case "ENTREGADO": return "Entregado";
    default: return estadoAPI;
    }
};

// Color según estado visual
const colorTarjeta = (estadoUI) => {
    switch (estadoUI) {
    case "Nuevo": return "gris";              // NUEVO = gris
    case "En preparación": return "naranja";  // EN_PREPARACION = amarillo/naranja
    case "Listo": return "verde";
    case "Urgente": return "rojo";
    case "Entregado": return "azul";
    default: return "gris";
    }
};

const formatearHora = (iso) => {
    if (!iso) return "";
    const f = new Date(iso);
    return f.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

// ============================
// CARGAR PEDIDOS
// ============================
async function cargarPedidos() {
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

        if (p.estado === "CREADO" && !temporizadoresUrgencia[p.id]) {

    temporizadoresUrgencia[p.id] = true; // marcamos que ya tiene temporizador

    setTimeout(async () => {

        // Verificar si el pedido sigue siendo CREADO
        try {
            const checkRes = await fetch(`/api/pedidos/${p.id}/`);
            const checkData = await checkRes.json();

            if (checkData.estado === "CREADO") {

                // Cambiar a URGENTE
                await fetch(`/api/pedidos/${p.id}/`, {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ estado: "URGENTE" })
                });

                cargarPedidos(); // actualizar pantalla
            }

        } catch (err) {
            console.error("Error en temporizador de urgencia:", err);
        }

            }, 10000); // 10 segundos
        }

        let boton = "";

        // BOTONES SEGÚN ESTADO
        if (p.estado === "CREADO" || p.estado === "URGENTE") {
            // Ambos muestran INICIAR y pasan a EN_PREPARACION
            boton = `<button class="btn-accion btn-verde" data-id="${p.id}" data-next="EN_PREPARACION">INICIAR</button>`;
        } 
        else if (p.estado === "EN_PREPARACION") {
            boton = `<button class="btn-accion btn-rojo" data-id="${p.id}" data-next="LISTO">TERMINAR</button>`;
        } 
        else if (p.estado === "LISTO") {
            boton = `<button class="btn-accion btn-azul" data-id="${p.id}" data-next="ENTREGADO">ENTREGADO</button>`;
        }


        tarjeta.innerHTML = `
        <div class="encabezado">
            <h3 class="mesa">MESA ${p.mesa}</h3>
            <p class="hora">[${formatearHora(p.fecha_creacion)}]</p>
        </div>

        <div class="contenido">
            <p>PEDIDO #${p.id}</p>
            <ul>
            <li>${p.descripcion || "Sin descripción"}</li>
            </ul>
        </div>

        ${boton}
        `;

        contenedor.appendChild(tarjeta);
    });

    activarBotonesAccion();
    activarFiltros();
    actualizarHora();

    } catch (error) {
    contenedor.innerHTML = "<p style='color:red'>Error al conectar con la API</p>";
    console.error(error);
    }
}

// ============================
// BOTONES (INICIAR / TERMINAR / ENTREGADO)
// ============================
function activarBotonesAccion() {
    document.querySelectorAll(".btn-accion").forEach((btn) => {
        btn.onclick = async () => {
            const id = btn.dataset.id;
            const siguiente = btn.dataset.next;

            // Obtener datos actuales del pedido ANTES de actualizar estado
            const datosRes = await fetch(`/api/pedidos/${id}/`);
            const datosPedido = await datosRes.json();

            await fetch(`/api/pedidos/${id}/`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado: siguiente })
            });

            // Mostrar notificación cuando pase a LISTO
            if (siguiente === "LISTO") {
                let mesa = datosPedido.mesa;
                let detalle = datosPedido.descripcion || "Sin detalle";
                mostrarNotificacion(id, mesa, detalle);
            }

            cargarPedidos(); // recargar pantalla
        };
    });
}


// ============================
// FILTROS
// ============================
function activarFiltros() {
const tarjetas = document.querySelectorAll(".tarjeta");

// FILTROS SUPERIORES
document.querySelectorAll("#filtros-superiores button").forEach((boton) => {
    boton.onclick = () => {
    const filtro = boton.dataset.filtro; // "Entregado", "Listo", etc.

    tarjetas.forEach((t) => {
        const estado = t.dataset.estado.trim(); // <- aseguramos igualdad exacta
        t.style.display = (filtro === "todos" || estado === filtro) ? "flex" : "none";
    });

    btnVolver.style.display = (filtro === "todos") ? "none" : "inline-block";
    };
});

// FILTROS INFERIORES (abajo a la derecha)
document.querySelectorAll("#filtros-inferiores button").forEach((boton) => {
    boton.onclick = () => {
    const filtro = boton.dataset.filtro; // "Entregado"

    tarjetas.forEach((t) => {
        const estado = t.dataset.estado.trim();
        t.style.display = (estado === filtro) ? "flex" : "none";
    });

    btnVolver.style.display = "inline-block";
    };
});
}


// Botón volver
btnVolver.onclick = () => {
    document.querySelectorAll(".tarjeta").forEach((t) => t.style.display = "flex");
    btnVolver.style.display = "none";
};

// Botón actualizar
btnActualizar.onclick = cargarPedidos;

cargarPedidos();
});


function actualizarContadores(pedidos) {
    let total = pedidos.length;
    let prep = pedidos.filter(p => p.estado === "EN_PREPARACION").length;
    let listo = pedidos.filter(p => p.estado === "LISTO").length;
    let entregado = pedidos.filter(p => p.estado === "ENTREGADO").length;
    let urgente = pedidos.filter(p => p.estado === "URGENTE").length;

    document.getElementById("filtro-todos").textContent = `Todos (${total})`;
    document.getElementById("filtro-preparacion").textContent = `En preparación (${prep})`;
    document.getElementById("filtro-listo").textContent = `Listo (${listo})`;
    document.getElementById("filtro-entregado").textContent = `Entregado (${entregado})`;
    document.getElementById("filtro-urgente").textContent = `Urgente (${urgente})`;
}


function mostrarNotificacion(id, mesa, detalle) {
    const cont = document.getElementById("notificaciones");

    const caja = document.createElement("div");
    caja.className = "notificacion";

    caja.innerHTML = `
        <button class="boton-cerrar" onclick="this.parentElement.remove()">×</button>
        <strong>La orden con ID: ${id} para la mesa N°${mesa} se encuentra<br>lista para ser entregada.</strong>
        <p>Detalle: "${detalle}"</p>
    `;

    cont.appendChild(caja);

    // Se elimina sola a los 10 segundos
    setTimeout(() => {
        if (caja.parentElement) caja.remove();
    }, 10000);
}
=======
document.addEventListener("DOMContentLoaded", () => {
const contenedor = document.getElementById("contenedor-pedidos");
const btnActualizar = document.getElementById("btn-actualizar");
const btnVolver = document.getElementById("btn-volver");
const ultimaAct = document.getElementById("ultima-actualizacion");


let temporizadoresUrgencia = {};


const actualizarHora = () => {
    ultimaAct.textContent = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
    });
};

// Traducción API → Monitor visual
const estadoLegible = (estadoAPI) => {
    switch (estadoAPI) {
    case "URGENTE": return "Urgente";
    case "CREADO": return "Nuevo";               // Color gris + botón INICIAR
    case "EN_PREPARACION": return "En preparación";
    case "LISTO": return "Listo";
    case "ENTREGADO": return "Entregado";
    default: return estadoAPI;
    }
};

// Color según estado visual
const colorTarjeta = (estadoUI) => {
    switch (estadoUI) {
    case "Nuevo": return "gris";              // NUEVO = gris
    case "En preparación": return "naranja";  // EN_PREPARACION = amarillo/naranja
    case "Listo": return "verde";
    case "Urgente": return "rojo";
    case "Entregado": return "azul";
    default: return "gris";
    }
};

const formatearHora = (iso) => {
    if (!iso) return "";
    const f = new Date(iso);
    return f.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

// ============================
// CARGAR PEDIDOS
// ============================
async function cargarPedidos() {
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

        if (p.estado === "CREADO" && !temporizadoresUrgencia[p.id]) {

    temporizadoresUrgencia[p.id] = true; // marcamos que ya tiene temporizador

    setTimeout(async () => {

        // Verificar si el pedido sigue siendo CREADO
        try {
            const checkRes = await fetch(`/api/pedidos/${p.id}/`);
            const checkData = await checkRes.json();

            if (checkData.estado === "CREADO") {

                // Cambiar a URGENTE
                await fetch(`/api/pedidos/${p.id}/`, {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ estado: "URGENTE" })
                });

                cargarPedidos(); // actualizar pantalla
            }

        } catch (err) {
            console.error("Error en temporizador de urgencia:", err);
        }

            }, 10000); // 10 segundos
        }

        let boton = "";

        // BOTONES SEGÚN ESTADO
        if (p.estado === "CREADO" || p.estado === "URGENTE") {
            // Ambos muestran INICIAR y pasan a EN_PREPARACION
            boton = `<button class="btn-accion btn-verde" data-id="${p.id}" data-next="EN_PREPARACION">INICIAR</button>`;
        } 
        else if (p.estado === "EN_PREPARACION") {
            boton = `<button class="btn-accion btn-rojo" data-id="${p.id}" data-next="LISTO">TERMINAR</button>`;
        } 
        else if (p.estado === "LISTO") {
            boton = `<button class="btn-accion btn-azul" data-id="${p.id}" data-next="ENTREGADO">ENTREGADO</button>`;
        }


        tarjeta.innerHTML = `
        <div class="encabezado">
            <h3 class="mesa">MESA ${p.mesa}</h3>
            <p class="hora">[${formatearHora(p.fecha_creacion)}]</p>
        </div>

        <div class="contenido">
            <p>PEDIDO #${p.id}</p>
            <ul>
            <li>${p.descripcion || "Sin descripción"}</li>
            </ul>
        </div>

        ${boton}
        `;

        contenedor.appendChild(tarjeta);
    });

    activarBotonesAccion();
    activarFiltros();
    actualizarHora();

    } catch (error) {
    contenedor.innerHTML = "<p style='color:red'>Error al conectar con la API</p>";
    console.error(error);
    }
}

// ============================
// BOTONES (INICIAR / TERMINAR / ENTREGADO)
// ============================
function activarBotonesAccion() {
    document.querySelectorAll(".btn-accion").forEach((btn) => {
        btn.onclick = async () => {
            const id = btn.dataset.id;
            const siguiente = btn.dataset.next;

            // Obtener datos actuales del pedido ANTES de actualizar estado
            const datosRes = await fetch(`/api/pedidos/${id}/`);
            const datosPedido = await datosRes.json();

            await fetch(`/api/pedidos/${id}/`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado: siguiente })
            });

            // Mostrar notificación cuando pase a LISTO
            if (siguiente === "LISTO") {
                let mesa = datosPedido.mesa;
                let detalle = datosPedido.descripcion || "Sin detalle";
                mostrarNotificacion(id, mesa, detalle);
            }

            cargarPedidos(); // recargar pantalla
        };
    });
}


// ============================
// FILTROS
// ============================
function activarFiltros() {
const tarjetas = document.querySelectorAll(".tarjeta");

// FILTROS SUPERIORES
document.querySelectorAll("#filtros-superiores button").forEach((boton) => {
    boton.onclick = () => {
    const filtro = boton.dataset.filtro; // "Entregado", "Listo", etc.

    tarjetas.forEach((t) => {
        const estado = t.dataset.estado.trim(); // <- aseguramos igualdad exacta
        t.style.display = (filtro === "todos" || estado === filtro) ? "flex" : "none";
    });

    btnVolver.style.display = (filtro === "todos") ? "none" : "inline-block";
    };
});

// FILTROS INFERIORES (abajo a la derecha)
document.querySelectorAll("#filtros-inferiores button").forEach((boton) => {
    boton.onclick = () => {
    const filtro = boton.dataset.filtro; // "Entregado"

    tarjetas.forEach((t) => {
        const estado = t.dataset.estado.trim();
        t.style.display = (estado === filtro) ? "flex" : "none";
    });

    btnVolver.style.display = "inline-block";
    };
});
}


// Botón volver
btnVolver.onclick = () => {
    document.querySelectorAll(".tarjeta").forEach((t) => t.style.display = "flex");
    btnVolver.style.display = "none";
};

// Botón actualizar
btnActualizar.onclick = cargarPedidos;

cargarPedidos();
});


function actualizarContadores(pedidos) {
    let total = pedidos.length;
    let prep = pedidos.filter(p => p.estado === "EN_PREPARACION").length;
    let listo = pedidos.filter(p => p.estado === "LISTO").length;
    let entregado = pedidos.filter(p => p.estado === "ENTREGADO").length;
    let urgente = pedidos.filter(p => p.estado === "URGENTE").length;

    document.getElementById("filtro-todos").textContent = `Todos (${total})`;
    document.getElementById("filtro-preparacion").textContent = `En preparación (${prep})`;
    document.getElementById("filtro-listo").textContent = `Listo (${listo})`;
    document.getElementById("filtro-entregado").textContent = `Entregado (${entregado})`;
    document.getElementById("filtro-urgente").textContent = `Urgente (${urgente})`;
}


function mostrarNotificacion(id, mesa, detalle) {
    const cont = document.getElementById("notificaciones");

    const caja = document.createElement("div");
    caja.className = "notificacion";

    caja.innerHTML = `
        <button class="boton-cerrar" onclick="this.parentElement.remove()">×</button>
        <strong>La orden con ID: ${id} para la mesa N°${mesa} se encuentra<br>lista para ser entregada.</strong>
        <p>Detalle: "${detalle}"</p>
    `;

    cont.appendChild(caja);

    // Se elimina sola a los 10 segundos
    setTimeout(() => {
        if (caja.parentElement) caja.remove();
    }, 10000);
}
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
