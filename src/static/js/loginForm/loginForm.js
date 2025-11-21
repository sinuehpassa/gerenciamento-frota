    document.addEventListener('DOMContentLoaded', function() {
        // Limpa os inputs apenas se houver mensagem de erro
        const alertDanger = document.querySelector('.alert-danger');
        if (alertDanger) {
            const inputs = document.querySelectorAll('.form-control');
            inputs.forEach(input => input.value = '');
        }
    });