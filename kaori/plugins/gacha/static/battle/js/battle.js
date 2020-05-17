import {animate, sleep, sanitizeHtml} from "./utils.js";
import {renderCard} from "./card.js";
import {relativeColor} from "./utils.js";
import {_wrapRegExp} from "./babel.js"

export function logItem({card, align = 'none'} = {}) {
  const el = document.createElement('div')
  el.classList.add('logItem')
  if (align && align !== 'none') {
    el.classList.add('align')
  }
  if (align === 'left') {
    el.classList.add('alignLeft')
  }
  if (align === 'right') {
    el.classList.add('alignRight')
  }
  if (card) {
    const img = document.createElement('img')
    img.classList.add('logItemImage')
    img.src = sanitizeHtml(card.image_url)
    img.alt = sanitizeHtml(card.name)
    el.appendChild(img)
  } else {
    el.classList.add('isFreeform')
  }
  const body = document.createElement('div')
  body.className = 'logItemBody'
  el.appendChild(body)
  el.log = item => {
    if (item instanceof HTMLElement) {
      item = item.outerHTML
    }
    body.innerHTML = item
  }
  return el;
}

function renderAvatar(card, {pos} = {}) {
  const {
    avatarNode: node,
    hp,
    max_hp,
    image_url,
    name,
  } = card;

  node.style.top = '40%';
  if (pos) {
    node.style[pos] = '5%';
  }

  node.querySelector('[data-name]').innerText = name

  let hpText = node.querySelector('[data-hp]');
  hpText.innerText = `HP: ${hp} / ${max_hp}`;



  let hpBar = node.querySelector('[data-hp-bar]');
  hpBar.style.width = hp / max_hp * 100 + '%'
  hpBar.style.backgroundColor = relativeColor(hp, {min: 1, max: max_hp, linear: true})

  let img = node.querySelector('[data-image]');
  img.src = image_url
  img.alt = name
  if (hp <= 0) {
    img.classList.add('deadCard')
  } else {
    img.classList.remove('deadCard')
  }

}

export function initBattle(battle) {
  renderCard(battle.a)
  renderCard(battle.b)
  renderAvatar(battle.a, {pos: 'left'})
  renderAvatar(battle.b, {pos: 'right'})
}

export async function startBattle(battle) {
  const cards = {
    [battle.a.id]: battle.a,
    [battle.b.id]: battle.b,
  }

  document.getElementById('cardBox').open = false;

  const battleStart = logItem()
  battleStart.style.cssText = `
    text-align: center;
    transition: font-size;
    font-weight: bold;
    font-size: 2em;
    text-transform: uppercase;
    pointer-events: none;
  `;
  battleStart.log('Battle Start')

  battle.log.prepend(battleStart)
  console.log('ayy')
  await animate(battleStart, 'animate__zoomIn', '300ms')
  animate(battleStart, 'animate__zoomIn', '300ms').then(() => console.log("then lmao"))
  console.log('lmao')
  await sleep(1000)
  await animate(battleStart, 'animate__zoomOut', '300ms')
  battle.log.removeChild(battleStart)


  let attacker = cards[battle.turns[0].attacker];
  renderCard(attacker, 'attacking')
  const announceAttacker = logItem({card: attacker, align: 'left'})
  announceAttacker.log(`<u>${sanitizeHtml(attacker.name)}</u> goes first due to higher speed.`);
  battle.log.prepend(announceAttacker)
  await sleep(500)


  const firstAttacker = attacker.id

  battle.turns.forEach(function (turn, turnNo) {
    window.setTimeout(function () {
      let attacker = cards[turn.attacker]
      let defender = cards[turn.defender];
      renderCard(attacker, 'attacking')
      renderCard(defender, 'defending')

      const li = logItem({
        card: attacker,
        align: attacker.id === firstAttacker ? 'left' : 'right'
      })
      animate(li, 'animate__fadeInRight', '300ms')
      li.log(turnMessage({turn, cards}))
      battle.log.prepend(li)

      if (['hit', 'kill'].includes(turn.result)) {
        defender.hp = Math.max(0, defender.hp - turn.damage)
      }
      renderCard(attacker, 'attacking')
      renderCard(defender, 'defending')
      renderAvatar(attacker)
      renderAvatar(defender)
      animate(attacker.avatarNode, 'animate__tada', '1s')
      if (turn.result === 'evade') {
        animate(defender.avatarNode, 'animate__slideOutDown', '1s')
      }
      sleep(1100).then(() => {
        if (turn.result === 'kill') {
          animate(
            attacker.avatarNode,
            ['animate__bounce', 'animate__repeat-3'],
            '1s'
          )
        }
        renderCard(attacker, 'defending')
        renderCard(defender, 'attacking')
      })
    }, (turnNo + 1) * 2200)
  })
}

function turnMessage({turn, cards}) {
  const attacker = `<u>${sanitizeHtml(cards[turn.attacker].name)}</u>`;
  const defender = `<u>${sanitizeHtml(cards[turn.defender].name)}</u>`;

  const msg = document.createElement('span')

  if (turn.result === 'evade') {
    msg.innerHTML = `${attacker}'s attack misses`
    return msg;
  }

  if (['hit', 'kill'].includes(turn.result)) {
    msg.innerHTML += `${attacker} hits ${defender} `;

    let dmg = `for ${turn.damage} `
    if (turn.crit) {
      dmg += `with a <strong>critical hit!</strong>`
    }
    msg.innerHTML += dmg
    if (turn.result === 'kill') {
      msg.innerHTML += ` ${defender} is <strong>killed!!</strong>`
    }
    return msg;
  }

  throw Error('cannot make message for turn')

}

export function hydrateTurns(string) {

  const match = string.match(_wrapRegExp(/(v[0-9]+)\.([0-9]+)x([0-9]+)(.+)/i, {
    version: 1,
    atk: 2,
    def: 3,
    payload: 4
  }));

  if (!match) {
    throw new Error('invalid turn format')
  }
  
  const cards = [match.groups['atk'], match.groups['def']].map(s => parseInt(s, 10));

  const results = {
    E: 'evade',
    H: 'hit',
    K: 'kill',
    S: 'standoff',
  }

  return match.groups['payload']
    .split('~')
    .map((str, index) => {
      const m = str.match(_wrapRegExp(/([A-Z])([0-9]+)?(C)?/i, {
        result: 1,
        damage: 2,
        crit: 3
      }))
      if (!m) {
        throw new Error('invalid turn format')
      }
      return m.groups
    })
    .map((turn, turnNumber) => {
      turn['result'] = results[turn['result']] || turn['result']
      turn['attacker'] = cards[turnNumber % 2]
      turn['defender'] = cards[(turnNumber + 1) % 2]
      turn['damage'] = parseInt(turn.damage, 10)
      turn['crit'] = !!turn['crit']
      return turn;
    })
}