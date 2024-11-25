let option_a_name = document.getElementById("option-a");
let option_b_name = document.getElementById("option-b");

let weighting_slider = document.getElementById("weighting");
let old_slider_value = weighting_slider.value;
let option_a_weight = 0;
let option_b_weight = 0;

let option_a_weighting_label = document.getElementById("option-a-weighting").getElementsByTagName("span")[0];
let option_b_weighting_label = document.getElementById("option-b-weighting").getElementsByTagName("span")[0];

let privacy_btn = document.getElementById("privacy");
let is_private = false;

let example_coin = document.querySelector(".coin");

function update_weighting_labels(a, b) {
    let label_a = `Option A: ${Math.floor(a * 100)}%`;
    let label_b = `Option B: ${Math.floor(b * 100)}%`;

    option_a_weighting_label.innerText = label_a;
    option_b_weighting_label.innerText = label_b;
}


setInterval(() => {
    let slider_value = weighting_slider.value;
    if (slider_value === old_slider_value) {
        return;
    }

    slider_value = slider_value / 100;

    option_a_weight = slider_value;
    option_b_weight = 1-slider_value;

    update_weighting_labels(option_a_weight, option_b_weight);
}, 25);

privacy_btn.addEventListener("change", () => {
    is_private = !is_private;
});

example_coin.addEventListener("click", () => {
    flip();
})