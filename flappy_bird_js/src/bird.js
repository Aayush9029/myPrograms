class Bird {
  //OOP, hint: 'object orientated programming'
  constructor(x, y, w, h) {
    this.x = x;
    this.y = y;
    this.width = w;
    this.height = h;
    this.vel = 0;
    this.gravity = 0.5;
    this.lift = -16;
  }
  up() {
    this.vel += this.lift;
  }
  show() {
    fill(0); //the bird has no fill
    stroke(100, 255, 220); //bird outline is cyan color
    rect(this.x, this.y, this.width, this.height);
  }
  update() {
    // this.x = this.x + random(-5, 5);
    this.vel += this.gravity; //velocity increases as obj goes downwards
    this.vel *= 0.9; //adding "wind resistance"
    this.y += this.vel; //object falls down according to vel]

    if (this.y + this.height + 3 >= height) {
      //3 is for the stroke of the bird
      this.y = height - this.height - 3;
      this.vel = 0;
    }
    if (this.y <= 0) {
      this.y = 0;
      this.vel = 0;
    }
  }
}
