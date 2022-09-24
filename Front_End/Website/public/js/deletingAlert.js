//Permet d'avertir un utilisateur avant de supprimer une alerte
"use strict";

const article = document.getElementById('object');

if (object) {
    object.addEventListener('click', e => {
        if(e.target.className === 'btn btn-danger delete-article') {
            if(confirm('Vous êtes sûr de vouloir supprimer cette alerte ? Cette action est irréveresible.')) {
                const id = e.target.getAttribute('data-id');
                window.location.replace(`/object/delete/${id}`);
            }
        }
    });
}
