// ═══════════════════════════════════════════════
// SLAMA Consulting — Main JavaScript
// ═══════════════════════════════════════════════

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    }
});

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.navbar-links');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('open');
        });
        // Close mobile nav when clicking a link
        links.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                links.classList.remove('open');
            });
        });
    }
});

// Scroll reveal animation
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.brutal-card, .service-card, .blog-card, .value-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Active nav link based on current page
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar-links a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
});
