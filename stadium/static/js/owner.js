// var inputs = document.querySelectorAll('input')

// for (let i = 1; i < inputs.length; i++) {
//     inputs[i].disabled = true
// }




function turnOnModalDelete(id) {
    var modalDelete = new bootstrap.Modal(document.getElementById(id));
    modalDelete.show();
}

function turnOnModalAccept(id) {
    var modalAccept = new bootstrap.Modal(document.getElementById(id));
    modalAccept.show();
}
