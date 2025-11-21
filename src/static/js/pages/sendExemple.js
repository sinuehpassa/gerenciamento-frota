import { createApi } from '../api/apiExemples.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formCadastrar'); // puxa o formulário pelo ID
    const csrfToken = document.getElementById('csrf_token').value; // puxa o token CSRF do input hidden

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form); // cria um FormData com os dados do formulário
        const data = Object.fromEntries(formData.entries()); // converte FormData para objeto simples

        try {
            const novoRegistro = await createApi(data, csrfToken); // chama a função da API para criar o produto
        } catch (error)  { // trata erros
            console.error('Erro ao registrar:', error); // loga o erro no console
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById("formPut");
    
});