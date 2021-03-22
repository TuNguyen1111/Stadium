var modalLogin = new mdb.Modal(document.getElementById('login'));
var modalRegister = new mdb.Modal(document.getElementById('register'));

function turnOnModalLogin() {
    modalLogin.show();
}

function turnOnModalRegister() {
    modalLogin.hide();
    modalRegister.show();
}