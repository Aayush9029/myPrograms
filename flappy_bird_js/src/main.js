let boxes = [];
num_boxes = 60; // higher num == less boxes
points = 0;
box_respawn_speed = 5;

function setup() {
  createCanvas(600, 400);
  bird = new Bird(100, 0, 30, 30);
  boxes.push(new Box());
  let a = document.getElementById("score");
  console.log(a);
}

function draw() {
  background(0, 150);
  for (let i = boxes.length - 1; i >= 0; i--) {
    boxes[i].show();
    boxes[i].update();
    if (boxes[i].hits(bird)) {
      // what happens when the box gets hit
      // console.log('hit?')
    }
    if (boxes[i].offscreen()) {
      boxes.splice(i, 1);
      points++;
      if (points % 10 == 0) {
        num_boxes -= box_respawn_speed;
      }
      if (num_boxes < -60) {
        box_respawn_speed *= -1;
      }
    }
  }

  bird.show();
  bird.update();

  if (frameCount % num_boxes == 0) {
    boxes.push(new Box());
  }
}

function keyPressed() {
  //executes when a key is pressed
  if (keyCode == 32) {
    // 32 is keycode for space bar
    bird.up(); //executes up "fumction" from bird object
  }
}
