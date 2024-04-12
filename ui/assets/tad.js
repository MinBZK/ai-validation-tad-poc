/**
 * Good enough function to toggle tabs
 * @param myId
 * @param tabEl
 */
function toggle(myId, tabEl) {

    let tabs = document.getElementsByClassName("tabs__list")[0].getElementsByTagName("li");
    for (i =0; i < tabs.length; i++) {
        let aEls = tabs[i].getElementsByTagName("a");
        aEls[0].classList.remove("is-selected");
        if (tabs[i] === tabEl) {
            aEls[0].classList.add("is-selected");
        }
    }

    let els = document.getElementsByClassName("tad_tabs");
    for (i = 0; i  < els.length; i++) {
        els[i].classList.remove("tad_visible");
        els[i].classList.add("tad_hidden");
    }
    document.getElementById(myId).classList.remove("tad_hidden")
    document.getElementById(myId).classList.add("tad_visible")
}
