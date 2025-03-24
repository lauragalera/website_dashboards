
  document.querySelectorAll('.orbit').forEach((el, index) => {
    // Randomize initial positions
    el.style.left = `${Math.random() * 80 + 10}%`;
    el.style.top = `${Math.random() * 80 + 10}%`;
    
    // Randomize animation
    const duration = 15 + Math.random() * 15;
    el.style.animation = `float ${duration}s infinite ease-in-out`;
  });