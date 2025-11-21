import { fetchVehicles } from '../api/usersApi.js';

document.addEventListener('DOMContentLoaded', () => {
    initAllCars();
});

function initAllCars() {
    const carsTableBody = document.getElementById('veiculosDisponiveis');
    fetchVehicles()
        .then(cars => {
            if (Array.isArray(cars) && cars.length > 0) {
                cars.forEach(car => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <div class="p-4 m-2 border border-gray-300 rounded-lg shadow bg-white flex flex-col gap-1 min-w-[220px]">
                        <div class="font-bold text-blue-900 text-lg">${car.model} (${car.year})</div>
                        <div class="text-gray-700">Placa: <span class="font-mono">${car.plate}</span></div>
                        <div class="text-gray-700">Status: <span class="font-semibold">${car.status}</span></div>
                    </div>
                    `;
                    carsTableBody.appendChild(row);
                });
            } else if (cars.message) {
                carsTableBody.innerHTML = `<tr><td colspan="5">${cars.message}</td></tr>`;
            }})
        .catch(error => {
            carsTableBody.innerHTML = `<tr><td colspan="5">Erro ao buscar veículos</td></tr>`;
            console.error('Erro ao buscar veículos:', error);
        });}

