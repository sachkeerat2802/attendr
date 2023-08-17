let date_obj = document.getElementById("date_obj");
let timetableSection = document.querySelector(".timetable-items");

const today = new Date();
const dd = String(today.getDate()).padStart(2, "0");
const mm = String(today.getMonth() + 1).padStart(2, "0");
const yyyy = today.getFullYear();

date_obj.value = yyyy + "-" + mm + "-" + dd;

date_obj.onchange = function () {
    let value = date_obj.value;
    let url = `${window.location.origin}/api/timetable/${value}`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            timetableSection.innerHTML = "";
            data.forEach((ele) => {
                let timetable_data = `<div class="timetable-item flex">
                <p class="timetable-item__time fw-medium h6 clr-black-50">${ele.time}</p>
                <div class="timetable-item__divider"></div>
                <div>
                <div class="flex">
                <p class="timetable-item__roomfaculty fw-light clr-black-50">${ele.room} : ${ele.faculty}</p>
                </div>
                <p class="timetable-item__name fw-medium">${ele.name}</p>
                </div>
                </div>
                <br>`;
                timetableSection.innerHTML += timetable_data;
            });
        });
};

let ev = new Event("change");
date_obj.dispatchEvent(ev);
