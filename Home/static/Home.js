window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.nav'); // Replace with the class or ID of your navbar
    var scrollPosition = window.scrollY;
  
    if (scrollPosition > 450) { // Change the value to the desired scroll position
      navbar.classList.add('visible');
    } else {
      navbar.classList.remove('visible');
    }
  });
  