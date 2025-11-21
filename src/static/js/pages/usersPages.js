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
                        <td>${car.model}</td>
                        <td>${car.year}</td>
                        <td>${car.license_plate}</td>
                        <td>${car.status}</td>
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

