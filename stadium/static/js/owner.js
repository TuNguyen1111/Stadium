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

    for (let i = 0; i < changeNumberFieldInput.length; i++) {
        input = changeNumberFieldInput[i]
        input.setAttribute('max', maxNumber)
        input.setAttribute('min', 1)
    }

    for (let i = 0; i < orderIdInput.length; i++) {
        input = orderIdInput[i]
        input.value = getOrderid
    }


    modalUpdate.show();
}



