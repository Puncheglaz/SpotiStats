import Chart from "chart.js/auto";
const { server_vars } = require("./variables.js");

let myChart; // Variable to store the Chart instance

function shortenNumber(number) {
    const billion = 1e9; // 1 billion
    const million = 1e6; // 1 million
    const thousand = 1e3; // 1 thousand

    if (Math.abs(number) >= billion) {
        return (number / billion).toFixed(1) + "B";
    } else if (Math.abs(number) >= million) {
        return (number / million).toFixed(1) + "M";
    } else if (Math.abs(number) >= thousand) {
        return (number / thousand).toFixed(1) + "K";
    } else {
        return number.toString();
    }
}

const AVAILABLE_CHARTS = [
    {
        type: "bar",
        id: "bar_1",
        name: "Number of tracks released each year for a selected genre",
        requestMethod: "tracksByYears&genre=",
        label: "Tracks released",
    },
    {
        type: "bar",
        id: "bar_2",
        name: "Number of plays of the selected genre each year",
        requestMethod: "playsByYears&genre=",
        label: "Plays",
    },
    {
        type: "bar",
        id: "bar_3",
        name: "Averaged music features of the selected genre",
        requestMethod: "features&genre=",
        label: "Value",
    },

    {
        type: "pie",
        id: "pie_1",
        name: "Top genres by number of plays",
        requestMethod: "genresByPlays",
        label: "Plays",
    },
    {
        type: "pie",
        id: "pie_2",
        name: "Top of the years by the total number of plays of all tracks released during them",
        requestMethod: "yearsByReleases",
        label: "Plays",
    },
    {
        type: "pie",
        id: "pie_3",
        name: "Top 5 genres with the most number of explicit tracks",
        requestMethod: "explicitByGenre",
        label: "Tracks",
    },

    {
        type: "map",
        id: "map_1",
        name: "Heat map of genre popularity by country",
        requestMethod: "genreByCountries&genre=",
        label: "Monthly plays",
    },
    {
        type: "map",
        id: "map_2",
        name: "Map of countries with their top genres and artists",
        requestMethod: "topGenreAndArtistByCountries",
        label: "Artist and genre",
    },
];

function clearChart() {
    if (myChart) {
        myChart.destroy();
    }
}

function removeOptionInput() {
    document.getElementById("option-select-container").innerHTML = "";
}

function createBarChart(chart, data) {
    return new Chart(document.getElementById("chart"), {
        type: chart.type,
        options: {
            animation: true,
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    enabled: true,
                },
            },
        },
        data: {
            labels: data.map((row) => row[0]),
            datasets: [
                {
                    label: chart.label,
                    data: data.map((row) => row[1]),
                },
            ],
        },
    });
}

function createPieChart(myChart, data) {
    // Convert string values to numbers
    const numericData = data.map(([label, value]) => [
        label,
        parseFloat(value),
    ]);

    // Calculate the total sum of numbers
    const sumTotal = numericData.reduce((sum, item) => sum + item[1], 0);

    // Calculate the percentage for each number
    const percentages = numericData.map((item) => {
        const number = parseInt(item[1], 10);
        const percent = (number / sumTotal) * 100;
        return percent;
    });

    console.log("Total Sum:", sumTotal);
    console.log("Percentages:", percentages);

    // // Sum the values of the categories below the threshold
    // const otherSum = numericData.reduce(
    //     (sum, [, value]) =>
    //         (value / totalSum) * 100 < thresholdPercentage ? sum + value : sum,
    //     0
    // );

    // // Add the "other" category to the filtered data
    // if (otherSum > 0) {
    //     filteredData.push(["Other", otherSum]);
    // }

    const N = 7; // Set the number of top labels to display in the legend

    const sortedData = data.sort((a, b) => b[1] - a[1]);

    // Extract the top N labels
    const topLabels = sortedData.slice(0, N).map((row) => row[0]);
    console.log(topLabels);

    var options = {
        type: myChart.type,
        options: {
            animation: true,
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true,
                        filter: (legendItem) => {
                            return legendItem.index < N;
                        },
                        font: {
                            size: 20,
                        },
                    },
                },
                tooltip: {
                    enabled: true,
                },
            },
        },
        data: {
            labels: data.map((row) => row[0]),
            datasets: [
                {
                    label: myChart.label,
                    data: data.map((row) => row[1]),
                },
            ],
        },
    };

    return new Chart(document.getElementById("chart"), options);
}

