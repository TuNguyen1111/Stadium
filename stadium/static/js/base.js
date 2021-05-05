$(document).ready(function(){
    $('.manage-btn').click(function() {
        $('ul li .first').toggleClass('rotate');
        $('.stadium-manage').slideToggle();
    });

    $('.state-btn').click(function() {
        $('ul li .second').toggleClass('rotate');
        $('.stadium-state').slideToggle();
    });

    $('.toggle-login-modal').click(function() {
        $('#login-modal').modal('show');
    });

    $('.toggle-register-modal').click(function() {
        $('#login-modal').modal('hide');
        $('#register-modal').modal('show');
    });

    if ( $('#error_1_id_email_or_phone').length ) {
        $('#register-modal').modal('show');
        console.log($('#error_1_id_email_or_phone'))
    }

    if ( $(`#message-info`).length ) {
        $('#login-modal').modal('show');
    }
})

