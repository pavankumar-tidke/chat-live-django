const switchers = [...document.querySelectorAll(".switcher")];

switchers.forEach((item) => {
  item.addEventListener("click", function () {
    switchers.forEach((item) =>
      item.parentElement.classList.remove("is-active")
    );
    this.parentElement.classList.add("is-active");
  });
});


// clearing error message
if($('#login_error_msg').text() != '') {
  setTimeout(() => {
    $('#login_error_msg').text('') 
  }, 3000);
}
