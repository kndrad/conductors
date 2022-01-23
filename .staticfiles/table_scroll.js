function getNavBarYOffSet() {
    const navBar = $('#navBar')
    return navBar.outerHeight(true);
}

function scrollToElementUnderNavBar(element) {
    let position = $(element).offset().top - getNavBarYOffSet();
    window.scrollTo({
        top: position,
        behavior:'smooth'
    })
}

function getDateNow() {
    let date = new Date();
    return {
        day:date.getDay(),
        month:date.getMonth() +1,
        year:date.getFullYear(),
    }
}

function scrollToTimetableDateNow() {
    let date = getDateNow();
    let element = `#${date.month}-${date.year}-allocations-True`
    scrollToElementUnderNavBar(element);
}


$(document).ready(function () {
    scrollToTimetableDateNow()
});
