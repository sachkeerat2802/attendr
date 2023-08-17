const table = document.querySelector(".lecture-table");
let present = 0,
    absent = 0;

for (let i = 1; i < table.rows.length - 1; i++) {
    present += parseFloat(table.rows[i].cells[2].innerHTML);
    absent += parseFloat(table.rows[i].cells[3].innerHTML);
}

let total = present + absent;
let presentPercentage = Math.round((present / total) * 100);
let absentPercentage = Math.round((absent / total) * 100);
presentPercentage = presentPercentage ? presentPercentage : 0;
absentPercentage = absentPercentage ? absentPercentage : 0;

Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = "#1a1a1a";

const ctx = document.getElementById("dashGraph");
const dashGraph = new Chart(ctx, {
    type: "pie",
    data: {
        labels: ["Present " + presentPercentage + "%", "Absent " + absentPercentage + "%"],
        datasets: [
            {
                data: [presentPercentage, absentPercentage],
                backgroundColor: ["#A5C1DC", "#E9F6FA"],
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            animateScale: true,
        },
        title: {
            display: false,
        },
        plugins: {
            legend: {
                display: true,
                position: "bottom",
            },
            title: {
                display: false,
            },
            datalabels: {
                display: true,
                color: "#fff",
                font: {
                    weight: "bold",
                    size: 16,
                },
                textAlign: "center",
            },
        },
    },
});
