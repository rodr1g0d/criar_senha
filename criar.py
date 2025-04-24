import secrets
import string

# Gera uma senha forte com 20 caracteres import as libs e seja feliz
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(20))
password

print(password)

# https://c340-187-101-169-197.ngrok-free.app
#Forwarding                    https://c340-187-101-169-197.ngrok-free.app -> http://localhost:4000                                                                                                                                              Connections                   ttl     opn     rt1     rt5     p50     p90                                                                             5       0       0.00    0.01    6.52    7.09                                                                                                                                                                      HTTP Requests                                                                                                           -------------                                                                                                                                                                                                                                   00:53:22.178 -12 GET /api/installations         304 Not Modified                                                        00:53:22.108 -12 GET /favicon.ico               304 Not Modified                                                        00:53:21.672 -12 GET /styles.css                304 Not Modified                                                        00:53:21.761 -12 GET /api/devices               304 Not Modified                                                        00:53:21.594 -12 GET /                          304 Not Modified                                                        00:53:21.675 -12 GET /script.js                 304 Not Modified                                                        00:52:44.680 -12 GET /api/devices               200 OK                                                                  00:52:44.761 -12 GET /favicon.ico               200 OK                                                                  00:52:44.821 -12 GET /api/installations         200 OK                                                                  00:52:43.775 -12 GET /                          200 OK
/*

// Script para o painel de gerenciamento de dispositivos Android

// Garantir que os arquivos de dados existem
const fs = require('fs');
if (!fs.existsSync('./data/devices.json')) {
    fs.writeFileSync('./data/devices.json', '[]', 'utf8');
}
if (!fs.existsSync('./data/installations.json')) {
    fs.writeFileSync('./data/installations.json', '[]', 'utf8');
}

console.log('Script MDM carregado!');

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips e popovers do Bootstrap
    initBootstrapComponents();
    
    // Carregar dados dos dispositivos
    loadDeviceData();
    
    // Adicionar event listeners
    setupEventListeners();
    
    // Atualização automática a cada minuto
    setInterval(updateDeviceStatus, 60000);
});

// Inicializar componentes do Bootstrap
function initBootstrapComponents() {
    // Inicializar tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Configurar event listeners para a interface
function setupEventListeners() {
    // Formulário de adicionar dispositivo
    const addDeviceForm = document.getElementById('addDeviceForm');
    if (addDeviceForm) {
        addDeviceForm.addEventListener('submit', handleAddDevice);
    }
    
    // Formulário de agendamento
    const scheduleInstallForm = document.getElementById('scheduleInstallForm');
    if (scheduleInstallForm) {
        scheduleInstallForm.addEventListener('submit', handleScheduleInstall);
    }
    
    // Filtro de pesquisa para tabelas
    const deviceFilter = document.getElementById('deviceFilter');
    if (deviceFilter) {
        deviceFilter.addEventListener('input', filterDevices);
    }
    
    // Botão de atualizar dados
    const refreshButton = document.getElementById('refreshData');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            loadDeviceData(true);
        });
    }
}

// Carregar dados dos dispositivos
function loadDeviceData(showNotification = false) {
    console.log('Iniciando carregamento de dispositivos...');
    fetch('/api/devices')
        .then(response => {
            console.log('Resposta recebida:', response.status);
            if (!response.ok) {
                throw new Error('Erro ao carregar dados');
            }
            return response.json();
        })
        .then(devices => {
            console.log('Dados recebidos:', devices);
            // Verificar se devices é um array (mesmo que vazio)
            if (Array.isArray(devices)) {
                updateDeviceTable(devices);
                updateSummaryCards(devices);
                // ... resto do código ...
            } else {
                console.error('Resposta não é um array:', devices);
                document.querySelector('#deviceTableBody').innerHTML = 
                    '<tr><td colspan="6">Erro no formato de dados</td></tr>';
            }
        })
        .catch(error => {
            console.error('Erro específico:', error);
            console.error('Erro ao carregar dispositivos:', error);
            document.querySelector('#deviceTableBody').innerHTML = 
                '<tr><td colspan="6">Erro ao carregar dispositivos</td></tr>';
        });
}

// Atualizar tabela de dispositivos
function updateDeviceTable(devices) {
    const tableBody = document.querySelector('#tabelaDispositivos tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    devices.forEach(device => {
        const lastSeenFormatted = formatDateTime(device.lastSeen);
        const statusClass = getStatusClass(device.status);
        const statusText = getStatusText(device.status);
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${device.name || 'N/A'}</td>
            <td>${device.deviceId || 'N/A'}</td>
            <td><span class="status-badge ${statusClass}">${statusText}</span></td>
            <td>${lastSeenFormatted}</td>
            <td>${device.version || 'N/A'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="showActionModal('${device.deviceId}')">
                    <i class="bi bi-gear"></i> Ações
                </button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Atualizar tabela de instalações pendentes
function updateInstallTable(installations) {
    const tableBody = document.querySelector('#tabelaInstalacoes tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    installations.forEach(install => {
        const scheduledFormatted = formatDateTime(install.scheduled);
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${install.id}</td>
            <td>${install.device}</td>
            <td>${install.app}</td>
            <td>${install.version}</td>
            <td>${scheduledFormatted}</td>
            <td><span class="badge bg-info">${install.status}</span></td>
            <td>
                <button class="btn btn-sm btn-outline-danger" data-install-id="${install.id}" data-action="cancel-install">
                    <i class="bi bi-x-circle"></i> Cancelar
                </button>
            </td>
        `;
        
        tableBody.appendChild(row);
        
        // Evento para o botão de cancelar
        const cancelBtn = row.querySelector('[data-action="cancel-install"]');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', handleCancelInstall);
        }
    });
}

// Atualizar cards de resumo
function updateSummaryCards(devices) {
    const totalDevices = devices.length;
    const onlineDevices = devices.filter(d => d.status === 'online').length;
    const lockedDevices = devices.filter(d => d.status === 'locked').length;
    
    updateCardValue('totalDevices', totalDevices);
    updateCardValue('onlineDevices', onlineDevices);
    updateCardValue('lockedDevices', lockedDevices);
}

// Atualizar valor em um card
function updateCardValue(cardId, value) {
    const valueElement = document.getElementById(cardId);
    if (valueElement) {
        valueElement.textContent = value;
    }
}

// Manipular ações nos dispositivos
function handleDeviceAction(e) {
    e.preventDefault();
    
    const deviceId = this.getAttribute('data-device-id');
    const action = this.getAttribute('data-action');
    
    switch (action) {
        case 'view':
            showDeviceDetails(deviceId);
            break;
        case 'lock':
            confirmAction(
                'Bloquear Dispositivo', 
                `Tem certeza que deseja bloquear o dispositivo ${deviceId}?`,
                () => lockDevice(deviceId)
            );
            break;
        case 'unlock':
            confirmAction(
                'Desbloquear Dispositivo', 
                `Tem certeza que deseja desbloquear o dispositivo ${deviceId}?`,
                () => unlockDevice(deviceId)
            );
            break;
        case 'wipe':
            confirmAction(
                'Limpar Dados', 
                `ATENÇÃO: Esta ação irá apagar todos os dados do dispositivo ${deviceId}. Esta ação não pode ser desfeita. Deseja continuar?`,
                () => wipeDevice(deviceId)
            );
            break;
        case 'install':
            showInstallModal(deviceId);
            break;
    }
}

// Manipulador para cancelar instalação
function handleCancelInstall() {
    const installId = this.getAttribute('data-install-id');
    
    confirmAction(
        'Cancelar Instalação', 
        `Tem certeza que deseja cancelar a instalação ${installId}?`,
        () => {
            // Simulação de cancelamento
            setTimeout(() => {
                this.closest('tr').remove();
                showAlert(`Instalação ${installId} cancelada com sucesso.`, 'success');
            }, 500);
        }
    );
}

// Manipulador para adicionar dispositivo
function handleAddDevice(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const deviceData = Object.fromEntries(formData.entries());
    
    // Simulação de adição
    const modal = bootstrap.Modal.getInstance(document.getElementById('addDeviceModal'));
    modal.hide();
    
    showAlert('Dispositivo adicionado com sucesso! O código de ativação foi enviado.', 'success');
    
    // Resetar formulário
    this.reset();
    
    // Recarregar dados após 1 segundo
    setTimeout(() => loadDeviceData(), 1000);
}

// Manipulador para agendar instalação
function handleScheduleInstall(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const installData = Object.fromEntries(formData.entries());
    
    // Simulação de agendamento
    const modal = bootstrap.Modal.getInstance(document.getElementById('scheduleModal'));
    modal.hide();
    
    showAlert('Instalação agendada com sucesso!', 'success');
    
    // Resetar formulário
    this.reset();
    
    // Recarregar dados após 1 segundo
    setTimeout(() => loadDeviceData(), 1000);
}

// Mostrar modal de detalhes do dispositivo
function showDeviceDetails(deviceId) {
    // Simulação de carregamento de detalhes
    const detailsBody = document.querySelector('#deviceDetailsModal .modal-body');
    detailsBody.innerHTML = '<div class="text-center py-3"><div class="spinner-border" role="status"></div><p>Carregando detalhes...</p></div>';
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('deviceDetailsModal'));
    modal.show();
    
    // Atualizar título
    document.querySelector('#deviceDetailsModal .modal-title').textContent = `Detalhes do Dispositivo: ${deviceId}`;
    
    // Simular recebimento de dados
    setTimeout(() => {
        detailsBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h5>Informações do Dispositivo</h5>
                    <table class="table table-sm">
                        <tr><td><strong>ID:</strong></td><td>${deviceId}</td></tr>
                        <tr><td><strong>Nome:</strong></td><td>Samsung Galaxy S21</td></tr>
                        <tr><td><strong>Modelo:</strong></td><td>SM-G991B</td></tr>
                        <tr><td><strong>Número de Série:</strong></td><td>R9ZN20ABCDE</td></tr>
                        <tr><td><strong>IMEI:</strong></td><td>123456789012345</td></tr>
                        <tr><td><strong>Versão Android:</strong></td><td>Android 11</td></tr>
                        <tr><td><strong>Nível de Patch:</strong></td><td>1 de Maio de 2023</td></tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <h5>Status</h5>
                    <table class="table table-sm">
                        <tr><td><strong>Status Atual:</strong></td><td><span class="status-badge status-online">Online</span></td></tr>
                        <tr><td><strong>Última Conexão:</strong></td><td>Hoje às 10:30</td></tr>
                        <tr><td><strong>Bateria:</strong></td><td>78%</td></tr>
                        <tr><td><strong>Armazenamento:</strong></td><td>64GB (48% usado)</td></tr>
                        <tr><td><strong>Endereço IP:</strong></td><td>192.168.1.45</td></tr>
                        <tr><td><strong>Usuário:</strong></td><td>Carlos Silva</td></tr>
                        <tr><td><strong>Departamento:</strong></td><td>Vendas</td></tr>
                    </table>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <h5>Aplicativos Instalados</h5>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Aplicativo</th>
                                <th>Versão</th>
                                <th>Instalado em</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Secure Browser</td>
                                <td>2.0.1</td>
                                <td>01/06/2023</td>
                            </tr>
                            <tr>
                                <td>Email Corporativo</td>
                                <td>3.5.2</td>
                                <td>28/05/2023</td>
                            </tr>
                            <tr>
                                <td>Antivírus</td>
                                <td>1.2.0</td>
                                <td>15/05/2023</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }, 1000);
}

// Mostrar modal de instalação
function showInstallModal(deviceId) {
    // Preencher o campo do dispositivo
    document.getElementById('installDeviceId').value = deviceId;
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('scheduleModal'));
    modal.show();
}

// Ações simuladas
function lockDevice(deviceId) {
    showActionProgress('Enviando comando de bloqueio...');
    
    // Fazer chamada de API real para bloquear dispositivo
    fetch(`/api/devices/${deviceId}/lock`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideActionProgress();
        if (data.success) {
            showAlert(`Dispositivo ${deviceId} bloqueado com sucesso.`, 'success');
        } else {
            showAlert(`Falha ao bloquear dispositivo: ${data.message}`, 'danger');
        }
        loadDeviceData();
    })
    .catch(error => {
        hideActionProgress();
        showAlert(`Erro ao bloquear dispositivo: ${error.message}`, 'danger');
        console.error('Erro ao bloquear dispositivo:', error);
    });
}

function unlockDevice(deviceId) {
    showActionProgress('Enviando comando de desbloqueio...');
    
    // Fazer chamada de API real para desbloquear dispositivo
    fetch(`/api/devices/${deviceId}/unlock`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideActionProgress();
        if (data.success) {
            showAlert(`Dispositivo ${deviceId} desbloqueado com sucesso.`, 'success');
        } else {
            showAlert(`Falha ao desbloquear dispositivo: ${data.message}`, 'danger');
        }
        loadDeviceData();
    })
    .catch(error => {
        hideActionProgress();
        showAlert(`Erro ao desbloquear dispositivo: ${error.message}`, 'danger');
        console.error('Erro ao desbloquear dispositivo:', error);
    });
}

function wipeDevice(deviceId) {
    // Simular limpeza de dispositivo
    showActionProgress('Enviando comando de limpeza...');
    
    setTimeout(() => {
        hideActionProgress();
        showAlert(`Comando de limpeza enviado para o dispositivo ${deviceId}.`, 'success');
        loadDeviceData();
    }, 2000);
}

// Mostrar progresso de ação
function showActionProgress(message) {
    const progressDiv = document.createElement('div');
    progressDiv.id = 'actionProgress';
    progressDiv.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-dark bg-opacity-50';
    progressDiv.style.zIndex = '9999';
    
    progressDiv.innerHTML = `
        <div class="card p-4">
            <div class="text-center">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <p class="mb-0">${message}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(progressDiv);
}

// Esconder progresso de ação
function hideActionProgress() {
    const progressDiv = document.getElementById('actionProgress');
    if (progressDiv) {
        progressDiv.remove();
    }
}

// Filtrar dispositivos na tabela
function filterDevices() {
    const filterValue = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#tabelaDispositivos tbody tr');
    
    tableRows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(filterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Atualizar status dos dispositivos (simulado)
function updateDeviceStatus() {
    // Simulação de atualização periódica dos status
    const statusBadges = document.querySelectorAll('.status-badge');
    const statuses = ['online', 'offline', 'locked'];
    
    // Aleatoriamente atualizar alguns dispositivos
    statusBadges.forEach(badge => {
        // 20% de chance de mudar o status
        if (Math.random() < 0.2) {
            const oldStatus = badge.classList.contains('status-online') ? 'online' : 
                             badge.classList.contains('status-offline') ? 'offline' : 'locked';
            
            // Escolher um novo status diferente do atual
            let newStatus;
            do {
                newStatus = statuses[Math.floor(Math.random() * statuses.length)];
            } while (newStatus === oldStatus);
            
            // Remover classe antiga
            badge.classList.remove(`status-${oldStatus}`);
            // Adicionar nova classe
            badge.classList.add(`status-${newStatus}`);
            // Atualizar texto
            badge.textContent = getStatusText(newStatus);
        }
    });
    
    // Atualizar resumo
    const deviceRows = document.querySelectorAll('#tabelaDispositivos tbody tr');
    const devices = [];
    
    deviceRows.forEach(row => {
        const statusCell = row.querySelector('.status-badge');
        let status = 'offline';
        
        if (statusCell.classList.contains('status-online')) status = 'online';
        else if (statusCell.classList.contains('status-locked')) status = 'locked';
        
        devices.push({ status });
    });
    
    updateSummaryCards(devices);
}

// Utilitários
function getStatusClass(status) {
    switch (status) {
        case 'online': return 'status-online';
        case 'offline': return 'status-offline';
        case 'locked': return 'status-locked';
        default: return '';
    }
}

function getStatusText(status) {
    switch (status) {
        case 'online': return 'Online';
        case 'offline': return 'Offline';
        case 'locked': return 'Bloqueado';
        default: return status;
    }
}

function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    return moment(date).format('DD/MM/YYYY HH:mm');
}

// Mostrar diálogo de confirmação
function confirmAction(title, message, onConfirm) {
    const confirmModal = document.getElementById('confirmModal');
    const confirmTitle = confirmModal.querySelector('.modal-title');
    const confirmMessage = confirmModal.querySelector('.modal-body');
    const confirmButton = confirmModal.querySelector('#confirmActionButton');
    
    confirmTitle.textContent = title;
    confirmMessage.textContent = message;
    
    // Remover handlers antigos
    const newConfirmButton = confirmButton.cloneNode(true);
    confirmButton.parentNode.replaceChild(newConfirmButton, confirmButton);
    
    // Adicionar novo handler
    newConfirmButton.addEventListener('click', () => {
        const modal = bootstrap.Modal.getInstance(confirmModal);
        modal.hide();
        onConfirm();
    });
    
    // Mostrar modal
    const modal = new bootstrap.Modal(confirmModal);
    modal.show();
}

// Mostrar mensagem de alerta
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) {
        // Criar container se não existir
        const container = document.createElement('div');
        container.id = 'alertContainer';
        document.body.appendChild(container);
    }
    
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    document.getElementById('alertContainer').insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto remover após 5 segundos
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            alertElement.classList.add('fade-alert');
            setTimeout(() => alertElement.remove(), 500);
        }
    }, 5000);
}

// Mostrar modal de ações para um dispositivo
function showActionModal(deviceId) {
    // Atualizar o ID do dispositivo no modal
    document.getElementById('deviceIdDisplay').textContent = deviceId;
    document.getElementById('currentDeviceId').value = deviceId;
    
    // Mostrar o modal
    const modal = new bootstrap.Modal(document.getElementById('modalAcoes'));
    modal.show();
}

// Função para bloquear dispositivo a partir do modal
function lockDeviceFromModal() {
    const deviceId = document.getElementById('currentDeviceId').value;
    if (!deviceId) {
        showAlert('ID do dispositivo não encontrado', 'danger');
        return;
    }
    
    // Fechar modal de ações
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalAcoes'));
    if (modal) modal.hide();
    
    // Confirmar e executar ação
    confirmAction(
        'Bloquear Dispositivo', 
        `Tem certeza que deseja bloquear o dispositivo ${deviceId}?`,
        () => lockDevice(deviceId)
    );
}

// Função para desbloquear dispositivo a partir do modal
function unlockDeviceFromModal() {
    const deviceId = document.getElementById('currentDeviceId').value;
    if (!deviceId) {
        showAlert('ID do dispositivo não encontrado', 'danger');
        return;
    }
    
    // Fechar modal de ações
    const modal = bootstrap.Modal.getInstance(document.getElementById('modalAcoes'));
    if (modal) modal.hide();
    
    // Confirmar e executar ação
    confirmAction(
        'Desbloquear Dispositivo', 
        `Tem certeza que deseja desbloquear o dispositivo ${deviceId}?`,
        () => unlockDevice(deviceId)
    );
}

*/
