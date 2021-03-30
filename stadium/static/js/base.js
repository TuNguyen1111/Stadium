var modalLogin = new bootstrap.Modal(document.getElementById('login'));
var modalRegister = new bootstrap.Modal(document.getElementById('register'));
var errorRegisterMessage = document.querySelectorAll(".invalid-feedback")
var errorLoginMessage = document.querySelectorAll('#error-message')

if (errorRegisterMessage.length) {
    modalRegister.show();
}


if (errorLoginMessage.length) {
    modalLogin.show();
}

function turnOnModalLogin() {
    modalLogin.show();
}

function turnOnModalRegister() {
    modalLogin.hide();
    modalRegister.show();
}

var dropdown = document.getElementsByClassName("dropdown-btn");

for (let i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    let arrow = this.querySelector("i")
    if (arrow.className == "fa fa-caret-down"){
        arrow.classList.remove("fa-caret-down")
        arrow.classList.add("fa-caret-up")
    }
    else{
      arrow.classList.remove("fa-caret-up")
      arrow.classList.add("fa-caret-down")
    }
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";

    } else {
      dropdownContent.style.display = "block";
    }
  });
}

var sidebarContent = document.querySelectorAll('.field-name')
for (let i = 0; i < sidebarContent.length; i++) {
    let item = sidebarContent[i]
    item.addEventListener('click', function(){
        this.style.background = 'red';
    })
}
