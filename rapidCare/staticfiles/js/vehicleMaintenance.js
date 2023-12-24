/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
function filterFunction(input) {
    var filter, list, txtValue, list_item, i;
    filter = input.value.toUpperCase();
    list = $(input).parent().find('ul');
    list_item = $(list).children();

    for (i = 0; i < list_item.length; i++) {
        txtValue = list_item[i].textContent || list_item[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
        list_item[i].style.display = "";
        } else {
        list_item[i].style.display = "none";
        }
    }
}

$('.list-group-item').click(function() {
    value = $(this).attr('value');
    $(this).parent().parent().parent().find('button').html('<span class="d-inline-block w-75">'+value+'</span>');
    input = $(this).parent().parent().find('input[type=hidden]');
    console.log($(input).attr('name'));
    $(input).val(value);
    $(this).parent().parent().find('input[type=submit]').click();
})


