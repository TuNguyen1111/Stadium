function turnOnModalDelete(id) {
    $(`#delete-${id}`).modal('show')
}

function turnOnModalAccept(id) {
    $(`#accept-${id}`).modal('show')
}

function turnOnModalUpdate(e, id) {
    let getOrderid = $(e.target).attr('order-id')
    let maxNumber = $(e.target).attr('max-number')
    let orderIdInput = $('[id=id_order_id]')
    let changeNumberFieldInput = $('.field_number')

    for (let item of changeNumberFieldInput) {
        $(item).attr('max', maxNumber)
        $(item).attr('min', 1)
    }

    for (let item of orderIdInput) {
        $(item).val(getOrderid)
    }

    $(`#update-${id}`).modal('show')
}



