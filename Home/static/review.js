// Function to set the minimum height of elements in a NodeList to the tallest element's height
function setHeights(items) {
    let currentTallest = 0;
  
    items.forEach(function (item) {
      item.style.minHeight = '0'; // Unset min-height to get the actual new height
  
      if (item.offsetHeight > currentTallest) {
        currentTallest = item.offsetHeight;
      }
    });
  
    items.forEach(function (item) {
      item.style.minHeight = currentTallest + 'px';
    });
  }
  
  // Wait for the window to load before applying the function
  window.addEventListener('load', function () {
    const testimonials = document.querySelectorAll('.grid-testimonials p');
    setHeights(testimonials);
  
    // Add a resize event listener to recalculate heights on window resize
    window.addEventListener('resize', function () {
      setHeights(testimonials);
    });
  });
  