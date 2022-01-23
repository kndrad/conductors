import {smoothScrollUnderHeader} from "./scrolls.js";

$(function () {
    let now = new Date();
    let element = `#${now.getMonth() + 1}-${now.getFullYear()}-not-empty-True`;

    return smoothScrollUnderHeader(element);
});