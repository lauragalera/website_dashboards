class HelpPopup {
    constructor() {
      this.popup = null;
      this.initialized = false;
    }
  
    init() {
      if (this.initialized) return;
      
      // Create popup container
      const popupDiv = document.createElement('div');
      popupDiv.id = 'help-popup-container';
      document.body.appendChild(popupDiv);
      
      // Load popup content (in a real app, you might fetch this)
      popupDiv.innerHTML = document.getElementById('help-popup-template').innerHTML;
      
      this.popup = document.getElementById('helpPopup');
      this.initialized = true;
      
      // Set up event listeners
      document.querySelector('.close-popup').addEventListener('click', () => this.close());
      this.popup.addEventListener('click', (e) => {
        if (e.target === this.popup) this.close();
      });
      
      // Add logic for buttons
      document.getElementById('contactSupport').addEventListener('click', () => {
        // Handle contact support logic
        console.log('Contact support clicked');
      });
      
      document.getElementById('viewTutorial').addEventListener('click', () => {
        // Handle tutorial logic
        console.log('View tutorial clicked');
      });
    }
  
    open(content) {
      if (!this.initialized) this.init();
      if (content) {
        document.querySelector('.help-content').innerHTML = content;
      }
      this.popup.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  
    close() {
      this.popup.style.display = 'none';
      document.body.style.overflow = 'auto';
    }
  }
  
  // Export as singleton
  const helpPopup = new HelpPopup();
  export default helpPopup;