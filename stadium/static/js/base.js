$(document).ready(function(){
    setEventForButtonInSidebar()
    setEventForLoginAndRegisterBtn()
    showModalIfHaveError() 
    addClassForSelectType()
    setPropertyIfNoSidebar()
    clearMessage()
})

function clearMessage() {
    let message = $('#message')
    if (message.length) {
        setTimeout(function() {
            message.remove()
        }, 2000)
    }
}

function setEventForButtonInSidebar() {
    $('.manage-btn').on('click', function() {
        $('ul li .first').toggleClass('rotate')
        $('.stadium-manage').slideToggle()
    })

    $('.state-btn').on('click', function() {
        $('ul li .second').toggleClass('rotate')
        $('.stadium-state').slideToggle()
    })
}

function setEventForLoginAndRegisterBtn() {
    $('.toggle-login-modal').on('click', function() {
        $('#login-modal').modal('show')
    })

    $('.toggle-register-modal').on('click', function() {
        $('#login-modal').modal('hide')
        $('#register-modal').modal('show')
    })
}

function showModalIfHaveError() {
    if ( $('#error_1_id_email_or_phone').length ) {
        $('#register-modal').modal('show')
    }

    if ( $(`#message-error`).length ) {
        $('#login-modal').modal('show')
    }
}

function addClassForSelectType() {
    $('.select').addClass('form-select')
}

function setPropertyIfNoSidebar() {
    if (!$('#sidebar').length) {
        $('.col').css('marginLeft', '0')
    }
}