const formatDate = (timestamp, time=true) => {
  const date = new Date(timestamp * 1000);

  return time
    ? date.toLocaleString(undefined, {dateStyle:"short", timeStyle:"short"})
    : date.toLocaleDateString();
}

const renderItem = (item) => {

  const div = `<div class="item">
    ${ item.datetimeFormatted } 
    <a href="${item.link}" class="name">${item.name}</a>

    <div class="second-line">
      <span class="price">${ item.price }</span>
      <span class="date">datum na inzeratu: ${ item.originalDateFormatted }</span>
    </div>

    <div>${ item.desc }</div>
    <img src="${ item.img || '' }" loading="lazy">
    </div>
    `;

  return div;
}

const globals = {};

function hydrateItem(item) {
  item.datetimeFormatted = formatDate(item.time);
  item.dateFormatted = formatDate(item.time, false);
  item.originalDateFormatted = formatDate(item.date, false);

  return item;
}

async function load() {
  const res = await fetch(`bazos.json?${new Date().valueOf()}`);
  const data = await res.json();
  const sorted = Object.keys(data).sort((a, b) => data[a].time < data[b].time ? -1 : 1)
    .reverse()
    .map(k => data[k])
    .map(hydrateItem);

  globals.items = sorted;
}

function buildElement(tag, innerHTML) {
  const element = document.createElement(tag);
  element.innerHTML = innerHTML;

  return element;
}

function buildList() {
  const items = globals.items
    // .filter(i => i.dateFormatted === globals.date)
    .map(renderItem);
  const html = items.join("");
  const element = buildElement("div", html);

  globals.body.appendChild(element);
}

function buildMenu() {
  const renderItem = item => {
    return `<li>${ item }</li>`;
  }
  const dates = new Set(globals.items.map(i => i.dateFormatted));
  const five = [...dates]
    .slice(0, 5);
  const html = five
    .map(renderItem)
    .join("");

  const menu = buildElement("ul", html);

  globals.menuDates = dates;
  globals.date = five[0];
  globals.body.appendChild(menu);
  // globals.body.insertAdjacentElement("afterbegin", menu);
}

async function start() {
  globals.body = document.querySelector("body");

  await load();

  // buildMenu();
  buildList();
}

start();

