import {scrollBelowNavBar} from "./scrolls.js";

$(function () {
    let now = new Date();
    let element = `#${now.getMonth() + 1}-${now.getFullYear()}-allocations-True`;

    return scrollBelowNavBar(element);
});