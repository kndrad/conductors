function scrollToDayNow() {
    let date = getDateNow();
    let element = `#rowDay${date.day}`;
    scrollToElementUnderNavBar(element);
}

$(document).ready(function () {
    scrollToDayNow()
});
