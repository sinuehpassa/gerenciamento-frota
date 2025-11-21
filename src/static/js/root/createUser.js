document.getElementById("formCriarUsuario").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("usernameUsuario").value;
    const email = document.getElementById("emailUsuario").value;
    const password = document.getElementById("passwordUsuario").value;
    const csrfToken = document.querySelector('[name="csrf_token"]').value;
    const isAdmin = document.getElementById("isAdmin").checked;
    const isUser = document.getElementById("isUser").checked;

    let url = "";
    let successMsg = "";

    if (isAdmin && !isUser) {
        url = "/root/api/criar/admin";
        successMsg = "Admin criado com sucesso: ";
    } else if (isUser && !isAdmin) {
        url = "/root/api/criar/usuario";
        successMsg = "Usuário criado com sucesso: ";
    } else {
        alert("Selecione apenas uma opção: Admin ou Usuário.");
        return;
    }

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Erro: " + data.error);
        } else {
            alert(successMsg + data.username);
            document.getElementById("formCriarUsuario", "userListContainer").reset();
            window.fetchUsers();
        }
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro de conexão: " + error.message);
    });
});