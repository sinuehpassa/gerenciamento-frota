import { getData, postData, putData } from '../utils/fetchUtils.js';

export async function registerVehicle(formData, csrfToken) {
    return postData(
        '/admin/register/vehicle', 
        formData,
        { 'X-CSRF-Token': csrfToken }
    );
}

export async function fetchVehicles() {
    return getData('/users/all/vehicles');
}

export async function updateApi(formData, csrfToken) {
    return putData(
        '/caminho/da/api',
        formData,
        { 'X-CSRF-Token': csrfToken }
    );
}