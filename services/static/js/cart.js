// New Cart
// https://codepen.io/ziga-miklic/pen/noZoLo


var check = false;

function changeVal(el) {
  var qt = parseFloat(el.parent().children(".qt").val());
  var price = parseFloat(el.parent().children(".price").html());
  var eq = Math.round(price * qt * 100) / 100;

  
  el.parent().children(".full-price").html( eq + " AED" );
  
  changeTotal();			
}



async function changeTotal(form) {
  
  var price = 0;
  
  $(".full-price").each(function(index){
    price += parseFloat($(".full-price").eq(index).html());
  });
  
  price = Math.round(price * 100) / 100;
  var tax = Math.round(price * 0.05 * 100) / 100
  var fullPrice = Math.round((price + tax ) *100) / 100;
  
  if(price == 0) {
    fullPrice = 0;
  }
  
  $(".subtotal span").html(price);
  $(".tax span").html(tax);
  $(".total span").html(fullPrice);

  
}



$(document).ready(function(){
  
  $(".remove").click(function(){
    var el = $(this);
    el.parent().parent().parent().addClass("removed");

    el.parent().parent().parent().find('input[type=hidden]').prop('disabled', false);


    $('#cart-update-form').submit();

    window.setTimeout(
      function(){
        el.parent().parent().parent().slideUp('fast', function() { 
          el.parent().parent().parent().remove(); 
          if($(".product").length == 0) {
            if(check) {
              $("#cart").html("<h1>The shop does not function, yet!</h1><p>If you liked my shopping cart, please take a second and heart this Pen on <a href='https://codepen.io/ziga-miklic/pen/xhpob'>CodePen</a>. Thank you!</p>");
            } else {
              $("#cart").html("<h1>No products!</h1>");
            }
          }
          changeTotal(); 
        });
      }, 200);

  })


});

//   $(".qt-plus").click(function(){
//     $(this).parent().children(".qt").val(parseInt($(this).parent().children(".qt").val()) + 1);
    
//     $(this).parent().children(".full-price").addClass("added");
    
//     var el = $(this);
//     window.setTimeout(function(){el.parent().children(".full-price").removeClass("added"); changeVal(el);}, 150);
//   });
  
//   $(".qt-minus").click(function(){
    
//     child = $(this).parent().children(".qt");
    
//     if(parseInt(child.val()) > 1) {
//       child.val(parseInt(child.val()) - 1);
//     }
    
//     $(this).parent().children(".full-price").addClass("minused");
    
//     var el = $(this);
//     window.setTimeout(function(){el.parent().children(".full-price").removeClass("minused"); changeVal(el);}, 150);
//   });
  
//   window.setTimeout(function(){$(".is-open").removeClass("is-open")}, 1200);
  
//   $(".btn").click(function(){
//     check = true;
//     $(".remove").click();
//   });
// });
