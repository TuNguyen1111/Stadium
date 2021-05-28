$(document).ready(function(){
    $('.manage-btn').on('click', function() {
        $('ul li .first').toggleClass('rotate');
        $('.stadium-manage').slideToggle();
    });

    $('.state-btn').on('click', function() {
        $('ul li .second').toggleClass('rotate');
        $('.stadium-state').slideToggle();
    });

    $('.toggle-login-modal').on('click', function() {
        $('#login-modal').modal('show');
    });

    $('.toggle-register-modal').on('click', function() {
        $('#login-modal').modal('hide');
        $('#register-modal').modal('show');
    });

    if ( $('#error_1_id_email_or_phone').length ) {
        $('#register-modal').modal('show');
    }

    if ( $(`#message-error`).length ) {
        $('#login-modal').modal('show');
    }

    console.log($('#sidebar').length)
    if (!$('#sidebar').length) {
        console.log('dsdfsdf')
        $('.col').css('marginLeft', '0')
    }

    $('#id_role').addClass('form-select')
})

