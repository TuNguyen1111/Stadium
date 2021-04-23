var dropdownForm = document.getElementById('dropdown-form')
var dropdownBtn = document.getElementById('dropdown-btn')
var successMessage = document.querySelectorAll('#success')
var failedMessage = document.querySelectorAll('#error')
var notificationSuccessModal = new bootstrap.Modal(document.getElementById('notification-success'))
var notificationFailedModal = new bootstrap.Modal(document.getElementById('notification-failed'))
console.log(failedMessage)
function turnOnNotificationModal() {
    if (successMessage.length) {
        notificationSuccessModal.show()
    }
    else if (failedMessage.length) {
        notificationFailedModal.show()
    }
}
turnOnNotificationModal()

function focusForm(e) {
    stadiumName = e.target.getAttribute('stadium-name')
    userName = e.target.getAttribute('user-name')
    userPhoneNumber = e.target.getAttribute('user-phone-number')
    timeframe = e.target.getAttribute('time-frame')

    stadiumInput = document.getElementById('stadium-name')
    userNameInput = document.getElementById('id_customer_name')
    userPhoneNumberInput = document.getElementById('id_customer_phone_number')
    timeframeInput = document.querySelectorAll('#time_frame')
    console.log(timeframeInput[1].value)
    stadiumInput.value = stadiumName
    timeframeInput[1].value = timeframe

    if ( userName ) {
        userNameInput.value = userName
        userPhoneNumberInput.value = userPhoneNumber
    }
}

function checkInputField(e) {
    stadiumNameSearch = document.getElementById('stadium-name-search')
    addressSearch = document.getElementById('address')
    console.log("Adfdasfasdfadsf")

}
