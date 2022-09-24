//Permet d'avertir un utilisateur avant de supprimer son compte
"use strict";

const page = document.getElementById('mainblock');

if (mainblock) {
    mainblock.addEventListener('click', e => {
        if(e.target.className === 'btn btn-danger delete-user') {
            if(confirm('Vous êtes sûr de vouloir supprimer votre compte ? Cette action est irréveresible.')) {
                const id = e.target.getAttribute('data-id');
                window.location.replace(`/account/delete/${id}`);
            }
        }
    });
}