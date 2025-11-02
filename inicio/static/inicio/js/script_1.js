// Theme toggle functionality
let isDarkMode = false;

function toggleTheme() {
    const html = document.documentElement;
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }
}

// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const contentArea = document.getElementById('mainContent');

    // Cargar dashboard por defecto
    contentArea.innerHTML = generateDashboard();

    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');

            const section = this.dataset.section;

            switch(section) {
                case 'dashboard':
                    contentArea.innerHTML = generateDashboard();
                    break;
                case 'usuarios':
                    contentArea.innerHTML = generateUsuarios();
                    break;
                case 'facturacion':
                    contentArea.innerHTML = generateFacturacion();
                    break;
                case 'pagos':
                    contentArea.innerHTML = generatePagos();
                    break;
                case 'consumos':
                    contentArea.innerHTML = generateConsumos();
                    break;
                case 'reportes':
                    contentArea.innerHTML = generateReportes();
                    break;
                case 'configuracion':
                    contentArea.innerHTML = generateConfiguracion();
                    break;
            }
        });
    });
});

// Generate Dashboard Content
function generateDashboard() {
    return `
        <!-- Statistics Cards -->
        <div class="dashboard-grid">
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Total Usuarios</span>
                    <div class="stat-icon" style="background-color: #dbeafe; color: #1e40af;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                    </div>
                </div>
                <div class="stat-value">1,247</div>
                <div class="stat-change positive">↑ 12% vs. mes anterior</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Facturación Mensual</span>
                    <div class="stat-icon" style="background-color: #d1fae5; color: #065f46;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="12" y1="1" x2="12" y2="23"></line>
                            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                        </svg>
                    </div>
                </div>
                <div class="stat-value">$2.4M</div>
                <div class="stat-change positive">↑ 8% vs. mes anterior</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Pagos Pendientes</span>
                    <div class="stat-icon" style="background-color: #fef3c7; color: #92400e;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <path d="M12 6v6l4 2"></path>
                        </svg>
                    </div>
                </div>
                <div class="stat-value">143</div>
                <div class="stat-change negative">↓ 5% vs. mes anterior</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Consumo Promedio</span>
                    <div class="stat-icon" style="background-color: #e0e7ff; color: #3730a3;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                        </svg>
                    </div>
                </div>
                <div class="stat-value">18.5m³</div>
                <div class="stat-change positive">↑ 3% vs. mes anterior</div>
            </div>
        </div>

        <!-- Recent Transactions Table -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Pagos Recientes</h2>
                <button class="btn btn-secondary" onclick="alert('Ver historial completo de pagos')">Ver todos</button>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Boleta N°</th>
                        <th>Monto</th>
                        <th>Estado</th>
                        <th>Fecha</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>María González</td>
                        <td>#2024-1523</td>
                        <td>$12,500</td>
                        <td><span class="badge badge-success">Pagado</span></td>
                        <td>24/10/2025</td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver detalle de pago #2024-1523')" title="Ver detalle">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                </button>
                                <button class="btn-icon" onclick="alert('Descargando boleta #2024-1523')" title="Descargar">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="7 10 12 15 17 10"></polyline>
                                        <line x1="12" y1="15" x2="12" y2="3"></line>
                                    </svg>
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Juan Pérez</td>
                        <td>#2024-1522</td>
                        <td>$15,300</td>
                        <td><span class="badge badge-success">Pagado</span></td>
                        <td>24/10/2025</td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver detalle de pago #2024-1522')" title="Ver detalle">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                </button>
                                <button class="btn-icon" onclick="alert('Descargando boleta #2024-1522')" title="Descargar">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="7 10 12 15 17 10"></polyline>
                                        <line x1="12" y1="15" x2="12" y2="3"></line>
                                    </svg>
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>Ana Rodríguez</td>
                        <td>#2024-1521</td>
                        <td>$9,800</td>
                        <td><span class="badge badge-warning">Pendiente</span></td>
                        <td>23/10/2025</td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver detalle de pago #2024-1521')" title="Ver detalle">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                        <circle cx="12" cy="12" r="3"></circle>
                                    </svg>
                                </button>
                                <button class="btn-icon" onclick="alert('Descargando boleta #2024-1521')" title="Descargar">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="7 10 12 15 17 10"></polyline>
                                        <line x1="12" y1="15" x2="12" y2="3"></line>
                                    </svg>
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Acciones Rápidas</h2>
            </div>
            <div class="dashboard-grid">
                <button class="btn btn-primary" onclick="alert('Formulario de nuevo usuario')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <svg style="margin: 0 auto;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="12" y1="5" x2="12" y2="19"></line>
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                        <span>Nuevo Usuario</span>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Generador de facturas')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <svg style="margin: 0 auto;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                            <line x1="2" y1="10" x2="22" y2="10"></line>
                        </svg>
                        <span>Generar Factura</span>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Registro de consumos')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <svg style="margin: 0 auto;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                        </svg>
                        <span>Registrar Consumo</span>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Generador de reportes')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <svg style="margin: 0 auto;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="20" x2="18" y2="10"></line>
                            <line x1="12" y1="20" x2="12" y2="4"></line>
                            <line x1="6" y1="20" x2="6" y2="14"></line>
                        </svg>
                        <span>Ver Reportes</span>
                    </div>
                </button>
            </div>
        </div>
    `;
}

