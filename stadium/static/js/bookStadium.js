var dropdownForm = document.getElementById('dropdown-form')
var dropdownBtn = document.getElementById('dropdown-btn')
var message = document.querySelectorAll('#message')
var notifModal = new bootstrap.Modal(document.getElementById('notification'))
console.log(notifModal)
if (message.length) {
    notifModal.show()
    console.log("dsfsdfds")
}

function focusForm(e) {
    stadiumName = e.target.getAttribute('stadium-name')
    stadiumInput = document.getElementById('stadium-name')
    stadiumInput.value = stadiumName
    // $('.dropdown-toggle').dropdown('toggle')
}
