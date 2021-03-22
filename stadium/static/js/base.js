var modalLogin = new bootstrap.Modal(document.getElementById('login'));
var modalRegister = new bootstrap.Modal(document.getElementById('register'));

function turnOnModalLogin() {
    modalLogin.show();
}

function turnOnModalRegister() {
    modalLogin.hide();
    modalRegister.show();
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }