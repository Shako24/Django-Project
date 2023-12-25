//Switcher function:
function timeList(el) {
    //Spot switcher:
    $(el).parent().parent().parent().parent().find(".timeList").removeClass("time-active");

    $(el).addClass("time-active");

    // Setting inputs for house Keeping cart
    $(el).parent().parent().parent().parent().find(".startDate").prop('disabled', true);
    $(el).parent().parent().find("input").prop('disabled', false);
    jQuery('#oneTimeBooking').val($(el).val());

    jQuery('#appointmentDate').val($(el).parent().parent().find("input").val());
    jQuery('#appointmentTime').val(jQuery('#oneTimeBooking').val()+':00');

  }

