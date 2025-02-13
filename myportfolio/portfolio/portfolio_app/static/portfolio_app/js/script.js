document.addEventListener('DOMContentLoaded', (event) => {
    // messages
    var messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        message.style.display = 'block';
        setTimeout(function() {
            message.style.opacity = '1';
            message.classList.add('show');
        }, 100);
        
        setTimeout(function() {
            message.style.opacity = '0';
            message.classList.remove('show');
            setTimeout(function() {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });

    // Search functionality
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const blogContainer = document.getElementById('blog-cards-container');
    const paginationContainer = document.getElementById('pagination-container');

    function performSearch(url) {
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = data.html;
            
            const newBlogCards = tempDiv.querySelector('#blog-cards-container');
            const newPagination = tempDiv.querySelector('#pagination-container');
            
            if (newBlogCards) {
                blogContainer.innerHTML = newBlogCards.innerHTML;
            }
            if (newPagination) {
                paginationContainer.innerHTML = newPagination.innerHTML;
            }
            
            window.history.pushState({}, '', url);
            
            // Re-attach event listeners to pagination links
            attachPaginationListeners();

            // Scroll to the top of the blog section
            scrollToBlogSection();
        })
        .catch(error => console.error('Error:', error));
    }

    function attachPaginationListeners() {
        const paginationLinks = document.querySelectorAll('#pagination-container a');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                performSearch(this.href);
            });
        });
    }

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        const url = `${window.location.pathname}?q=${encodeURIComponent(query)}#blog-section`;
        performSearch(url);
    });

    searchInput.addEventListener('input', (e) => {
        if (e.target.value.trim() === '') {
            const url = `${window.location.pathname}#blog-section`;
            performSearch(url);
        }
    });

    // Initial attachment of pagination listeners
    attachPaginationListeners();

    // Scroll to blog section function
    function scrollToBlogSection() {
        const blogSection = document.getElementById('blog-section');
        blogSection.scrollIntoView({
            behavior: 'smooth'
        });
    }


    // active nav link highlight
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-link");

    function activateLinkOnScroll() {
        let scrollY = window.pageYOffset;
        let foundActive = false;

        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 50;
            let sectionId = current.getAttribute("id");

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove("active");
                    if (link.getAttribute("href").includes(sectionId)) {
                        link.classList.add("active");
                        foundActive = true;
                    }
                });
            }
        });

        // Special handling for when scroll is at the top or above the first section
        if (!foundActive) {
            if (scrollY < sections[0].offsetTop - 50) {
                navLinks.forEach(link => link.classList.remove("active"));
                navLinks[0].classList.add("active"); // Assuming the first nav link is "Home"
            } else {
                navLinks.forEach(link => link.classList.remove("active"));
            }
        }
    }

    window.addEventListener("scroll", activateLinkOnScroll);
    activateLinkOnScroll(); // Run on initial load in case user is already at a section

    // Testimonials carousel
    const testimonialsCarousel = document.querySelector('.testimonials-carousel');
    if (testimonialsCarousel) {
        $(testimonialsCarousel).owlCarousel({
            center: true,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            dots: true,
            loop: true,
            margin: 20,
            dotsEach: true,
            responsive: {
                0: {
                    items: 1
                }
            },
            onInitialized: function(event) {
                // Ensure dots are visible after initialization
                const dots = document.querySelectorAll('.owl-dot');
                dots.forEach(dot => {
                    dot.style.display = 'block';
                });
            }
        });
    }

    // Typing effect
    const heroText = document.querySelector('.hero .hero-text h2');
    const typedText = document.querySelector('.hero .hero-text .typed-text');
    
    if (heroText && typedText) {
        const typedStrings = typedText.textContent;
        new Typed('.hero .hero-text h2', {
            strings: typedStrings.split(', '),
            typeSpeed: 100,
            backSpeed: 20,
            smartBackspace: false,
            loop: true
        });
    }
});