let names = [];
let quotes = [];
let i = 0;
fetch("./data.json")
  .then((response) => response.json())
  .then((data) => {
    for (const d of data) {
      names.push(d["name"]);
      quotes.push(d["quote"]);
    }
  });

document.getElementById("body").addEventListener("keydown", forward);

function forward(e) {
  let saying = document.getElementById("saying");
  let by = document.getElementById("by");

  saying.innerHTML = quotes[i];
  if (names[i] != "") {
    by.innerHTML = "- " + names[i];
  }

  i += e.key != " " ? 1 : -1;
  console.log(i);
}
