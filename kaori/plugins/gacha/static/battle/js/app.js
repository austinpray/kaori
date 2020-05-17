import {hydrateTurns, startBattle, initBattle} from "./battle.js";

function main(battleData) {

  if (!battleData) {
    return;
  }

  document.getElementById('in').value = battleData
  let battle = JSON.parse(battleData)

  battle.turns = hydrateTurns(battle.turns)

  const {a, b} = battle;

  a.hp = a.max_hp
  b.hp = b.max_hp

  console.debug(battle);

  const cardTemplate = document.createElement('div')

  cardTemplate.innerHTML = document.getElementById('cardTemplate').innerText;

  cardTemplate.copyTemplate = function () {
    return this.firstElementChild.cloneNode(true);
  }


  a.node =  cardTemplate.copyTemplate()
  b.node =  cardTemplate.copyTemplate()

  const cardAvatarTemplate = document.createElement('div')

  cardAvatarTemplate.innerHTML = document.getElementById('cardAvatarTemplate').innerText;

  cardAvatarTemplate.copyTemplate = function () {
    return this.firstElementChild.cloneNode(true);
  }

  a.avatarNode = cardAvatarTemplate.copyTemplate()
  b.avatarNode = cardAvatarTemplate.copyTemplate()

  const startButton = document.createElement('button')
  startButton.innerText = 'Start Battle'
  startButton.style.cssText = 'font-size: 1.5em; display: block; margin: 10px auto;'
  let battleStarted = false;
  startButton.addEventListener('click', function () {
    if (!battleStarted) {
      console.debug('battle start')
      startBattle(battle)
      this.disabled = true;
      this.style.display = 'none';
    }
  })


  const log = document.createElement('div')
  log.className = 'battleLog'

  battle.log = log

  const controls = document.getElementById('controls')

  controls.appendChild(log)
  controls.appendChild(startButton)

  document.getElementById('cards').append(a.node, b.node)
  document.getElementById('battlefield').append(a.avatarNode, b.avatarNode)

  initBattle(battle)

}


const params = new URLSearchParams(window.location.search);
const battleData = params.get('in');

main(battleData);

window.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('[data-preload-style]')
    .forEach(link => link.rel = 'stylesheet')
});
