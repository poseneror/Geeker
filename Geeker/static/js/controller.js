$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

function recruit(profile) {
    $.ajax({
        url: '/geeker/tryrecruit/',
        method: 'POST',
        data: {
            profile: profile // data you need to pass to your function
        },
        success: function (data) {
            $("#rec_" + profile).addClass("disabled").text("Expert Recruited!!");
        },
        error: function (data) {
            $("#rec_" + profile).removeClass("btn-success").addClass("btn-danger").text("Request Error!");
        }
    });
};

function fire(profile) {
    $.ajax({
        url: '/geeker/fire/',
        method: 'POST',
        data: {
            profile: profile
        },
        success: function (data) {
            $("#fire_" + profile).addClass("disabled").text("Dismissed!");
        },
        error: function (data) {
            $("#fire_" + profile).text("Request Error!");
        }
    });
};

function toggleAvailability(state) {
    $.ajax({
        url: '/geeker/toggleavailability/',
        method: 'POST',
        success: function (data) {
            if(state){
                $(".availability")
                    .removeClass("btn-primary")
                    .addClass("btn-danger")
                    .text("UnAvailable")
                    .attr('onclick', 'toggleAvailability(false)');
            }
            else{
                $(".availability")
                    .removeClass("btn-danger")
                    .addClass("btn-primary")
                    .text("Available")
                    .attr('onclick', 'toggleAvailability(true)');
            }
        }
    });
};

$(document).ready(function(){
    var url = window.location;
    // Will only work if string in href matches with location
    $('ul.nav a[href="'+ url +'"]').parent().addClass('active');

    // Will also work for relative and absolute hrefs
    $('ul.nav a').filter(function() {
        return this.href == url;
    }).parent().addClass('active');
  // Add smooth scrolling to all links in navbar + footer link
  $("#scrollers a, footer a[href='#GeekerPage']").on('click', function(event) {
  // Prevent default anchor click behavior
  event.preventDefault();
  // Store hash
  var hash = this.hash;

  // Using jQuery's animate() method to add smooth page scroll
  // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
  $('html, body').animate({
    scrollTop: $(hash).offset().top
  }, 900, function(){
    // Add hash (#) to URL when done scrolling (default click behavior)
    window.location.hash = hash;
    });
  });
});

$(window).scroll(function() {
  $(".slideanim").each(function(){
    var pos = $(this).offset().top;
    var winTop = $(window).scrollTop();
    if (pos < winTop + 600) {
      $(this).addClass("slide");
    }
  });
});