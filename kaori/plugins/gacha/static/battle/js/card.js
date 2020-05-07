import {relativeColor} from "./utils.js";

export function renderCard(card, state = 'idle') {

  const {
    node,
    id,
    name,
    image_url,
    rarity,
    nature,
    hp,
    max_hp,
  } = card;

  const natures = [
    "stupid",
    "baby",
    "clown",
    "horny",
    "cursed",
    "feral",
  ]

  const stats = [
    "hp",
    "evasion",
    "armor",
    "dmg",
    "crit",
    "speed",
  ]

  node.id = 'card_' + id
  node.className = 'card'

  let img = node.querySelector('.cardImage');
  img.src = image_url
  img.alt = `${name} (${rarity}-tier ${nature}`

  node.querySelector('[data-name]').innerText = name
  node.querySelector('[data-rarity]').innerText = rarity
  node.querySelector('[data-nature]').innerText = nature

  let hpText = node.querySelector('[data-hp]');
  if (hpText) {
    hpText.innerText = `HP: ${hp} / ${max_hp}`;
  }



  let hpBar = node.querySelector('[data-hp-bar]');
  if (hpBar) {
    hpBar.style.width = hp / max_hp * 100 + '%'
    hpBar.style.backgroundColor = relativeColor(hp, {min: 1, max: max_hp, linear: true})
  }

  const rows = natures
    .map((nature, i) => ({nature, stat: stats[i]}))
    .map(({nature, stat}) => ({nature, stat, natureValue: card[nature], statValue: card[stat]}))
    .map(row => {

      let {stat, statValue, nature, natureValue} = row;

      let statColor = 'rgb(0, 0, 0)';
      let natureColor = relativeColor(natureValue, {min: NATURE_MIN, max: NATURE_MAX})

      if (stat in maxes) {
        const min = mins[stat];
        const max = maxes[stat];
        statColor = relativeColor(statValue, {min, max})
      }


      if (stat === 'hp') {
        statValue = `${statValue}&nbsp;/&nbsp;${max_hp}`
      }

      return `
      <tr>
        <td>${nature}</td>
        <td style="color: ${natureColor}">${natureValue}</td>
        <td>${stat}</td>
        <td style="color: ${statColor}">${statValue}</td>
      </tr>
      `
    })


  node.querySelector('[data-stats]').innerHTML = rows.join('\n')

  return node;
}

const ARMOR_MAX = 10
const CRIT_MAX = 0.9
const DAMAGE_MAX = 100
const EVA_MAX = 0.9
const HP_MAX = 100
const maxes = {
  hp: HP_MAX,
  evasion: EVA_MAX,
  armor: ARMOR_MAX,
  dmg: DAMAGE_MAX,
  crits: CRIT_MAX,
}
const mins = {
  hp: 1,
  evasion: 0,
  armor: 0,
  dmg: 1,
  crits: 0,
}
const NATURE_MIN = 1;
const NATURE_MAX = 11;