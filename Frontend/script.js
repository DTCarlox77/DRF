const authToken = localStorage.getItem('authToken');

let pagina = 1;
const container = document.querySelector('#contenedor');
const paginador = document.querySelector('#pagination');
const alertContainer = document.querySelector('#alertcontainer');

function getSongs(page) {

    fetch(`http://localhost:8000/api/songs/?page=${page}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('No se pudo llevar a cabo la consulta');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        insertSongs(data.results);
        setupPagination(data.count, page);
    })
    .catch(error => {
        console.error(error);
    });
}

function insertSongs(data) {
    container.innerHTML = '';
    data.forEach(song => {
        container.innerHTML += `
        <div class="card" style="width: 18rem;">
        <img src="${song.image}" class="card-img-top" alt="...">
            <div class="card-body">
                <h3>${song.name}</h3>
                <h6>Artista(s):</h6>
                <p class="card-text">${song.artist}</p>
                <h6>Descripción:</h6>
                <p class="card-text">${song.description}</p>
            </div>
        </div>
        `;
    });
}

function setupPagination(totalItems, currentPage) {
    const itemsPerPage = 4;
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    paginador.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === currentPage ? 'active' : ''}`;
        li.innerHTML = `
            <a class="page-link" href="#">${i}</a>
        `;
        li.addEventListener('click', (event) => {
            event.preventDefault();
            document.querySelector('.page-item.active').classList.remove('active');
            li.classList.add('active');
            getSongs(i);
        });
        paginador.appendChild(li);
    }
}

getSongs(pagina);

const buttonAdd = document.querySelector('#addsong');

buttonAdd.addEventListener('click', (event) => {
    event.preventDefault();
    const name = document.querySelector('#songname').value;
    const artist = document.querySelector('#songartist').value;
    const image = document.querySelector('#songimage').value;
    const description = document.querySelector('#songdescription').value;

    if (!name || !artist || !image || !description) {
        alertContainer.innerHTML = `
        <div class="alert alert-danger">
            <h2>Error</h2>
            <p>Asegúrate de completar todos los campos</p>
        </div>
    `;
    } else {
        fetchSong(JSON.stringify({
            "name": name,
            "artist": artist,
            "description": description,
            "image": image
        }));
    }
});

function fetchSong(data) {

    alertContainer.innerHTML = '';
    fetch('http://localhost:8000/api/songs/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        console.log(response);
        if (!response.ok) {
            return response.json().then(errorData => {
                alertContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <h2>Error</h2>
                        <p>${Object.values(errorData).join(' ')}</p>
                    </div>
                `;
                throw new Error('No se pudo llevar a cabo la consulta');
            });
        } else {
            alertContainer.innerHTML = `
                <div class="alert alert-success">
                    <h2>Éxito</h2>
                    <p>La canción se agregó exitosamente</p>
                </div>
            `;
            document.querySelector('#songname').value = '';
            document.querySelector('#songartist').value = '';
            document.querySelector('#songimage').value = '';
            document.querySelector('#songdescription').value = '';
            getSongs(pagina);
        }
    })
    .catch(error => {
        console.error(error);
    });
}

const loginform = document.querySelector('#loginform');
const loginformtitle = document.querySelector('#loginformtitle');
const loginbutton = document.querySelector('#loginuser');

const closesession = document.querySelector('#closesession');

closesession.addEventListener('click', (event) => {
    event.preventDefault();
    fetch('http://localhost:8000/api/logout/', {
        method : 'POST',
        headers : {
            Authorization : `Token ${localStorage.getItem('authToken')}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al cerrar sesión');
        }

        loginform.style.display = 'block';
        loginformtitle.style.display = 'block';
        closesession.style.display = 'none';
        localStorage.removeItem('authToken');
    });
});

if (authToken) {
    loginform.style.display = 'none';
    loginformtitle.style.display = 'none';
    closesession.style.display = 'block';
}

loginbutton.addEventListener('click', (event) => {
    event.preventDefault();
    const username = document.querySelector('#username');
    const password = document.querySelector('#password');

    fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({
                "username" : username.value,
                "password" : password.value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Algo salió mal');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.token) {
            localStorage.setItem('authToken', data.token);
        }
    })
    .catch(error => {
        console.error(error);
    });
});