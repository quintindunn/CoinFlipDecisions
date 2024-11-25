const MIN_FLIPPING_TIME = 2.0; // seconds
const FLIPPING_TIME_MAX_OFFSET = 2.0; // seconds
const TIME_PER_FLIP = .25; // seconds
const coin = document.querySelector('.coin');
coin.style.transition = `transform ${TIME_PER_FLIP}s`;

let flipped = false;


function flip() {
  flipped = !flipped;
  coin.dataset.flipped = flipped ? "true" : "false";
}

function set_option(opt_a = false) {
  if(a && flipped) {
    flip();
  } else if (!a && !flipped) {
    flip();
  }
}

function do_flip(weight_a) {
  let opt_a =  Math.random() <= weight_a;

  let i = 0;
  let dynamic_flipping_time = MIN_FLIPPING_TIME + Math.random() * FLIPPING_TIME_MAX_OFFSET;

  let interval = setInterval(() => {
    if (i >= dynamic_flipping_time / TIME_PER_FLIP) {
      clearInterval(interval);
    }
    flip();
    i++;
  }, TIME_PER_FLIP*1000);
  set_option(opt_a);
  return opt_a;
}

// Dev Code
coin.addEventListener( 'click', () => {
  do_flip(0.35);
});