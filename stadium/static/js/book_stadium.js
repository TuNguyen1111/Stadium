$(document).ready(function() {
    showNotificationModal()
    toggleSearchAndOrderForm()
    setEventForOrderBtn()
    checkUserIsAuthenticated()
})


function showNotificationModal() {
    if ( $('#success').length ) {
        $('#notification-success').modal('show')
    }
    else if ( $('#warning').length ) {
        $('#notification-failed').modal('show')
        setTimeout(function() {
            $('#warning').remove()
        },2000)
    }
}

function toggleSearchAndOrderForm() {
    $('.search-btn-dropdown').click(function() {
        $('.search-show').slideToggle()
    })
}

function setEventForOrderBtn() {
    $('.order-btn').click(function(e) {
        let currentItem = $(e.target)
        let stadiumName = currentItem.attr('stadium-name')
        let userName = currentItem.attr('user-name')
        let userPhoneNumber = currentItem.attr('user-phone-number')
        let timeframe = currentItem.attr('time-frame')
        let stadiumId = currentItem.attr('stadium-id')
        let timeframeInput = $('.form-order #time_frame')

        $('#stadium-name').val(stadiumName)
        $('#id_customer_name').val(userName)
        $('#id_customer_phone_number').val(userPhoneNumber)
        $('#id_stadium_id').val(stadiumId)

        console.log($('#id_stadium_id'))

        if (timeframe) {
            timeframeInput.val(timeframe)
        }

        if (userName) {
            $('#id_customer_name').val(userName)
            $('#id_customer_phone_number').val(userPhoneNumber)
        }
        $('#book-stadium').modal('show')
    })
}

function checkUserIsAuthenticated() {
    $('#stadium-detail').click(function(e) {
        if ($('#user-id').val() === 'None' ) {
            e.preventDefault()
            // console.log(typeof $('#user-id').val(), $('#user-id').val())
            $('#login-modal').modal('show')
        }
    })
}
