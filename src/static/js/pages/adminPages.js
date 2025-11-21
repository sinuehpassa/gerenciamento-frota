import { registerVehicle } from '../api/adminApi.js';

document.addEventListener('DOMContentLoaded', () => {
    initRegisterVehicle();
    initAdminVehiclesTables();
});

import { fetchVehicles } from '../api/adminApi.js';

function initAdminVehiclesTables() {
    // Seleciona os TBODYs das tabelas pela ordem no HTML
    const allTables = document.querySelectorAll('table');
    const disponiveisBody = allTables[0] ? allTables[0].querySelector('tbody') : null;
    const emUsoBody = allTables[1] ? allTables[1].querySelector('tbody') : null;

    fetchVehicles()
        .then(cars => {
            const { vehicles = [] } = cars || {};
            if (disponiveisBody) disponiveisBody.innerHTML = '';
            if (emUsoBody) emUsoBody.innerHTML = '';
            // Disponíveis
            const disponiveis = vehicles.filter(car => car.status === 'disponível');
            disponiveis.forEach(car => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-4 py-2 border border-blue-900 border border-blue-800">${car.plate}</td>
                    <td class="px-4 py-2 border border-blue-900">${car.model}</td>
                    <td class="px-4 py-2 border border-blue-900">${car.year}</td>
                    <td class="px-4 py-2 border border-blue-900">-</td>
                `;
                if (disponiveisBody) disponiveisBody.appendChild(row);
            });
            // Em uso
            const emUso = vehicles.filter(car => car.status === 'em uso');
            emUso.forEach(car => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-4 py-2 border border-blue-900">${car.plate}</td>
                    <td class="px-4 py-2 border border-blue-900">${car.model}</td>
                    <td class="px-4 py-2 border border-blue-900">${car.year}</td>
                    <td class="px-4 py-2 border border-blue-900">-</td>
                `;
                if (emUsoBody) emUsoBody.appendChild(row);
            });
        })
        .catch(error => {
            if (disponiveisBody) disponiveisBody.innerHTML = '<tr><td colspan="4">Erro ao buscar veículos</td></tr>';
            if (emUsoBody) emUsoBody.innerHTML = '<tr><td colspan="4">Erro ao buscar veículos</td></tr>';
            console.error('Erro ao buscar veículos:', error);
        });
};

function initRegisterVehicle() {
    const registerForm = document.getElementById('registerVehicle');
    const csrfToken = document.getElementById('csrf_token').value;
    registerForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());

        registerVehicle(data, csrfToken)
            .then(response => {
                alert('Veículo registrado com sucesso!');
                registerForm.reset();
            })
            .catch(error => {
                function traduzErro(msg) {
                    if (msg.includes('Length must be 7')) return 'A placa deve ter 7 caracteres.';
                    if (msg.includes('Not a valid date')) return 'Ano inválido. Use apenas números (ex: 2020).';
                    if (msg.includes('Must be greater than or equal to')) return 'Ano deve ser maior ou igual a 1950.';
                    // Adicione outros casos conforme necessário
                    return msg;
                }
                if (error.erros) {
                    const mensagens = Object.values(error.erros).flat().map(traduzErro).join('\n');
                    alert(mensagens);
                } else if (error.error) {
                    alert(error.error);
                } else {
                    alert('Erro ao registrar veículo.');
                }
                console.error('Erro ao registrar veículo:', error);
            });
            });
        }