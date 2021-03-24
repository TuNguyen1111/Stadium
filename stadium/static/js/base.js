try {
  var modalLogin = new bootstrap.Modal(document.getElementById("login"));
  var modalRegister = new bootstrap.Modal(document.getElementById("register"));

  function turnOnModalLogin() {
    modalLogin.show();
  }

  function turnOnModalRegister() {
    modalLogin.hide();
    modalRegister.show();
  }
} catch(err) {}

var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function () {
    let arrow = this.querySelector("i");
    console.log(arrow);
    if (arrow.className == "fa fa-caret-down") {
      arrow.classList.remove("fa-caret-down");
      arrow.classList.add("fa-caret-up");
    } else {
      arrow.classList.remove("fa-caret-up");
      arrow.classList.add("fa-caret-down");
    }
    console.log(arrow);
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}
