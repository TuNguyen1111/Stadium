$(document).ready(function() {
    function showNotificationModal() {
        if ( $('#success').length ) {
            $('#notification-success').modal('show');
        }
        else if ( $('#error').length ) {
            $('#notification-failed').modal('show');
        };
    }

    showNotificationModal();

    function toggleSearchAndOrderForm() {
        $('.search-btn-dropdown').click(function() {
            $('.search-show').slideToggle();
        });

        $('.order-btn-dropdown').click(function() {
            $('.order-show').slideToggle();
        });
    }

    toggleSearchAndOrderForm();


    $('.order-btn').click(function() {
        let stadiumName = $(this).attr('stadium-name');
        let userName = $(this).attr('user-name');
        let userPhoneNumber = $(this).attr('user-phone-number');
        let timeframe = $(this).attr('time-frame');

        let stadiumInput = $('#stadium-name');
        let userNameInput = $('#id_customer_name');
        let userPhoneNumberInput = $('#id_customer_phone_number');
        let timeframeInput = $('.form-order #time_frame');
        console.log(timeframeInput)
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

        $('.order-show').slideDown();
    })




})

// function focusForm(e) {
//     stadiumName = e.target.getAttribute('stadium-name')
//     userName = e.target.getAttribute('user-name')
//     userPhoneNumber = e.target.getAttribute('user-phone-number')
//     timeframe = e.target.getAttribute('time-frame')

//     stadiumInput = document.getElementById('stadium-name')
//     userNameInput = document.getElementById('id_customer_name')
//     userPhoneNumberInput = document.getElementById('id_customer_phone_number')
//     timeframeInput = document.querySelectorAll('#time_frame')
//     console.log(timeframeInput[1].value)
//     stadiumInput.value = stadiumName

//     if ( timeframe ) {
//         timeframeInput[1].value = timeframe
//     }

//     if ( userName ) {
//         userNameInput.value = userName
//         userPhoneNumberInput.value = userPhoneNumber
//     }
// }


