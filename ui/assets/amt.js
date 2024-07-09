let shapChart;

/**
 * Good enough function to toggle tabs
 * @param myId
 * @param tabEl
 */
function toggle(myId, tabEl) {

    let tabs = document.getElementsByClassName("tabs__list")[0].getElementsByTagName("li");
    for (let i =0; i < tabs.length; i++) {
        let aEls = tabs[i].getElementsByTagName("a");
        aEls[0].classList.remove("is-selected");
        if (tabs[i] === tabEl) {
            aEls[0].classList.add("is-selected");
        }
    }

    let els = document.getElementsByClassName("amt_tabs");
    for (let i = 0; i  < els.length; i++) {
        els[i].classList.remove("amt_visible");
        els[i].classList.add("amt_hidden");
    }
    document.getElementById(myId).classList.remove("amt_hidden")
    document.getElementById(myId).classList.add("amt_visible")
}

function toggleOrganisation(id, clickEl) {
    let myEl = document.getElementById(id);
    if (myEl.style.display === "block") {
        myEl.style.display = "none";
        clickEl.style.transform = "rotate(180deg)";
    }  else {
        myEl.style.display = "block";
        clickEl.style.transform = "rotate(270deg)";
    }
}

function renderShapGraph(data, labels) {
    const ctx = document.getElementById('shapChart');

    if (shapChart) {
        shapChart.destroy();
    }

    shapChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,

            datasets: [{
                backgroundColor: ["rgba(0, 123, 199, 0.8)"],
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            plugins:
                {
                    legend: {
                        display: false
                    }
                },
        }
    });
}

function compareShapValue( a, b ) {
    if ( a.value < b.value ){
        return 1;
    }
    if ( a.value > b.value ){
        return -1;
    }
    return 0;
}
