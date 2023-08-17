const searchForm = document.getElementById("search_form");
const searchInput = document.getElementById("search_input");
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const usersResult = document.getElementById("user_results");
const staffResult = document.getElementById("staff_results");
const classesResult = document.getElementById("class_results");

const sendSearchData = (query) => {
    let url = `${window.location.origin}/api/search/${query}/`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            usersResult.innerHTML = "";
            staffResult.innerHTML = "";
            classesResult.innerHTML = "";

            data.users.forEach((user) => {
                usersResult.innerHTML += `
                    <a style="text-decoration: none; display: block;" href="${window.location.origin}/users/${user.prn}/">
                        <div class="search-result">
                            <p>${user.name}</p>
                        </div>
                    </a>
                `;
            });

            data.staff.forEach((staff) => {
                staffResult.innerHTML += `
                    <a style="text-decoration: none; display: block;" href="${window.location.origin}/users/${staff.empno}/">
                        <div class="search-result">
                            <p>${staff.name}</p>
                        </div>
                    </a>
                `;
            });

            data.classes.forEach((classroom) => {
                classesResult.innerHTML += `
                    <a style="text-decoration: none; display: block;" href="${window.location.origin}/classes/${classroom.id}/">
                        <div class="search-result">
                            <p>${classroom.name}</p>
                        </div>
                    </a>
                `;
            });
        });
};

const clearSearch = () => {
    usersResult.innerHTML = "";
    staffResult.innerHTML = "";
    classesResult.innerHTML = "";
};

searchInput.addEventListener("keyup", (e) => {
    if (e.target.value !== "") {
        sendSearchData(e.target.value);
    } else {
        clearSearch();
    }
});
