// ==========================================
// SIC - Sistema de Autorización de Compras
// Static version for GitHub Pages
// Mock authentication and data management
// ==========================================

// Mock Users (fake credentials)
const MOCK_USERS = [
    {
        email: "admin@empresa.cl",
        password: "admin123",
        username: "admin",
        first_name: "Carlos",
        last_name: "González",
        rut: "12.345.678-9",
        role: "administrador",
        pertenece: "Gerencia General"
    },
    {
        email: "usuario@empresa.cl",
        password: "user123",
        username: "jperez",
        first_name: "Juan",
        last_name: "Pérez",
        rut: "11.222.333-4",
        role: "usuario_normal",
        pertenece: "Producción"
    },
    {
        email: "revisor@empresa.cl",
        password: "revisor123",
        username: "mlopez",
        first_name: "María",
        last_name: "López",
        rut: "15.666.777-8",
        role: "revisor",
        pertenece: "Control de Calidad"
    },
    {
        email: "aprobador@empresa.cl",
        password: "aprobador123",
        username: "rmorales",
        first_name: "Roberto",
        last_name: "Morales",
        rut: "13.444.555-6",
        role: "aprobador",
        pertenece: "Gerencia de Compras"
    }
];

// Default mock solicitudes
const DEFAULT_SOLICITUDES = [
    {
        numero_sic: 1,
        es_muestra: false,
        pertenece: "Producción",
        fecha_sic: "2026-01-15",
        fecha_requerida: "2026-02-01",
        solicitante_email: "usuario@empresa.cl",
        descripcion: "Compra de materiales de oficina",
        especificacion_tecnica: "Resmas de papel A4, tinta para impresora HP",
        cantidad: 50,
        unidad: "Unidades",
        comentario: "Urgente para el departamento",
        estado: "Pendiente",
        archivo: null,
        editada: false
    },
    {
        numero_sic: 2,
        es_muestra: true,
        pertenece: "Control de Calidad",
        fecha_sic: "2026-01-20",
        fecha_requerida: "2026-02-10",
        solicitante_email: "usuario@empresa.cl",
        descripcion: "Muestra de guantes de seguridad",
        especificacion_tecnica: "Guantes de nitrilo talla M, resistencia química",
        cantidad: 10,
        unidad: "Pares",
        comentario: "Para evaluación de nuevo proveedor",
        estado: "Autorizado",
        archivo: null,
        editada: false
    },
    {
        numero_sic: 3,
        es_muestra: false,
        pertenece: "Producción",
        fecha_sic: "2026-02-01",
        fecha_requerida: "2026-02-15",
        solicitante_email: "admin@empresa.cl",
        descripcion: "Herramientas de mantenimiento",
        especificacion_tecnica: "Set de llaves Allen, destornilladores Phillips y planos",
        cantidad: 5,
        unidad: "Sets",
        comentario: "",
        estado: "Rechazado",
        archivo: null,
        editada: false
    },
    {
        numero_sic: 4,
        es_muestra: false,
        pertenece: "Gerencia General",
        fecha_sic: "2026-02-05",
        fecha_requerida: "2026-03-01",
        solicitante_email: "admin@empresa.cl",
        descripcion: "Equipos informáticos",
        especificacion_tecnica: "Notebooks Lenovo ThinkPad T14, 16GB RAM, 512GB SSD",
        cantidad: 3,
        unidad: "Unidades",
        comentario: "Renovación de equipos del área",
        estado: "Pendiente",
        archivo: null,
        editada: false
    },
    {
        numero_sic: 5,
        es_muestra: true,
        pertenece: "Control de Calidad",
        fecha_sic: "2026-02-10",
        fecha_requerida: "2026-03-05",
        solicitante_email: "revisor@empresa.cl",
        descripcion: "Muestra de reactivos químicos",
        especificacion_tecnica: "Ácido sulfúrico grado analítico, 500ml",
        cantidad: 2,
        unidad: "Botellas",
        comentario: "Para pruebas de laboratorio",
        estado: "Pendiente",
        archivo: null,
        editada: false
    }
];

// ==========================================
// Data Management (localStorage)
// ==========================================

function initData() {
    if (!localStorage.getItem("sic_solicitudes")) {
        localStorage.setItem("sic_solicitudes", JSON.stringify(DEFAULT_SOLICITUDES));
    }
}

