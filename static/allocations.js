import {scrollBelowNavBar} from "./scrolls.js";

$(function () {
    let now = new Date();
    let element = `#day${now.getDate()}Month${now.getMonth() + 1}`;

    return scrollBelowNavBar(element);
});
