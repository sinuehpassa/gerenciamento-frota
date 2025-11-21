import { fetchVehicles } from '../api/usersApi.js';

document.addEventListener('DOMContentLoaded', () => {
    const hasVeiculosDiv = document.getElementById('veiculosEmUso') || document.getElementById('veiculosDisponiveis');
    if (hasVeiculosDiv) {
        initAllCars();
    }
    const hasVeiculosStatus = document.getElementById('veiculosStatus');
    if (hasVeiculosStatus) {
        initHomeCars();
    }
});

function initAllCars() {
    const veiculosEmUsoDiv = document.getElementById('veiculosEmUso');
    const veiculosDisponiveisDiv = document.getElementById('veiculosDisponiveis');
    fetchVehicles()
        .then(cars => {
            const { vehicles = [], message } = cars || {};
            if (veiculosEmUsoDiv) veiculosEmUsoDiv.innerHTML = '';
            if (veiculosDisponiveisDiv) veiculosDisponiveisDiv.innerHTML = '';
            const emUso = vehicles.filter(car => car.status === 'em uso');
            if (emUso.length > 0) {
                emUso.forEach(car => {
                    const card = document.createElement('div');
                    card.className = 'p-4 m-2 border max-w-[30vh] border-yellow-300 rounded-lg shadow bg-white flex flex-col gap-1';
                    card.innerHTML = `
                        <div class="font-bold text-yellow-900 text-lg">${car.model} (${car.year})</div>
                        <div class="text-yellow-700">Placa: <span class="font-mono">${car.plate}</span></div>
                        <div class="text-yellow-700">Status: <span class="font-semibold">${car.status}</span></div>
                        
                    `;
                    veiculosEmUsoDiv.appendChild(card);
                });
            } else if (message) {
                veiculosEmUsoDiv.innerHTML = `<div>${message}</div>`;
            }

            const disponiveis = vehicles.filter(car => car.status === 'disponível');
            if (disponiveis.length > 0) {
                disponiveis.forEach(car => {
                    const card = document.createElement('div');
                    card.className = 'p-4 m-2 border max-w-[30vh] border-green-300 rounded-lg shadow bg-white flex flex-col gap-1';
                    card.innerHTML = `
                        <div class="font-bold text-green-900 text-lg">${car.model} (${car.year})</div>
                        <div class="text-green-700">Placa: <span class="font-mono">${car.plate}</span></div>
                        <div class="text-green-700">Status: <span class="font-semibold">${car.status}</span></div>
                        <button class="bg-green-700 text-white px-2 py-1 rounded hover:bg-green-600 transition">Solicitar Veículo</button>
                    `;
                    veiculosDisponiveisDiv.appendChild(card);
                });
            } else if (message) {
                veiculosDisponiveisDiv.innerHTML = `<div>${message}</div>`;
            }})
        .catch(error => {
            if (veiculosEmUsoDiv) veiculosEmUsoDiv.innerHTML = `<div>Erro ao buscar veículos</div>`;
            if (veiculosDisponiveisDiv) veiculosDisponiveisDiv.innerHTML = `<div>Erro ao buscar veículos</div>`;
            console.error('Erro ao buscar veículos:', error);
        });}



function initHomeCars() {
    const veiculosStatus = document.getElementById('veiculosStatus');
    fetchVehicles()
        .then(cars => {
            const { disponivel = 0, em_uso = 0 } = cars || {};
            if (veiculosStatus) {
                veiculosStatus.innerHTML = `
                    <div class="text-green-800 font-bold">Veículos disponíveis: ${disponivel}</div>
                    <div class="text-yellow-600 font-bold">Veículos em uso: ${em_uso}</div>
                    <a href="/users/veiculos" class="text-blue-800 bg-blue-100 rounded border border-blue-800 px-2 py-1 inline-block mt-2">Ver todos os veículos</a>
                `;
            }
        })
        .catch(error => {
            if (veiculosStatus) veiculosStatus.innerHTML = '<div>Erro ao buscar status dos veículos</div>';
            console.error('Erro ao buscar status dos veículos:', error);
        });
}   
