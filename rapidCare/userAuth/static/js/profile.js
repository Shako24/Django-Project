function edit() {
    editForm = document.getElementById('editChanges');
    saveForm = document.getElementById('saveChanges');

    editForm.style.display = 'none'
    saveForm.style.display = 'block'
}

function editPic() {
    profilePic = document.getElementById('profilePicInput');
    profilePic.click();
}

function changePic() {
  selectPic = document.getElementById('id_img')
  selectPic.click()
}

function changeProfileView() {
  document.getElementById('profileView').style.display='none'; 
  document.getElementById('editProfileView').style.display = 'block';
}

function changeEditProfileView() {
  document.getElementById('editProfileView').style.display='none'; 
  document.getElementById('profileView').style.display = 'block';
}

function suboption(el) {
  $(el).parent().find('input[type=hidden]').prop('disabled', false);
  $('#subscriptionChanges').submit();
}

// function renewsub(el) {
//   console.log($(el).val());
//   $('#subscriptionChanges').submit();
// }

$(window).on("load", function(){
  addresses = document.getElementsByClassName('removeAddress-btn');
  for (let i = 0; i < addresses.length; i++) {
    addresses[i].addEventListener("click", function(e){
      e.preventDefault();
      $(this).parent().parent().parent().append('<input type="hidden" name="'+$(this).attr('name')+'">')
      $(this).parent().parent().parent().addClass('removeAddress');
      $(this).parent().parent().parent().next().remove("hr")
      $(this).parent().parent().parent().slideUp()
    })
    
  }
})
  



// https://releases.jquery.com/   (add the jquerry script in the base.html for this js file to work) (Currently script is added)
// https://speckyboy.com/custom-file-upload-fields/
function readURL(input) {
    if (input.files && input.files[0]) {
  
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
  
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
  
        $('.image-title').html(input.files[0].name);
      };
  
      reader.readAsDataURL(input.files[0]);
  
    } else {
      removeUpload();
    }
  }
  
  function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
  }
  $('.image-upload-wrap').bind('dragover', function () {
      $('.image-upload-wrap').addClass('image-dropping');
    });
    $('.image-upload-wrap').bind('dragleave', function () {
      $('.image-upload-wrap').removeClass('image-dropping');
  });

