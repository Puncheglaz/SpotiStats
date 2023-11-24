import Chart from "chart.js/auto";
const { server_vars } = require("./variables.js");

let myChart; // Variable to store the Chart instance

async function fetchData(genre) {
    const response = await fetch(
        `http://${server_vars.address}:${server_vars.port}/getTracksPerYearForGenre?genre=${genre}`
    );
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
}

function updateChart(selectedGenre) {
    fetchData(selectedGenre)
        .then((data) => {
            // Destroy the existing chart if it exists
            if (myChart) {
                myChart.destroy();
            }

            // Create a new chart with the new data
            myChart = new Chart(document.getElementById("chart"), {
                type: "bar",
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
                    labels: data.map((row) => row.year),
                    datasets: [
                        {
                            label: "Tracks released",
                            data: data.map((row) => row.count),
                        },
                    ],
                },
            });
        })
        .catch((error) => {
            console.error("Error fetching data:", error.message);
        });
}

document.getElementById("genreSelect").addEventListener("change", function () {
    const selectedGenre = this.value;
    updateChart(selectedGenre);
});

// Initial chart update
const initialGenre = document.getElementById("genreSelect").value;
updateChart(initialGenre);
