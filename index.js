const globals = {
  definitions: [
    { key: "Domy", file: "bazosreality_dum.json" },
    { key: "Domy", file: "bezrealitky.json" },
    { key: "Pozemky", file: "bazosreality_pozemek.json" },
  ],
};

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
    <a href="${item.link}" target="_blank" class="name"><strong>⧉</strong></a>

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

function hydrateItem(item) {
  item.datetimeFormatted = formatDate(item.time);
  item.dateFormatted = formatDate(item.time, false);
  item.originalDateFormatted = formatDate(item.date, false);

  return item;
}

async function load() {
  const responses = await Promise.all(globals.definitions.map(d => fetch(`${d.file}?${new Date().valueOf()}`)));
  const lists = await Promise.all(responses.map(r => r.json()));
  lists.forEach((list, index) => {
    const key = globals.definitions[index].key;
    Object.values(list).forEach(e => e.key = key);
  });
  const data = Object.assign({}, ...lists);

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

function buildList(key) {
  const items = globals.items
    // .filter(i => i.dateFormatted === globals.date)
    .filter(i => !key || i.key === key)
    .map(renderItem);
  const html = items.join("");
  const element = buildElement("div", html);

  globals.list.innerHTML = "";
  globals.list.appendChild(element);
}

function buildMenu() {
  const renderItem = item => {
    return `<li><a href="#${ item }">${ item }</a></li>`;
  }
  // const dates = new Set(globals.items.map(i => i.dateFormatted));
  // const five = [...dates]
    // .slice(0, 5);
  // const html = five
  //   .map(renderItem)
  //   .join("");

  const html = [...new Set(globals.definitions.map(d => d.key))]
    .map(renderItem)
    .join("");
  const menu = buildElement("ul", html);

  globals.menu.appendChild(menu);
}

function getKey() {
  const key = location.hash.slice(1);
  return key;
}

function onHashChanged() {
  const key = getKey();
  buildList(key);
}

async function start() {
  globals.menu = document.querySelector(".menu");
  globals.list = document.querySelector(".list");
  window.addEventListener("hashchange", onHashChanged);

  await load();

  buildMenu();

  const key = getKey();
  if (key) {
    buildList(key);
  } else {
    location.hash = "#Domy";
  }
}

start();

