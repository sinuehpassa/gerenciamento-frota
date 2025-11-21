      const userListBody = document.getElementById("userListBody");
      async function fetchUsers() {
        try {
          const fetchUsers = await fetch('/api/users/list');
          const users = await fetchUsers.json();
          userListBody.innerHTML = '';
users.forEach(user => {
  const row = document.createElement('tr');
  row.innerHTML = `
    <td class="px-4 py-2">${user.username}</td>
    <td class="px-4 py-2">${user.email}</td>
    <td class="px-4 py-2">${user.roles.join(', ')}</td>
    <td class="px-4 py-2">
      <div class="flex gap-2 justify-end">
        <button class="rounded bg-red-600 text-white px-3 py-1 text-xs font-medium hover:bg-red-400" onclick="deletarUsuario('${user.email}')">Deletar</button>
        <button class="rounded bg-yellow-400 text-gray-900 px-3 py-1 text-xs font-medium hover:bg-yellow-200" onclick="editarUsuario('${user.email}')">Editar</button>
      </div>
    </td>
  `;
  userListBody.appendChild(row);
});
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      }

document.getElementById("btnVoltarLista").addEventListener("click", function() {
    document.getElementById("editUser").style.display = "none";
    document.querySelector("table").style.display = "table";
});

document.addEventListener('DOMContentLoaded', function() {
  const csrfToken = document.querySelector('[name="csrf_token"]').value;

      window.deletarUsuario = async function(userEmail) {
        try {
          const response = await fetch(`/root/api/users/delete/${userEmail}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            }
          });
          if (response.ok) {
            alert('Usuário deletado com sucesso!');
            fetchUsers();
          } else {
            alert('Erro ao deletar usuário.');
          }
        } catch (error) {
          console.error('Error deleting user:', error);
        }
      }

window.editarUsuario = async function(userEmail) {
    try {
        const response = await fetch(`/root/api/users/${userEmail}`);
        if (!response.ok) {
            alert("Usuário não encontrado!");
            return;
        }
        const user = await response.json();

        document.getElementById("editUsernameUsuario").value = user.username;
        document.getElementById("editEmailUsuario").value = user.email;
        document.getElementById("editPasswordUsuario").value = "";
        document.getElementById("editEmailOriginal").value = user.email;
        document.getElementById("editIsAdmin").checked = user.roles.includes("admin");
        document.getElementById("editIsUser").checked = user.roles.includes("user");

        document.querySelector("table").style.display = "none";
        document.getElementById("title").style.display = "none"; 
        document.getElementById("editUser").style.display = "block";
    } catch (error) {
        alert("Erro ao buscar usuário para edição.");
        console.error(error);
    }
};

document.getElementById("btnVoltarLista").addEventListener("click", function() {
    document.getElementById("editUser").style.display = "none";
    document.querySelector("table").style.display = "table";
    document.getElementById("title").style.display = "block";
});

document.getElementById("formEditarUsuario").addEventListener("submit", async function(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name="csrf_token"]').value;
    const novoUsername = document.getElementById("editUsernameUsuario").value;
    const novoEmail = document.getElementById("editEmailUsuario").value;
    const novoPassword = document.getElementById("editPasswordUsuario").value;
    const role = document.getElementById("editIsAdmin").checked ? "admin" : "user";
    const userEmail = document.getElementById("editEmailOriginal").value; 

    try {
        const response = await fetch(`/root/api/put/users/${userEmail}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                username: novoUsername,
                email: novoEmail,
                password: novoPassword,
                role: role
            })
        });
        if (response.ok) {
            alert('Usuário editado com sucesso!');
            document.getElementById("formEditarUsuario").reset();
            document.getElementById("editUser").style.display = "none";
            document.querySelector("table").style.display = "table";
            fetchUsers();
        } else {
            alert('Erro ao editar usuário.');
        }
    } catch (error) {
        console.error('Error editing user:', error);
    }
});
  fetchUsers();
});