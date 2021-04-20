var dropdownForm = document.getElementById('dropdown-form')
var dropdownBtn = document.getElementById('dropdown-btn')
var message = document.querySelectorAll('#message')
var notifModal = new bootstrap.Modal(document.getElementById('notification'))
if (message.length) {
    notifModal.show()
}

function focusForm(e) {
    stadiumName = e.target.getAttribute('stadium-name')
    stadiumInput = document.getElementById('stadium-name')
    stadiumInput.value = stadiumName
    console.log(stadiumInput.value )
}

function checkInputField(e) {
    stadiumNameSearch = document.getElementById('stadium-name-search')
    addressSearch = document.getElementById('address')
    console.log("Adfdasfasdfadsf")

}
