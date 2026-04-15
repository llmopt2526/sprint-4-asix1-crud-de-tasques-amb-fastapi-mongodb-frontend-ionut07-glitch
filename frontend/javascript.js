const API_URL = ""; 
let allTasks = []; 

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasques`);
        allTasks = await response.json();
        updateUserFilter(); 
        renderTasks(allTasks);
    } catch (error) {
        console.error('Error:', error);
    }
}

function renderTasks(tasksToRender) {
    document.getElementById('list-pendent').innerHTML = '';
    document.getElementById('list-feta').innerHTML = '';
    tasksToRender.forEach(task => {
        const listElement = document.getElementById(`list-${task.estat}`);
        if (listElement) listElement.appendChild(createTaskCard(task));
    });
}

function filterTasks() {
    const searchT = document.getElementById('searchTitle').value.toLowerCase();
    const filterU = document.getElementById('filterUser').value;
    const filterC = document.getElementById('filterCategory').value;
    const filterS = document.getElementById('filterStatus').value;

    const filtered = allTasks.filter(task => {
        return task.titol.toLowerCase().includes(searchT) &&
               (filterU === "" || task.persona_assignada === filterU) &&
               (filterC === "" || task.categoria === filterC) &&
               (filterS === "" || task.estat === filterS);
    });
    renderTasks(filtered);
}

function updateUserFilter() {
    const userSelect = document.getElementById('filterUser');
    const users = [...new Set(allTasks.map(t => t.persona_assignada))];
    userSelect.innerHTML = '<option value="">Tots els usuaris</option>';
    users.forEach(u => {
        const opt = document.createElement('option');
        opt.value = opt.innerText = u;
        userSelect.appendChild(opt);
    });
}

function resetFilters() {
    document.getElementById('searchTitle').value = '';
    document.getElementById('filterUser').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterStatus').value = '';
    renderTasks(allTasks);
}

function createTaskCard(task) {
    const realId = task.id || task._id;
    const initials = task.persona_assignada ? task.persona_assignada.charAt(0).toUpperCase() : '?';
    let colorClass = 'card-default';
    if (task.categoria === 'Sistemes') colorClass = 'card-blue';
    else if (task.categoria === 'Disseny') colorClass = 'card-pink';
    else if (task.categoria === 'Desenvolupament') colorClass = 'card-green';

    const card = document.createElement('div');
    card.className = `task-card ${colorClass}`;
    card.id = `task-${realId}`;
    card.draggable = true;
    card.ondragstart = (e) => e.dataTransfer.setData("text", e.target.id);
    
    card.innerHTML = `
        <div class="task-title">${task.titol}</div>
        <div class="task-desc">${task.descripcio}</div>
        <div class="task-footer">
            <div class="task-assignee-avatar">${initials}</div>
            <div class="task-actions">
                <button onclick="openModal('editar', '', '${realId}')">✏️</button>
                <button onclick="deleteTask('${realId}')">🗑️</button>
            </div>
        </div>
    `;
    return card;
}

function allowDrop(ev) { ev.preventDefault(); }
async function drop(ev) {
    ev.preventDefault();
    const id = ev.dataTransfer.getData("text").replace('task-', '');
    let col = ev.target;
    while (col && !col.classList.contains('kanban-column')) col = col.parentElement;
    if (col) {
        await fetch(`${API_URL}/actualizar/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ estat: col.getAttribute('data-status') })
        });
        loadTasks();
    }
}

async function openModal(mode, status = '', id = null) {
    const modal = document.getElementById('taskModal');
    modal.style.display = 'block';
    if (mode === 'crear') {
        document.getElementById('taskForm').reset();
        document.getElementById('estat').value = status;
        document.getElementById('taskId').value = '';
    } else {
        const res = await fetch(`${API_URL}/buscar_id/${id}`);
        const t = await res.json();
        document.getElementById('taskId').value = id;
        document.getElementById('titol').value = t.titol;
        document.getElementById('descripcio').value = t.descripcio;
        document.getElementById('estat').value = t.estat;
        document.getElementById('categoria').value = t.categoria;
        document.getElementById('persona_assignada').value = t.persona_assignada;
    }
}

function closeModal() { document.getElementById('taskModal').style.display = 'none'; }

document.getElementById('taskForm').onsubmit = async (e) => {
    e.preventDefault();
    const id = document.getElementById('taskId').value;
    const data = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('descripcio').value,
        estat: document.getElementById('estat').value,
        categoria: document.getElementById('categoria').value,
        persona_assignada: document.getElementById('persona_assignada').value,
        prioritat: "baixa"
    };
    await fetch(id ? `${API_URL}/actualizar/${id}` : `${API_URL}/crear`, {
        method: id ? 'PUT' : 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    closeModal();
    loadTasks();
};

async function deleteTask(id) {
    if (confirm('Esborrar?')) {
        await fetch(`${API_URL}/borrar/${id}`, { method: 'DELETE' });
        loadTasks();
    }
}

window.onload = loadTasks;
