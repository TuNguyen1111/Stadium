// var inputs = document.querySelectorAll('input')

// for (let i = 1; i < inputs.length; i++) {
//     inputs[i].disabled = true
// }

var modalDelete = new bootstrap.Modal(document.getElementById('delete'));
var modalAccept = new bootstrap.Modal(document.getElementById('accept'));

function turnOnModalDelete() {
    modalDelete.show();
}

function turnOnModalAccept() {
    modalAccept.show();
}
