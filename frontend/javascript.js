// ------------------------------------------------------------------------ //
//                            Cerca JavaScript                              //
// ------------------------------------------------------------------------ //

// Variable de configuració per a l'API. 
// Es deixa buida ("") per fer servir rutes relatives. Això permet que el frontend 
// funcioni correctament tant en local (localhost) com en producció (servidor real)
// sense haver de canviar manualment l'adreça IP o el domini.
const API_URL = ""; 
let allTasks = []; 

// Mitjançant una funció asíncrona, obtenim les dades de l'API. Fem servir await fetch
// a l'endpoint de tasques i les guardem a la variable allTasks. D'aquesta manera,
// evitem fer peticions constants a l'API per a operacions de filtratge. 
// També actualitzem el filtre d'usuaris i gestionem possibles errors.
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasques`);
        allTasks = await response.json();
        updateUserFilter(); 
        renderTasks(allTasks);
    } catch (error) {
        console.error('Error al carregar tasques:', error);
    }
}

// Aquesta funció s'encarrega de renderitzar les tasques al DOM. Les separa 
// en el llistat de pendent o feta per distribuir-les en el tauler corresponent
// basant-se en el camp estat de cada document provinent de MongoDB.
function renderTasks(tasksToRender) {
    document.getElementById('list-pendent').innerHTML = '';
    document.getElementById('list-feta').innerHTML = '';
    tasksToRender.forEach(task => {
        const listElement = document.getElementById(`list-${task.estat}`);
        if (listElement) listElement.appendChild(createTaskCard(task));
    });
}

// ------------------------------------------------------------------------ //
//                           Filtratge de Dades                             //
// ------------------------------------------------------------------------ //


// Aquesta funció recull els valors dels inputs per realitzar la cerca per títol.
// També aplica els filtres per persona assignada, categoria i estat, permetent
// una cerca combinada molt precisa.
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


// Aquesta funció genera dinàmicament les opcions del desplegable d'usuaris.
// Fa servir un Set per obtenir noms únics de la llista de tasques actual,
// garantint que el filtre d'usuaris estigui sempre actualitzat.
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

// Restableix tots els camps de filtre a la seva posició inicial i 
// torna a mostrar totes les tasques sense cap restricció.
function resetFilters() {
    document.getElementById('searchTitle').value = '';
    document.getElementById('filterUser').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterStatus').value = '';
    renderTasks(allTasks);
}

// ------------------------------------------------------------------------ //
//                  Funcions de modificació de dades                        //
// ------------------------------------------------------------------------ //

// Construeix l'estructura HTML de cada targeta de tasca (Task Card).
// Assigna colors segons la categoria, gestiona les inicials de l'avatar i
// configura els esdeveniments per permetre que la targeta sigui arrossegable (Drag).
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

// Aquestes funcions gestionen el sistema arrosegar i posar. Quan una tasca es deixa 
// anar sobre una columna, s'executa una petició PUT a l'API per actualitzar 
// l'estat del document a la base de dades i es recarrega el tauler.
function allowDrop(ev) { ev.preventDefault(); }
async function drop(ev) {
    ev.preventDefault();
    const id = ev.dataTransfer.getData("text").replace('task-', '');
    let col = ev.target;
    // Busquem el contenidor pare que sigui la columna Kanban
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

// Gestiona l'obertura de la interficie modal tant per a la creació com per a l'edició.
// Si és edició, fa un fetch previ per emplenar el formulari amb les dades actuals.
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

// Tanca la interfice modal de formulari.
function closeModal() { document.getElementById('taskModal').style.display = 'none'; }

// Gestiona l'enviament del formulari (Submit). Decideix si ha de fer un POST (crear)
// o un PUT (actualitzar) segons si existeix un ID de tasca, i després actualitza el tauler.
document.getElementById('taskForm').onsubmit = async (e) => {
    e.preventDefault();
    const id = document.getElementById('taskId').value;
    const data = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('descripcio').value,
        estat: document.getElementById('estat').value,
        categoria: document.getElementById('categoria').value,
        persona_assignada: document.getElementById('persona_assignada').value,
        prioritat: "baixa" // Valor per defecte
    };
    
    await fetch(id ? `${API_URL}/actualizar/${id}` : `${API_URL}/crear`, {
        method: id ? 'PUT' : 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    closeModal();
    loadTasks();
};

// Elimina de forma permanent una tasca mitjançant una crida a l'endpoint de borrar.
// Inclou una confirmació de seguretat per a l'usuari.
async function deleteTask(id) {
    if (confirm('Estàs segur que vols esborrar aquesta tasca?')) {
        await fetch(`${API_URL}/borrar/${id}`, { method: 'DELETE' });
        loadTasks();
    }
}

// Càrrega inicial quan es completa la càrrega de la pàgina.
window.onload = loadTasks;
