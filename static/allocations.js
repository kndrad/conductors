import {smoothScrollUnderHeader} from "./scrolls.js";

$(function () {
    let now = new Date();
    let element = `#day${now.getDate()}-month${now.getMonth() + 1}`;

    return smoothScrollUnderHeader(element);
});
