export function scrollBelowNavBar(element) {
    window.scrollTo({
        top: $(element).offset().top - $('#navBar').outerHeight(true),
        behavior: 'smooth'
    });
}

