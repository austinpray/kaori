import {relativeColor} from "../js/utils.js";

const rctLinear = document.getElementById('rct_linear');
const rctBoost = document.getElementById('rct_boost');
for (let i = 1; i <= 100; i++) {
  const linear = document.createElement('div')
  linear.style.cssText = `
  width: 1em;
  height: 1em;
  `;
  const boost = linear.cloneNode(true)
  linear.style.backgroundColor = relativeColor(i, {min: 1, max: 100, linear: true})
  rctLinear.append(linear)
  boost.style.backgroundColor = relativeColor(i, {min: 1, max: 100})
  rctBoost.append(boost)
}

