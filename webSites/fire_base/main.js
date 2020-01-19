let database;
let config = {
  apiKey: "AIzaSyDVeRD0P145hETu39Ryh4HM8rvlTSj4Kos",
  authDomain: "try2-70357.firebaseapp.com",
  databaseURL: "https://try2-70357.firebaseio.com",
  projectId: "try2-70357",
  storageBucket: "",
  messagingSenderId: "99106327684"
};

firebase.initializeApp(config);
database = firebase.database();

let ref = database.ref("clips");
ref.on("value", gotData, errData);

function send2() {
  let ref = database.ref("clips");
  let data = {
    clipboard: "clipboard"
  };
  let result = ref.push(data, dataSent);
  console.log(result.key);

  function dataSent(status) {
    console.log(status);
  }
}

function gotData(data) {
  //clear listing
  console.log("got data" + data);
}

function errData(err) {
  console.log(err);
}
