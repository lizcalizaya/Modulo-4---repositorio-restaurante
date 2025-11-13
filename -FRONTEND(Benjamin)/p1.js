const orders = [
  { id: 'MESA1', num:'#1', user:'Cocinero', status:'en-preparacion', time: 2, items:['Menu: 2'], drink:'Fanta' },
  { id: 'MESA2', num:'#2', user:'Cocinero', status:'en-preparacion', time: 5, items:['Menu: 2'], drink:'Cafe'},
  { id: 'MESA3', num:'#3', user:'Cocinero', status:'listo', time: 10, items:['Menu: 1'], drink:'Coca-Cola' },
  { id: 'MESA4', num:'#4', user:'Cocinero', status:'entregado', time: 15, items:['Menu: 1'], drink:'Jugo natural' }
];

let currentFilter = 'todos';

function renderCounts(){
  document.getElementById('count-todos').textContent = orders.length;
  document.getElementById('count-en-preparacion').textContent = orders.filter(o=>o.status==='en-preparacion').length;
  document.getElementById('count-listo').textContent = orders.filter(o=>o.status==='listo').length;
  document.getElementById('count-entregado').textContent = orders.filter(o=>o.status==='entregado').length;
}
function renderBoard(){
  const board = document.getElementById('board');
  board.innerHTML = '';
  const filtered = orders.filter(o => currentFilter==='todos' ? true : o.status===currentFilter);
  filtered.forEach(o => {
    const card = document.createElement('div');
    card.className = `card ${o.status}`;
    card.innerHTML = `
      <div class="meta">
        <div>
          <strong>${o.id} (${o.num})</strong><br>
          <small>${o.user}</small>
          
          <div class="pedido">
            <h4>Pedido</h4>
            <ul class="items">
              ${o.items.map(i=>`<li>${i}</li>`).join('')}
              <li>Bebestible: ${o.drink}</li>
            </ul>
          </div>
        </div>
        
        <div style="text-align:right">
          <div>${o.time ? o.time + ' min' : '-'}</div>
          <span class="badge ${o.status}">${o.status}</span>
        </div>
      </div>
    `;
    board.appendChild(card);
  });
}





function setupUI(){
  document.querySelectorAll('.filter').forEach(btn=>{
    btn.addEventListener('click', e=>{
      document.querySelectorAll('.filter').forEach(b=>b.classList.remove('active'));
      e.currentTarget.classList.add('active');
      currentFilter = e.currentTarget.dataset.filter;
      renderBoard();
    });
  });

  document.getElementById('refresh').addEventListener('click', ()=>{
    renderCounts();
    renderBoard();
  });

  renderCounts();
  renderBoard();
}

document.addEventListener('DOMContentLoaded', setupUI);
