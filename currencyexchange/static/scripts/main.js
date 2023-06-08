var currencies = {};

function formatValue (value) {
    return value.toLocaleString(
        "en-US",
        {
            maximumFractionDigits: 2,
            minimumFractionDigits: 2
        }
    ).replace(",", " ");
}

function openCurrenciesList (event) {
    if (event.target.tagName !== "INPUT") {
        let dropdown = document.querySelector("#base-dropdown");
        if (dropdown.style.display == "") {
            dropdown.style.display = "grid";
        } else {
            dropdown.style.display = "";
        }
    }
}

function openDropdown (dropdown_id, type, data) {
    let dropdown = document.querySelector(`#${dropdown_id}-dropdown`);
    let seg_control = dropdown.querySelector(`.sc-${type}`);
    let card = dropdown.querySelector(`.card-${type}`);
    let canvas = document.querySelector(`#${dropdown_id}-canvas`);

    if (card.style.display == "") {
        resetChanges(dropdown);
        dropdown.style.display = "flex";
        seg_control.style.background = "#dfdfdf";
        card.style.display = "flex";
        if (typeof(data) != "undefined") {
            showChart(canvas, data);
        }
    } else {
        resetChanges(dropdown);
        chart = Chart.getChart(canvas)
        if (chart) {
            chart.destroy();
        }
    }
}

function resetChanges (dropdown) {
    let sc_info = dropdown.querySelector(".sc-info");
    let sc_chart = dropdown.querySelector(".sc-chart");
    let card_info = dropdown.querySelector(".card-info");
    let card_chart = dropdown.querySelector(".card-chart");
    sc_info.style.background = "";
    sc_chart.style.background = "";
    card_info.style.display = "";
    card_chart.style.display = "";
    dropdown.style.display = "";
}

function showChart (canvas, data) {
    let ctx = canvas.getContext("2d");
    let r, g, b;
    r = data[2][0];
    g = data[2][1];
    b = data[2][2];
    let chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data[0],
            datasets: [
                {
                    label: "Rate",
                    data: data[1],
                    fill: false,
                    borderColor: `rgb(${r}, ${g}, ${b})`,
                    lineTension: 0
                }
            ]
        },
        options: {
            responsive: true
        }
    });
}

function updateRatesList (base=1) {
    let cards = document.getElementsByClassName("card");
    let currency, rate;
    for (let index = 0; index < cards.length - 1; index++) {
        currency = Object.keys(currencies)[index];
        rate = Object.values(currencies)[index];
        document.getElementById(currency).innerText = formatValue(base * rate);
    }
}
