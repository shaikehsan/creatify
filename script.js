// script.js

window.addEventListener('scroll', function() {
    var aboutSection = document.querySelector('.about-section');
    var scrollPosition = window.innerHeight + window.scrollY;

    if (scrollPosition > aboutSection.offsetTop + 100) {
        aboutSection.classList.add('show');
    }
});
