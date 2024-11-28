const MIN_FLIPPING_TIME = 1.0; // seconds
const FLIPPING_TIME_MAX_OFFSET = 0; // seconds
const TIME_PER_FLIP = .25; // seconds
const coin = document.querySelector('.coin');
coin.style.transition = `transform ${TIME_PER_FLIP}s`;

let flipped = false;


function flip() {
  flipped = !flipped;
  coin.dataset.flipped = flipped ? "true" : "false";
}

function set_option(is_a) {
  if (is_a) {
    flipped = false;
    coin.dataset.flipped = "false";
    return
  }
  flipped = true;
  coin.dataset.flipped = "true";
}

function do_flip(result_a) {
  let i = 0;
  let dynamic_flipping_time = MIN_FLIPPING_TIME + Math.random() * FLIPPING_TIME_MAX_OFFSET;

  let results = document.getElementById("results");
  let interval = setInterval(() => {
    if (i >= dynamic_flipping_time / TIME_PER_FLIP) {
      clearInterval(interval);
      set_option(result_a);
      setTimeout(() => {
        results.dataset.hidden = "false";
      }, TIME_PER_FLIP*1000)

    }
    if (!(i >= dynamic_flipping_time / TIME_PER_FLIP))
      flip();
    i++;
  }, TIME_PER_FLIP*1000);
  set_option(result_a)
  return result_a;
}
