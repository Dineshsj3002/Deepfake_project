document.addEventListener('DOMContentLoaded', (event) => {
    // Example: Smooth scroll to top on button click
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.textContent = 'Back to Top';
    scrollToTopBtn.className = 'scroll-to-top';
    document.body.appendChild(scrollToTopBtn);

    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Show/Hide Scroll to Top button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 200) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });
});
