$(document).ready(function() {
    showNotificationModal();
    toggleSearchAndOrderForm();
    setEventForOrderBtn() 
})


function showNotificationModal() {
    if ( $('#success').length ) {
        $('#notification-success').modal('show');
    }
    else if ( $('#warning').length ) {
        $('#notification-failed').modal('show');
    };
}

function toggleSearchAndOrderForm() {
    $('.search-btn-dropdown').click(function() {
        $('.search-show').slideToggle();
    });
}

function setEventForOrderBtn() {
    $('.order-btn').click(function(e) {
        let currentItem = $(e.target)
        let stadiumName = currentItem.attr('stadium-name');
        let userName = currentItem.attr('user-name');
        let userPhoneNumber = currentItem.attr('user-phone-number');
        let timeframe = currentItem.attr('time-frame');

        let stadiumInput = $('#stadium-name');
        let userNameInput = $('#id_customer_name');
        let userPhoneNumberInput = $('#id_customer_phone_number');
        let timeframeInput = $('.form-order #time_frame');
        
        stadiumInput.val(stadiumName);
        userNameInput.val(userName);
        userPhoneNumberInput.val(userPhoneNumber);

        if ( timeframe ) {
            timeframeInput.val(timeframe);
        }

        if ( userName ) {
            userNameInput.val(userName);
            userPhoneNumberInput.val(userPhoneNumber);
        }
        
        $('#book-stadium').modal('show')
    })
}
