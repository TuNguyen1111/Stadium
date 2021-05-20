$(document).ready(function() {
    function turnOnModalDelete(id) {
        $(`delete ${id}`).modal('show')
    }

    function turnOnModalAccept(id) {
        $(`accept ${id}`).modal('show')
    }
})


function turnOnModalDelete(id) {
    var modalDelete = new bootstrap.Modal(document.getElementById(`delete ${id}`));
    modalDelete.show();
}

function turnOnModalAccept(id) {
    var modalAccept = new bootstrap.Modal(document.getElementById(`accept ${id}`));
    modalAccept.show();
}

function turnOnModalUpdate(e, id) {
    var modalUpdate = new bootstrap.Modal(document.getElementById(`update ${id}`));
    let getOrderid = e.target.getAttribute('order-id')
    let maxNumber = e.target.getAttribute('max-number')
    let orderIdInput = document.querySelectorAll('#id_order_id')
    let changeNumberFieldInput = document.querySelectorAll('.field_number')

    for (let item of changeNumberFieldInput) {
        item.setAttribute('max', maxNumber)
        item.setAttribute('min', 1)
    }

    for (let item of orderIdInput) {
        item.value = getOrderid
    }

    modalUpdate.show();
}



