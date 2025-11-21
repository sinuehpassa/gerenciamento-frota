import { registerVehicle } from '../api/adminApi.js';

document.addEventListener('DOMContentLoaded', () => {
    initRegisterVehicle();
});

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