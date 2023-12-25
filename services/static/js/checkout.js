const paymentButton = document.getElementById('paymentPortal');
const addressButton = document.getElementById('addressPortal');
const backaddressButton = document.getElementById('backAddressPortal');
const container = document.getElementById('container');

paymentButton.addEventListener('click', (e) => {
    e.preventDefault();
    // ($("input[name=addressesChoice]:checked").val())

    console.log($("#guestEmailInput").val(), $("#guestPhoneInput").val());

    if ($("input[name=addressesChoice]:checked").length > 0) { 
        $('#address-card>address').html($("input[name=addressesChoice]:checked").parent().find('label>address').html() +'<br/>'+$("#guestEmailInput").val() +'<br/>'+$("#guestPhoneInput").val());
        $('input[name=addressInput]').val($("input[name=addressesChoice]:checked").val());
        $('input[name=guestEmailInput]').val($('#guestEmailInput').val());
        $('input[name=guestPhoneInput]').val($('#guestPhoneInput').val());
        container.classList.add("right-panel-active");
    }
});

addressButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

backaddressButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});




