$(document).ready(function(){
    $('#delete-order-btn').on('click', turnOnDeleteModal)
})

function turnOnDeleteModal() {
    $('#delete-order').modal('show')
}