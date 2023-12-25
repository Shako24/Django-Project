$('.house-hours').click(function() {
    $(this).parent().parent().find(".house-hours").removeClass("selected");
    $(this).addClass("selected");

    $(this).parent().parent().find("#hours").val($(this).attr('data-value'));
    console.log($('#hours').val());
    $('#table-val-1').html($('#hours').val())
})

$('.house-maids').click(function() {
    $(this).parent().parent().find(".house-maids").removeClass("selected");
    $(this).addClass("selected");

    $(this).parent().parent().find("#maids").val($(this).attr('data-value'));
    console.log($('#maids').val());
    $('#table-val-2').html($('#maids').val())
})

$('.house-supplies').click(function() {
    $(this).parent().find(".house-supplies").removeClass("selected");
    $(this).addClass("selected");

    $(this).parent().find("#supplies").val($(this).attr('data-value'));
    console.log($('#supplies').val());

    if ($('#supplies').val() == 'true') {
        $('#table-val-3').html('yes')
    } else {
        $('#table-val-3').html('no')
    }

})

$('.house-days').click(function() {
    $(this).parent().parent().find(".house-days").removeClass("selected");
    $(this).addClass("selected");

    $(this).parent().parent().find("#days").val($(this).attr('data-value'));
    console.log($('#days').val());
    $('#table-val-4').html($('#days').val())
})

