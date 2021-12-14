export function getNavBarYOffSet () {
    const navBar = $('#navBar')
    return navBar.outerHeight(true);
}

function scrollToTimetableDateNow() {
    let date = new Date();
    let element = `#${date.getMonth() + 1}-${date.getFullYear()}-allocations-True`
    let position = $(element).offset().top - getNavBarYOffSet();

    window.scrollTo({
        top: position,
        behavior:'smooth'
    })
}

$(document).ready(function() {
    scrollToTimetableDateNow();
})