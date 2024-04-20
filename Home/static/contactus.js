$(document).ready(function() {
  $('i').hide();
})

$(window).load(function() {
  $('i').show();

  var twitterPos = $('#twitter').position();
  var githubPos = $('#github').position();
  var stackPos = $('#stack').position();
  var linkedinPos = $('#linkedin').position();
  var codePos = $('#code').position();
  var plusPos = $('#plus').position();
  var mailPos = $('#mail').position();
  var imgPos = $('.me').position();
  
  $('i').css({
    position: 'absolute',
    zIndex: '1',
    top: imgPos.top + 100,
    left: '20%'
  });
  
  setTimeout(function() {
    $('#twitter').animate({
      top:  300,
      left:  90
    }, 500);
  }, 250);
  
  setTimeout(function() {
    $('#twitter').animate({
      top: 300,
      left: 90
    }, 250);
    
    $('#github').animate({
      top: 300,
      left: 150
    }, 500);
  }, 500);
  
  setTimeout(function() {
    $('#github').animate({
      top: 300,
      left: 150
  }, 250);
    
    $('#stack').animate({
      top: 300,
      left: 210
    }, 500);
  }, 750);
  
  setTimeout(function() {
    $('#stack').animate({
      top: 300,
      left: 210
    }, 250);
    
    $('#linkedin').animate({
      top: 300,
      left: 270
    }, 500);
  }, 1000);
  
  setTimeout(function() {
    $('#linkedin').animate({
      top: 300,
      left: 270
    }, 250);
    
    $('#code').animate({
      top: 300,
      left: 330
    }, 500);
  }, 1250);
  
  setTimeout(function() {
    $('#code').animate({
      top: 300,
      left: 330
    }, 250);
    
    $('#plus').animate({
      top: 300,
      left: 390
    }, 500);
  }, 1500);
  
  setTimeout(function() {
    $('#plus').animate({
      top: 300,
      left: 390
    }, 250);
    
    $('#mail').animate({
      top: 300,
      left: 450
    }, 500);
  }, 1750);
  
  setTimeout(function() {
    $('#mail').animate({
      top: 300,
      left: 450
    }, 250);
  }, 2000);
  
})