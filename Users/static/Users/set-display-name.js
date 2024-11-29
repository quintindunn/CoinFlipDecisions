let new_display_name = document.getElementById("display-name");
let submit_btn = document.getElementById("submit");
let name_error = document.getElementById("bad-name");
let error_p = name_error.querySelector("p");

let csrfmiddlewaretoken = document.querySelector(`input[name="csrfmiddlewaretoken"]`).value;

let okay = false;

function submit(name) {
    if (!okay) {
        console.log("Bad");
        return;
    }
    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/account/setdisplayname/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status !== 200) {
                console.error("Failed to update display name:", xhr.status);
                return;
            }
            window.location = "/";
        }
    };

    let data = JSON.stringify({
        "displayname": name
    });
    xhr.send(data);
}

function verify_display_name(name) {

    if (name.length < 5) {
        error_p.innerText = "Sorry, your name must be at least 5 characters!"
        name_error.dataset.hidden = "false";
        return;
    }

    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/account/checkdisplayname/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status !== 200) {
                console.error("Failed to check display name:", xhr.status);
                return;
            }
            okay = xhr.responseText === "true";

            if (!okay) {
                name_error.dataset.hidden = "false";
                error_p.innerText = "Sorry, this name is already taken!"
            }
            submit(name);
        }
    };

    let data = JSON.stringify({"displayname": name});
    xhr.send(data);
}


submit_btn.addEventListener("click", (e) => {
    name_error.dataset.hidden = "true";
    verify_display_name(new_display_name.value);
});

