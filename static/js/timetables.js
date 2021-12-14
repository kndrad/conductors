function scrollToElementUnderNavBar(id) {
    let navBar = document.getElementById('navBar');
    let navBarYOffSet = navBar.getBoundingClientRect().bottom;

    let element = document.getElementById(id);
    let yOffset = element.getBoundingClientRect().top - 10;

    options = {
        top: yOffset - navBarYOffSet,
        behavior:'smooth'
    }
    window.scrollTo(options)
}

function scrollToCurrentDateTimetable() {
    let now = new Date();
    let month = now.getMonth() + 1;
    let year = now.getFullYear();

    let id = `timetable-${month}-${year}`;
    scrollToElementUnderNavBar(id)
}

document.addEventListener('DOMContentLoaded', function(){
    scrollToCurrentDateTimetable()
});
