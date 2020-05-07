export async function sleep(msec) {
  return new Promise(function (resolve) {
    window.setTimeout(function () {
      resolve();
    }, msec);
  })
}

export async function animate(el, className, duration = '1s') {
  return new Promise(resolve => {
    let tokens = ['animate__animated', ...[className].flat(Infinity)];
    el.classList.add(...tokens);
    el.style.setProperty('--animate-duration', duration)
    el.addEventListener('animationend', () => {
      el.classList.remove(...tokens)
      resolve(el)
    });
  });
}

function linearScale({x, xMin, xMax, a, b}) {
  return a + (x - xMin) * (b - a) / (xMax - xMin)
}

export function relativeColor(value, {min = 1, max = 100, linear = false}) {

  const ranges = {
    xMin: min,
    xMax: max,
    a: 0,
    b: 255,
  }

  let R = 0
  if (linear) {
    R = linearScale({x: max - value, ...ranges});
  }
  let G = linearScale({x: value, ...ranges});

  return `rgb(${R},${G},0)`;


}

export function sanitizeHtml(str) {
  const decoder = document.createElement('div')
  decoder.innerHTML = str
  return decoder.textContent
}