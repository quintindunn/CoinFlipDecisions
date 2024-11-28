let outcome = document.getElementById("outcome").value;
let is_first_flip = document.getElementById("is-first-flip").value === "True";
let flip_uuid = document.getElementById("flip-uuid").value;
let is_owner = document.getElementById("is-owner").value;
let base_rating = +document.getElementById("base-rating").value;

let rating_ids = ["bad", "neutral", "happy"];
let rating_btns = [];
let csrfmiddlewaretoken = document.querySelector(`input[name="csrfmiddlewaretoken"]`).value;


function rating(e) {
    if (!+is_owner) {
        e.preventDefault();
        return;
    }
    let value = e.target.value;
    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/flips/ratings/rate/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status !== 200) {
                update_ratings(base_rating)
                console.error("Failed to submit rating:", xhr.status);
            }
        }
    };

    let data = JSON.stringify({ "flip-id": flip_uuid, "value": value });
    xhr.send(data);

    update_ratings(value)
}

function update_ratings(selected_value) {
    for (let i = 0; i < rating_btns.length; i++) {
        let btn = rating_btns[i];
        btn.dataset.selected = +btn.value === +selected_value ? "true" : "false";
    }
}


function flip_it() {
    do_flip(+outcome === 1)
}

if (!is_first_flip) {
    flip_it();
} else {
    let execute_btn = document.getElementById("execute-flip");
    execute_btn.addEventListener("click", () => {
       flip_it();
       execute_btn.hidden = true;
    });
}

for (let i = 0; i < rating_ids.length; i++) {
    let btn = document.getElementById(rating_ids[i]);
    rating_btns.push(btn);
    btn.addEventListener("click", rating);
}