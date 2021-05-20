$(document).ready(function() {
    function showNotificationModal() {
        if ( $('#success').length ) {
            $('#notification-success').modal('show');
        }
        else if ( $('#warning').length ) {
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



