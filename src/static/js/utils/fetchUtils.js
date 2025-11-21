async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const error = new Error(
            errorData.error ||
            errorData.erros?.[0] ||
            (errorData.errors ? Object.values(errorData.errors).flat().join('\n') : null) ||
            'Erro ao processar requisição'
        );
        error.error = errorData.error;
        error.erros = errorData.erros;
        // repassa errors do backend (marshmallow)
        if (errorData.errors) error.erros = errorData.errors;
        throw error;
    }
    return await response.json();
}

export async function postData(url, data, headers = {}) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
            body: JSON.stringify(data),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

export async function getData(url, headers = {}) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

export async function putData(url, data, headers = {}) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
            body: JSON.stringify(data),
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

export async function deleteData(url, headers = {}) {
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}