const date = new Date();

function getRowTodayElement() {
    return $(`#day${date.getDate()}`);
}

const rowToday = getRowTodayElement();

function scrollToDayNow() {
    let navBar = $('#navBar')

    window.scrollTo({
        top: rowToday.offset().top - navBar.outerHeight(true),
        behavior:'smooth'
    });
}

$(function() {
    rowToday.addClass('');
});

$(document).ready(function() {
    scrollToDayNow();
})