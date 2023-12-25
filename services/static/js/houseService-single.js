/*
===============================================================

Hi! Welcome to my little playground!

My name is Tobias Bogliolo. 'Open source' by default and always 'responsive',
I'm a publicist, visual designer and frontend developer based in Barcelona. 

Here you will find some of my personal experiments. Sometimes usefull,
sometimes simply for fun. You are free to use them for whatever you want 
but I would appreciate an attribution from my work. I hope you enjoy it.

===============================================================
*/
//Global:
var survey = []; //Bidimensional array: [ [1,3], [2,4] ]
var textActive = false

//Switcher function:
$(".rb-tab").click(function(){
  //Spot switcher:
  $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
  $(this).addClass("rb-tab-active");

  // Setting inputs for house Keeping cart
  $(this).parent().find("input").val($(this).attr('data-value'));
  console.log($(this).parent().find("input").attr('name') + ' : ' + $(this).parent().find("input").val())
});

window.addEventListener('click', function(e){   
  if (document.getElementById('textarea_cleaning').contains(e.target) == false){
    // Clicked in box
    $(".rb-tab-3").removeClass("rb-tab-active");
  }
});

//Save data:
$(".trigger").click(function(){
  
});

