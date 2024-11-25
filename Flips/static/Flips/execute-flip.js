let outcome = document.getElementById("outcome").value;
let is_first_flip = document.getElementById("is-first-flip").value === "True";


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