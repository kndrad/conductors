const date = new Date();

function getRowTodayElement() {
    return $(`#day${date.getDate()}`);
}

const rowToday = getRowTodayElement();

$(function () {
    let navBar = $('#navBar')

    window.scrollTo({
        top: rowToday.offset().top - navBar.outerHeight(true),
        behavior:'smooth'
    });
});

$(function() {
    rowToday.addClass('text-red-500');
});