function getSolicitudes() {
    initData();
    return JSON.parse(localStorage.getItem("sic_solicitudes"));
}

function saveSolicitudes(solicitudes) {
    localStorage.setItem("sic_solicitudes", JSON.stringify(solicitudes));
}

function getNextNumeroSIC() {
    var solicitudes = getSolicitudes();
    if (solicitudes.length === 0) return 1;
    var max = 0;
    for (var i = 0; i < solicitudes.length; i++) {
        if (solicitudes[i].numero_sic > max) max = solicitudes[i].numero_sic;
    }
    return max + 1;
}

// ==========================================
// Authentication
// ==========================================

function login(email, password) {
    for (var i = 0; i < MOCK_USERS.length; i++) {
        if (MOCK_USERS[i].email === email && MOCK_USERS[i].password === password) {
            sessionStorage.setItem("sic_user", JSON.stringify(MOCK_USERS[i]));
            return true;
        }
    }
    return false;
}

function logout() {
    sessionStorage.removeItem("sic_user");
    window.location.href = "index.html";
}

function getCurrentUser() {
    var data = sessionStorage.getItem("sic_user");
    if (data) return JSON.parse(data);
    return null;
}

function requireAuth() {
    if (!getCurrentUser()) {
        window.location.href = "index.html";
        return false;
    }
    return true;
}

function getUserByEmail(email) {
    for (var i = 0; i < MOCK_USERS.length; i++) {
        if (MOCK_USERS[i].email === email) return MOCK_USERS[i];
    }
    return null;
}

function getFullName(user) {
    if (!user) return "Desconocido";
    return user.first_name + " " + user.last_name;
}

// ==========================================
// UI Helpers
// ==========================================

function isRevisor(user) {
    return user.role === "revisor" || user.role === "aprobador" || user.role === "administrador";
}

function isAprobador(user) {
    return user.role === "aprobador" || user.role === "administrador";
}

function isAdmin(user) {
    return user.role === "administrador";
}

function renderSidebar(user) {
    var html = '';
    html += '<div class="sidebar-header text-center py-4">';
    html += '<div class="container-fluid">';
    html += '<a class="navbar-brand" href="home.html">';
    html += '<img src="static/img/logo_mamut.jpg" alt="Logo" height="60">';
    html += '</a>';
    html += '<h5 class="text-white mb-1">' + escapeHtml(user.username) + '</h5>';
    html += '<small class="text-white mb-1">' + escapeHtml(user.email) + '</small>';
    html += '</div></div>';

    html += '<ul class="nav flex-column px-3">';
    html += '<li class="nav-item mb-2"><a href="home.html" class="nav-link text-white"><i class="fas fa-file-alt me-2"></i> Solicitudes SIC</a></li>';
    html += '<li class="nav-item mb-2"><a href="historial.html" class="nav-link text-white"><i class="fas fa-history me-2"></i> Historial</a></li>';

    if (isRevisor(user)) {
        html += '<li class="nav-item mb-2"><a href="revisor.html" class="nav-link text-white"><i class="fas fa-check me-2"></i> Revisor</a></li>';
    }
    if (isAprobador(user)) {
        html += '<li class="nav-item mb-2"><a href="aprobaciones.html" class="nav-link text-white"><i class="fas fa-thumbs-up me-2"></i> Aprobaciones</a></li>';
    }

    html += '</ul>';
    html += '<div class="sidebar-footer mt-auto p-3">';
    html += '<button onclick="logout()" class="btn btn-outline-danger w-100"><i class="fas fa-sign-out-alt me-2"></i>Cerrar Sesión</button>';
    html += '</div>';

    return html;
}

function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    return dateStr;
}

function getTodayStr() {
    var d = new Date();
    var month = '' + (d.getMonth() + 1);
    var day = '' + d.getDate();
    var year = d.getFullYear();
    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;
    return year + '-' + month + '-' + day;
}

// Initialize sidebar on authenticated pages
function initPage() {
    if (!requireAuth()) return false;
    var user = getCurrentUser();
    var sidebarEl = document.getElementById("sidebar");
    if (sidebarEl) {
        sidebarEl.innerHTML = renderSidebar(user);
    }
    return true;
}

console.log("Sistema SIC cargado correctamente.");
