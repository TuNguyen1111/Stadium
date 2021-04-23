function turnOnModalDelete(id) {
    var modalDelete = new bootstrap.Modal(document.getElementById(`delete ${id}`));
    modalDelete.show();
}

function turnOnModalAccept(id) {
    var modalAccept = new bootstrap.Modal(document.getElementById(`accept ${id}`));
    modalAccept.show();
}
