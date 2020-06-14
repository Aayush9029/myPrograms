var conn;
var peer = new Peer();

peer.on("open", function (id) {
  console.log("My peer ID is:" + id);
  document.getElementById("peerIdDisplay").innerHTML =
    '<b>My peer ID is: </b><font color="red">' + id + "</font>";
});

function ConnectToPeer() {
  var peerId = document.getElementById("peerIdTxtBox").value;
  console.log(peerId);
  conn = peer.connect(peerId);

  peer.on("error", function (err) {
    console.log("error");
  });
}

peer.on("connection", function (conn) {
  console.log("peer connected");
  conn.on("open", function () {
    console.log("conn open");
  });
  conn.on("data", function (data) {
    console.log(data);
  });
});

function SendMessage() {
  conn.send("Hello!");
}
