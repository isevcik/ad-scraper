async function load() {
    const res = await fetch(`bazos.json?${new Date().valueOf()}`);
    const data = await res.json();
    const sorted = Object.keys(data).sort((a, b) => data[a].time < data[b].time ? -1 : 1)
        .reverse()
        .map(k => data[k])

    const html = sorted.map(i => `<div><a href="${i.link}">${i.name}</a></div>`);

    document.write(html.join(""));
}

load();
// setInterval(() => load(), 5000);