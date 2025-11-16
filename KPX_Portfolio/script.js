// Wait for the HTML document to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    // --- MODAL LOGIC ---
    // Get the modal elements from the DOM
    const modal = document.getElementById('email-modal');
    const showBtn = document.getElementById('show-email-btn');
    const closeBtn = document.querySelector('.close-btn');

    // Function to open the modal
    showBtn.onclick = function() {
        modal.style.display = 'block';
    };

    // Function to close the modal when the 'x' is clicked
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };

    // Function to close the modal when clicking outside of the modal content
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };


    // --- FADE-IN ANIMATION LOGIC ---
    // Select all elements with the 'fade-in' class
    const faders = document.querySelectorAll('.fade-in');

    // Options for the Intersection Observer
    const appearOptions = {
        threshold: 0.3, // Trigger when 30% of the element is visible
        rootMargin: "0px 0px -50px 0px" // Start observing a bit earlier
    };

    // Create a new IntersectionObserver
    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            // If the element is not intersecting, do nothing
            if (!entry.isIntersecting) {
                return;
            }
            // If it is intersecting, add the 'is-visible' class to trigger the CSS animation
            entry.target.classList.add('is-visible');
        });
    }, appearOptions);

    // Tell the observer to watch each of our fader elements
    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });


    // --- SMOOTH SCROLLING LOGIC ---
    // Get all navigation links
    const navLinks = document.querySelectorAll('.nav-link');

    // Add a click event listener to each link
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Prevent the default instant jump
            e.preventDefault();

            // Get the target section's ID from the href attribute
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            // If the target section exists, scroll to it smoothly
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

}); // This is the final closing brace for the event listener