$(function () {
    let date = new Date();
    let row = $(`#day${date.getDate()}Month${date.getMonth() + 1}`);
    let navBar = $('#navBar');

    window.scrollTo({
        top: row.offset().top - navBar.outerHeight(true),
        behavior: 'smooth'
    });
    row.addClass('shadow-inner shadow-white')
});