// Generate Usuarios Content
function generateUsuarios() {
    return `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Gestión de Usuarios</h2>
                <button class="btn btn-primary" onclick="alert('Agregar nuevo usuario')">+ Nuevo Usuario</button>
            </div>
            <div style="margin-bottom: 1rem; display: flex; gap: 1rem;">
                <input type="text" placeholder="Buscar usuario..." style="flex: 1; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                <select style="padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                    <option>Todos los estados</option>
                    <option>Activos</option>
                    <option>Inactivos</option>
                    <option>Morosos</option>
                </select>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>RUT</th>
                        <th>Dirección</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#001</td>
                        <td>María González</td>
                        <td>15.234.567-8</td>
                        <td>Calle Principal 123</td>
                        <td><span class="badge badge-success">Activo</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Editar usuario María González')" title="Editar">✏️</button>
                                <button class="btn-icon" onclick="alert('Ver historial de María González')" title="Historial">📋</button>
                                <button class="btn-icon" onclick="if(confirm('¿Eliminar usuario María González?')) alert('Usuario eliminado')" title="Eliminar">🗑️</button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>#002</td>
                        <td>Juan Pérez</td>
                        <td>16.345.678-9</td>
                        <td>Av. Los Pinos 456</td>
                        <td><span class="badge badge-success">Activo</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Editar usuario Juan Pérez')" title="Editar">✏️</button>
                                <button class="btn-icon" onclick="alert('Ver historial de Juan Pérez')" title="Historial">📋</button>
                                <button class="btn-icon" onclick="if(confirm('¿Eliminar usuario Juan Pérez?')) alert('Usuario eliminado')" title="Eliminar">🗑️</button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>#003</td>
                        <td>Ana Rodríguez</td>
                        <td>17.456.789-0</td>
                        <td>Pasaje Los Robles 789</td>
                        <td><span class="badge badge-warning">Moroso</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Editar usuario Ana Rodríguez')" title="Editar">✏️</button>
                                <button class="btn-icon" onclick="alert('Ver historial de Ana Rodríguez')" title="Historial">📋</button>
                                <button class="btn-icon" onclick="if(confirm('¿Eliminar usuario Ana Rodríguez?')) alert('Usuario eliminado')" title="Eliminar">🗑️</button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>#004</td>
                        <td>Carlos Muñoz</td>
                        <td>18.567.890-1</td>
                        <td>Calle Los Aromos 321</td>
                        <td><span class="badge badge-success">Activo</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Editar usuario Carlos Muñoz')" title="Editar">✏️</button>
                                <button class="btn-icon" onclick="alert('Ver historial de Carlos Muñoz')" title="Historial">📋</button>
                                <button class="btn-icon" onclick="if(confirm('¿Eliminar usuario Carlos Muñoz?')) alert('Usuario eliminado')" title="Eliminar">🗑️</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// Generate Facturacion Content
function generateFacturacion() {
    return `
        <div class="dashboard-grid" style="margin-bottom: 1.5rem;">
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Total Facturado</span>
                    <div class="stat-icon" style="background-color: #d1fae5; color: #065f46;">💰</div>
                </div>
                <div class="stat-value">$2.4M</div>
                <div class="stat-change positive">↑ 8% este mes</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Facturas Emitidas</span>
                    <div class="stat-icon" style="background-color: #dbeafe; color: #1e40af;">📄</div>
                </div>
                <div class="stat-value">1,247</div>
                <div class="stat-change positive">↑ 12% este mes</div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-title">Por Cobrar</span>
                    <div class="stat-icon" style="background-color: #fef3c7; color: #92400e;">⏰</div>
                </div>
                <div class="stat-value">$320K</div>
                <div class="stat-change negative">143 facturas</div>
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Historial de Facturación</h2>
                <button class="btn btn-primary" onclick="alert('Generar nueva factura')">+ Nueva Factura</button>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>N° Factura</th>
                        <th>Usuario</th>
                        <th>Período</th>
                        <th>Consumo (m³)</th>
                        <th>Monto</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#2024-1523</td>
                        <td>María González</td>
                        <td>Octubre 2025</td>
                        <td>18.5</td>
                        <td>$12,500</td>
                        <td><span class="badge badge-success">Pagada</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver factura #2024-1523')" title="Ver">👁️</button>
                                <button class="btn-icon" onclick="alert('Descargar PDF #2024-1523')" title="Descargar">⬇️</button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>#2024-1522</td>
                        <td>Juan Pérez</td>
                        <td>Octubre 2025</td>
                        <td>22.3</td>
                        <td>$15,300</td>
                        <td><span class="badge badge-success">Pagada</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver factura #2024-1522')" title="Ver">👁️</button>
                                <button class="btn-icon" onclick="alert('Descargar PDF #2024-1522')" title="Descargar">⬇️</button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>#2024-1521</td>
                        <td>Ana Rodríguez</td>
                        <td>Octubre 2025</td>
                        <td>14.8</td>
                        <td>$9,800</td>
                        <td><span class="badge badge-warning">Pendiente</span></td>
                        <td>
                            <div class="actions">
                                <button class="btn-icon" onclick="alert('Ver factura #2024-1521')" title="Ver">👁️</button>
                                <button class="btn-icon" onclick="alert('Descargar PDF #2024-1521')" title="Descargar">⬇️</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// Generate Pagos Content
function generatePagos() {
    return `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Registro de Pagos</h2>
                <button class="btn btn-primary" onclick="alert('Registrar pago manual')">+ Registrar Pago</button>
            </div>
            <div style="margin-bottom: 1rem; display: flex; gap: 1rem;">
                <input type="date" style="padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                <select style="padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                    <option>Todos los estados</option>
                    <option>Pagado</option>
                    <option>Pendiente</option>
                    <option>Vencido</option>
                </select>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>N° Pago</th>
                        <th>Usuario</th>
                        <th>Factura</th>
                        <th>Método</th>
                        <th>Monto</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#PAG-523</td>
                        <td>María González</td>
                        <td>#2024-1523</td>
                        <td>Transferencia</td>
                        <td>$12,500</td>
                        <td>24/10/2025</td>
                        <td><span class="badge badge-success">Confirmado</span></td>
                    </tr>
                    <tr>
                        <td>#PAG-522</td>
                        <td>Juan Pérez</td>
                        <td>#2024-1522</td>
                        <td>Efectivo</td>
                        <td>$15,300</td>
                        <td>24/10/2025</td>
                        <td><span class="badge badge-success">Confirmado</span></td>
                    </tr>
                    <tr>
                        <td>#PAG-521</td>
                        <td>Ana Rodríguez</td>
                        <td>#2024-1521</td>
                        <td>-</td>
                        <td>$9,800</td>
                        <td>-</td>
                        <td><span class="badge badge-warning">Pendiente</span></td>
                    </tr>
                    <tr>
                        <td>#PAG-520</td>
                        <td>Carlos Muñoz</td>
                        <td>#2024-1520</td>
                        <td>Transferencia</td>
                        <td>$21,000</td>
                        <td>20/10/2025</td>
                        <td><span class="badge badge-danger">Vencido</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// Generate Consumos Content
function generateConsumos() {
    return `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Registro de Consumos</h2>
                <button class="btn btn-primary" onclick="alert('Registrar nueva lectura de medidor')">+ Nueva Lectura</button>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Medidor N°</th>
                        <th>Lectura Anterior</th>
                        <th>Lectura Actual</th>
                        <th>Consumo (m³)</th>
                        <th>Fecha Lectura</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>María González</td>
                        <td>MED-001</td>
                        <td>1,245 m³</td>
                        <td>1,263.5 m³</td>
                        <td>18.5</td>
                        <td>24/10/2025</td>
                        <td>
                            <button class="btn-icon" onclick="alert('Editar lectura MED-001')" title="Editar">✏️</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Juan Pérez</td>
                        <td>MED-002</td>
                        <td>2,108 m³</td>
                        <td>2,130.3 m³</td>
                        <td>22.3</td>
                        <td>24/10/2025</td>
                        <td>
                            <button class="btn-icon" onclick="alert('Editar lectura MED-002')" title="Editar">✏️</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Ana Rodríguez</td>
                        <td>MED-003</td>
                        <td>845 m³</td>
                        <td>859.8 m³</td>
                        <td>14.8</td>
                        <td>23/10/2025</td>
                        <td>
                            <button class="btn-icon" onclick="alert('Editar lectura MED-003')" title="Editar">✏️</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Carlos Muñoz</td>
                        <td>MED-004</td>
                        <td>1,523 m³</td>
                        <td>1,548 m³</td>
                        <td>25.0</td>
                        <td>22/10/2025</td>
                        <td>
                            <button class="btn-icon" onclick="alert('Editar lectura MED-004')" title="Editar">✏️</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// Generate Reportes Content
function generateReportes() {
    return `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Generador de Reportes</h2>
            </div>
            <div class="dashboard-grid">
                <button class="btn btn-primary" onclick="alert('Generando reporte de facturación...\nFormato: PDF\nPeríodo: Último mes')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <span style="font-size: 2rem;">📊</span>
                        <span>Reporte de Facturación</span>
                        <small style="opacity: 0.7;">Ingresos y cobros mensuales</small>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Generando reporte de consumos...\nFormato: PDF\nPeríodo: Último mes')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <span style="font-size: 2rem;">💧</span>
                        <span>Reporte de Consumos</span>
                        <small style="opacity: 0.7;">Análisis de uso de agua</small>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Generando reporte de morosidad...\nFormato: PDF\nUsuarios con deuda: 15')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <span style="font-size: 2rem;">⚠️</span>
                        <span>Reporte de Morosidad</span>
                        <small style="opacity: 0.7;">Usuarios con deuda</small>
                    </div>
                </button>
                <button class="btn btn-primary" onclick="alert('Generador de reporte personalizado\n\nSeleccione los parámetros que desea incluir en el reporte.')" style="padding: 1.5rem;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <span style="font-size: 2rem;">🔧</span>
                        <span>Reporte Personalizado</span>
                        <small style="opacity: 0.7;">Selecciona parámetros</small>
                    </div>
                </button>
            </div>
        </div>
    `;
}

// Generate Configuracion Content
function generateConfiguracion() {
    return `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Configuración del Sistema</h2>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div>
                    <h3 style="margin-bottom: 0.5rem;">Tarifas</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Tarifa Base ($/m³)</label>
                            <input type="number" value="650" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Cargo Fijo Mensual</label>
                            <input type="number" value="3500" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="margin-bottom: 0.5rem;">Fechas de Corte</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Día de Lectura</label>
                            <input type="number" value="15" min="1" max="31" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Día de Vencimiento</label>
                            <input type="number" value="25" min="1" max="31" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="margin-bottom: 0.5rem;">Información del Comité APR</h3>
                    <div style="display: grid; gap: 1rem;">
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Nombre del Comité</label>
                            <input type="text" value="Comité APR Villa Hermosa" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">RUT</label>
                            <input type="text" value="65.123.456-7" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                        <div>
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Dirección</label>
                            <input type="text" value="Camino Rural Km 5" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--input-background);">
                        </div>
                    </div>
                </div>

                <button class="btn btn-primary" onclick="alert('✅ Configuración guardada exitosamente')" style="width: fit-content;">Guardar Cambios</button>
            </div>
        </div>
    `;
}

// Simulate real-time data updates
function updateStats() {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        // Aquí podrías actualizar con datos reales desde una API
        console.log('Actualizando estadísticas...');
    });
}

// Update every 30 seconds
setInterval(updateStats, 30000);