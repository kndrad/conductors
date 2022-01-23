export function smoothScrollUnderHeader(element) {
    window.scrollTo({
        top: $(element).offset().top - $('#main-header').outerHeight(true),
        behavior: 'smooth'
    });
}

