import { getData, postData, putData } from '../utils/fetchUtils.js';

export async function createApi(formData, csrfToken) {
    return postData(
        '/caminho/da/api', 
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