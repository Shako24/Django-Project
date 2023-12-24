$('.car-select').click(function() {
    $(this).parent().find(".car-select").removeClass("selected");
    $(this).addClass("selected");

    $(this).parent().find("#car_select").val($(this).attr('data-value'));
    console.log($('#car_select').val());
    $('#table-val-1').html($('#car_select').val())
    // console.log($('#table-val-1').html())
})


$('.wash-btn-minus').click(function() {
    const currVal = $(this).parent().find('input').val()
    if (currVal == 12) {
        $(this).parent().find('input').val('8');
    }
    else if (currVal == 8) {
        $(this).parent().find('input').val('4');
    }
    else if (currVal == 4) {
        $(this).parent().find('input').val('2');
    }

    if ($(this).parent().find('input').attr('name') == 'interiorCleaning' ) {
        if (currVal == 2) {
            $(this).parent().find('input').val('1');
        }
        else if (currVal == 1) {
            $(this).parent().find('input').val('0');
        }
    }

    if ($(this).parent().find('input').attr('name') == 'basicExteriorWash' ) {
        $('#table-val-2').html($(this).parent().find('input').val()); 
    }
    else {
        $('#table-val-3').html($(this).parent().find('input').val());

    }
})

$('.wash-btn-plus').click(function() {
    const currVal = $(this).parent().find('input').val()

    if ($(this).parent().find('input').attr('name') == 'interiorCleaning' ) {
        if (currVal == 0) {
            $(this).parent().find('input').val('1');
        }
        else if (currVal == 1) {
            $(this).parent().find('input').val('2');
        }
    }
    if (currVal == 2) {
        $(this).parent().find('input').val('4');
    }
    else if (currVal == 4) {
        $(this).parent().find('input').val('8');
    }
    else if (currVal == 8) {
        $(this).parent().find('input').val('12');
    }

    if ($(this).parent().find('input').attr('name') == 'basicExteriorWash' ) {
        $('#table-val-2').html($(this).parent().find('input').val()); 
    }
    else {
        $('#table-val-3').html($(this).parent().find('input').val());

    }
})

$(document).on('load', function() {
    $('#table-val-1').change(function() {
        console.log('table changed')
        var price = 0
        if ($('#table-val-1').val() == 'Sedan') {
            price += parseInt($('#table-val-2').val()) * 22;
            price += parseInt($('#table-val-3').val()) * 15;
        }
        else if ($('#table-val-3').val() == 'SUV') {
            price += parseInt($('#table-val-2').val()) * 27;
            price += parseInt($('#table-val-3').val()) * 17;
        }

        $('#table-val-4').hmtl(price);
    })
})

$(document).on('submit', '#formPost', function (e) {
    e.preventDefault();
    var myform = $("#formPost")[0]
    var formData = new FormData(myform);
    console.log(formData);
})
    




