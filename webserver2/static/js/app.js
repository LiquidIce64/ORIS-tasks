const apiUrl = 'http://127.0.0.1:5000/api/users'; // URL API

    // Функция для получения всех объектов
    function fetchUsers() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const userList = document.getElementById('user-list');
                userList.innerHTML = ''; // Очищаем список перед добавлением новых данных
                data.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${user.id} - Username: ${user.username} - Display Name: ${user.display_name} - Password: ${user.password} - Email: ${user.email}`;

                    // Добавляем кнопку для обновления
                    const updateButton = document.createElement('button');
                    updateButton.className = "btn btn-secondary m-2"
                    updateButton.textContent = "Update";
                    updateButton.onclick = function() {
                        // При нажатии на "Update", заполняем поля для обновления
                        document.getElementById('update-id').value = user.id;
                        document.getElementById('update-username').value = user.username;
                        document.getElementById('update-display_name').value = user.display_name;
                        document.getElementById('update-password').value = user.password;
                        document.getElementById('update-email').value = user.email;
                    };
                    li.appendChild(updateButton);

                    // Добавляем кнопку для удаления
                    const deleteButton = document.createElement('button');
                    deleteButton.className = "btn btn-danger m-2"
                    deleteButton.textContent = "Delete";
                    deleteButton.onclick = function() {
                        // При нажатии на "Delete", удаляем объект
                        deleteUser(user.id);
                    };
                    li.appendChild(deleteButton);

                    userList.appendChild(li);
                });
            })
            .catch(error => displayError(error));
    }

    // Функция для создания нового объекта
    document.getElementById('create-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const display_name = document.getElementById('display_name').value;
        const password = document.getElementById('password').value;
        const email = document.getElementById('email').value;

        const body = JSON.stringify({ username, display_name, password, email });

        fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
    });

    // Функция для обновления объекта
    document.getElementById('update-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('update-id').value;
        const username = document.getElementById('update-username').value;
        const display_name = document.getElementById('update-display_name').value;
        const password = document.getElementById('update-password').value;
        const email = document.getElementById('update-email').value;

        const body = JSON.stringify({ username, display_name, password, email });

        fetch(`${apiUrl}/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: body
        })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
    });

    // Функция для удаления объекта
    function deleteUser(id) {
        fetch(`${apiUrl}/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
    }

    // Функция для отображения ответа от API
    function displayResponse(data) {
        const output = document.getElementById('response-output');
        output.textContent = JSON.stringify(data, null, 2);

        fetchUsers();
    }

    // Функция для обработки ошибок
    function displayError(error) {
        const output = document.getElementById('response-output');
        output.textContent = `Error: ${error}`;
    }

    fetchUsers();