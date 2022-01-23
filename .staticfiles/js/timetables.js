function getNavBarYOffSet() {
    const navBar = document.getElementById('navBar');
    return navBar.getBoundingClientRect().bottom + 7;
}

function scrollToElementUnderNavBar(id) {
    let navBarYOffSet = getNavBarYOffSet();

    const element = document.getElementById(id);
    let position = element.getBoundingClientRect().top - navBarYOffSet;

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

function scrollToCurrentDateTimetable() {
    let date = getDateNow();
    let id = `#timetable-${date.month}-${date.year}`;
    scrollToElementUnderNavBar(id)
}

document.addEventListener('DOMContentLoaded', function(){
    scrollToCurrentDateTimetable()
});
