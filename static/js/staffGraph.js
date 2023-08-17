const table = document.querySelector(".lecture-table");
let lectures = 0,
    students = 0,
    classes = 0;

for (let i = 1; i < table.rows.length - 1; i++) {
    classes += 1;
    lectures += parseFloat(table.rows[i].cells[1].innerHTML);
    students += parseFloat(table.rows[i].cells[2].innerHTML);
}

classes = classes ? classes : 0;
lectures = lectures ? lectures : 0;
students = students ? students : 0;

Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = "#1a1a1a";

const ctx = document.getElementById("dashGraph");
const dashGraph = new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Classes", "Lectures", "Students"],
        datasets: [
            {
                label: "Bar Graph",
                data: [classes, lectures, students],
                backgroundColor: ["#E9F6FA", "#E9F6FA", "#E9F6FA"],
            },
        ],
    },
    options: {
        scales: {
            yAxes: [
                {
                    ticks: {
                        beginAtZero: true,
                    },
                },
            ],
        },
        title: {
            display: false,
        },
        responsive: false,
        maintainAspectRatio: false,
        animation: {
            animateScale: true,
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