function updateChart(chart, options = "") {
    clearChart();
    fetchData(chart.requestMethod + options)
        .then((data) => {
            clearChart();
            switch (chart.type) {
                case "bar":
                    myChart = createBarChart(chart, data);
                    break;
                case "pie":
                    myChart = createPieChart(chart, data);
                    break;
                default:
                    break;
            }
            myChart = createBarChart(chart, data);
        })
        .catch((error) => {
            console.error("Error fetching data:", error.message);
        });
}

async function getGenres() {
    const requestMethod = "genres";
    try {
        const data = await fetchData(requestMethod);
        return data;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

async function fetchData(requestMethod) {
    const response = await fetch(
        `http://${server_vars.address}:${server_vars.port}/query?type=${requestMethod}`
    );
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
}

function createChartSelects() {
    var selectedChartTypeOption =
        document.getElementById("chart-type-select").value;

    var availableCharts = [];
    switch (selectedChartTypeOption) {
        case "bar":
            availableCharts = AVAILABLE_CHARTS.filter(
                (chart) => chart.type === "bar"
            );
            break;
        case "pie":
            availableCharts = AVAILABLE_CHARTS.filter(
                (chart) => chart.type === "pie"
            );
            break;
        case "map":
            availableCharts = AVAILABLE_CHARTS.filter(
                (chart) => chart.type === "map"
            );
            break;
        default:
            break;
    }

    // Create the <select> tags based on the chosen graph type
    const chartSelectId = "graph-select";
    var chartSelect = `<select id=${chartSelectId}>`;
    chartSelect += "<option value='' disabled selected>Select chart:</option>";
    availableCharts.forEach((chart) => {
        chartSelect +=
            "<option value='" + chart.id + "'>" + chart.name + "</option>";
    });
    chartSelect += "</select>";

    document.getElementById("chart-select-container").innerHTML = chartSelect;
    document
        .getElementById(chartSelectId)
        .addEventListener("change", function () {
            const chartId = this.value;
            const chart = AVAILABLE_CHARTS.find(
                (chart) => chart.id === chartId
            );
            const requestMethod = chart.requestMethod;
            if (requestMethod[requestMethod.length - 1] === "=") {
                clearChart();
                removeOptionInput();
                createOptionInput(chart);
            } else {
                updateChart(chart);
            }
        });
}

async function createMapOptionInput() {
    const genres = await getGenres(); // Wait for getGenres to complete
    console.log(genres);

    const optionDropdownDivId = "map-option-dropdown";
    const optionDropdownDivClass = "dropdown";
    var optionDropdownDiv = `<div id=${optionDropdownDivId} class=${optionDropdownDivClass}></div>`;
    document.getElementById("map-option-select-container").innerHTML =
        optionDropdownDiv;

    const optionInputId = "map-dropdown-input";
    const optionInputType = "text";
    const optionInputPlaceholder = "Input genre";
    var optionInput =
        `<input type="${optionInputType}" id="${optionInputId}" placeholder='` +
        optionInputPlaceholder +
        "'>";
    document.getElementById(optionDropdownDivId).innerHTML = optionInput;

    const optionUlId = "map-dropdown-list";
    var optionUl = `<ul id=${optionUlId}></ul>`;
    document.getElementById(optionDropdownDivId).innerHTML += optionUl;

    const inputElement = document.getElementById(optionInputId);
    const listElement = document.getElementById(optionUlId);

    const chart = AVAILABLE_CHARTS.find((chart) => chart.id === "map_1");

    inputElement.addEventListener("input", function () {
        const inputValue = inputElement.value.toLowerCase();
        const filteredOptions = genres.filter((option) =>
            option.toLowerCase().includes(inputValue)
        );

        // Clear the previous list
        listElement.innerHTML = "";

        // Create a new list based on filtered options
        filteredOptions.forEach((option) => {
            const li = document.createElement("li");
            li.textContent = option;
            li.addEventListener("click", function () {
                inputElement.value = option;
                listElement.innerHTML = ""; // Hide the dropdown after selection
                updateMap(chart, option);
            });
            listElement.appendChild(li);
        });
    });
}

async function createOptionInput(chart) {
    const genres = await getGenres(); // Wait for getGenres to complete
    console.log(genres);

    // Create the <select> tags based on the chosen graph type
    const optionDropdownDivId = "option-dropdown";
    const optionDropdownDivClass = "dropdown";
    var optionDropdownDiv = `<div id=${optionDropdownDivId} class=${optionDropdownDivClass}></div>`;
    document.getElementById("option-select-container").innerHTML =
        optionDropdownDiv;

    const optionInputId = "dropdown-input";
    const optionInputType = "text";
    const optionInputPlaceholder = "Input genre";
    var optionInput = `<input type="${optionInputType}" id="${optionInputId}" placeholder="${optionInputPlaceholder}">`;
    document.getElementById(optionDropdownDivId).innerHTML = optionInput;

    const optionUlId = "dropdown-list";
    var optionUl = `<ul id=${optionUlId}></ul>`;
    document.getElementById(optionDropdownDivId).innerHTML += optionUl;

    const inputElement = document.getElementById(optionInputId);
    const listElement = document.getElementById(optionUlId);

    inputElement.addEventListener("input", function () {
        const inputValue = inputElement.value.toLowerCase();
        const filteredOptions = genres.filter((option) =>
            option.toLowerCase().includes(inputValue)
        );

        // Clear the previous list
        listElement.innerHTML = "";

        // Create a new list based on filtered options
        filteredOptions.forEach((option) => {
            const li = document.createElement("li");
            li.textContent = option;
            li.addEventListener("click", function () {
                inputElement.value = option;
                listElement.innerHTML = ""; // Hide the dropdown after selection
                updateChart(chart, option);
            });
            listElement.appendChild(li);
        });
    });
}

document
    .getElementById("chart-type-select")
    .addEventListener("change", function () {
        clearChart();
        removeOptionInput();
        createChartSelects();
    });

anychart.onDocumentReady(function () {
    createMapOptionInput();
    const chart = AVAILABLE_CHARTS.find((chart) => chart.id === "map_1");
    const options = "rap";
    updateMap(chart, options);
});

function updateMap(chart, options) {
    document.getElementById("map-container").innerHTML = "";
    fetchData(chart.requestMethod + options).then((data) => {
        var map = anychart.map();

        map.title()
            .enabled(true)
            .useHtml(true)
            .padding([10, 0, 10, 0])
            .text(`Popularity of ${options} across countries`);

        map.geoData("anychart.maps.world");
        map.interactivity().selectionMode("none");
        map.padding(0);

        var formattedData = data.map(function (item) {
            return {
                id: item[0], // Assuming the first element is the ID
                plays: item[1], // Assuming the second element is the density (converted to an integer)
            };
        });

        // Create AnyChart data set
        var dataSet = anychart.data.set(formattedData);
        var playsData = dataSet.mapAs({ value: "plays" });
        var playsArray = formattedData.map(function (item) {
            return parseInt(item.plays);
        });

        // Create choropleth map using the density data
        var series = map.choropleth(playsData);

        series.labels(false); // Turn off countries names on the map

        // When hovered
        series
            .hovered()
            .fill("#f48fb1")
            .stroke(anychart.color.darken("#f48fb1"));

        // When selected
        series
            .selected()
            .fill("#c2185b")
            .stroke(anychart.color.darken("#c2185b"));

        // Tooltip
        series
            .tooltip()
            .useHtml(true)
            .format(function () {
                return (
                    '<span style="color: #d9d9d9">Plays</span>: ' +
                    parseInt(this.value).toLocaleString()
                );
            });

        var minPlays = Math.min(...playsArray);
        var maxPlays = Math.max(...playsArray);
        var step = (maxPlays - minPlays) / 9;
        var scale = anychart.scales.ordinalColor([
            { less: step },
            { from: step, to: step * 2 },
            { from: step * 2, to: step * 3 },
            { from: step * 3, to: step * 4 },
            { from: step * 4, to: step * 5 },
            { from: step * 5, to: step * 6 },
            { from: step * 6, to: step * 7 },
            { from: step * 7, to: step * 8 },
            { greater: step * 8 },
        ]);
        scale.colors([
            "#81d4fa",
            "#4fc3f7",
            "#29b6f6",
            "#039be5",
            "#0288d1",
            "#0277bd",
            "#01579b",
            "#014377",
            "#013377",
        ]);

        var colorRange = map.colorRange();
        colorRange.enabled(true).padding([0, 0, 20, 0]);
        colorRange
            .ticks()
            .enabled(true)
            .stroke("3 #ffffff")
            .position("center")
            .length(7);
        colorRange.colorLineSize(5);
        colorRange.marker().size(7);
        colorRange
            .labels()
            .fontSize(11)
            .padding(3, 0, 0, 0)
            .format(function () {
                var range = this.colorRange;
                var name;
                if (isFinite(range.start + range.end)) {
                    name =
                        shortenNumber(parseInt(range.start)) +
                        " - " +
                        shortenNumber(parseInt(range.end));
                } else if (isFinite(range.start)) {
                    name = "More than " + shortenNumber(parseInt(range.start));
                } else {
                    name = "Less than " + shortenNumber(parseInt(range.end));
                }
                return name;
            });

        series.colorScale(scale);

        var zoomController = anychart.ui.zoom();
        zoomController.render(map);

        map.container("map-container");

        map.draw();
    });
}
