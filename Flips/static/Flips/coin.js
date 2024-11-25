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

function set_option(opt_a = false) {
  if(opt_a && flipped) {
    flip();
  } else if (!opt_a && !flipped) {
    flip();
  }
}

function do_flip(result_a) {
  let i = 0;
  let dynamic_flipping_time = MIN_FLIPPING_TIME + Math.random() * FLIPPING_TIME_MAX_OFFSET;

  let results = document.getElementById("results");
  let interval = setInterval(() => {
    if (i >= dynamic_flipping_time / TIME_PER_FLIP) {
      clearInterval(interval);
      setTimeout(() => {
        results.dataset.hidden = "false";
      }, TIME_PER_FLIP*1000)

    }
    flip();
    i++;
  }, TIME_PER_FLIP*1000);
  set_option(result_a);


  return result_a;
}
