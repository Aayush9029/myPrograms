class Box {
  constructor() {
    this.top = random(height / 2 - 10);
    this.bottom = random(height / 2 - 10);
    this.x = width;
    this.w = 40;
    this.speed = 5;
    this.highlight = false;
  }
  show() {
    if (this.highlight) {
      fill(255, 0, 0, 50);
      stroke(255, 100, 100);
    } else {
      fill(0);
      stroke(255, 200, 100);
    }
    rect(this.x, 0, this.w, this.top);
    rect(this.x, height - this.bottom, this.w, this.bottom);
  }
  update() {
    this.x -= this.speed;
  }
  offscreen() {
    if (this.x < -this.w) {
      return true;
    } else {
      return false;
    }
  }
  hits(bird) {
    if (bird.y < this.top || bird.y > height - this.bottom) {
      if (bird.x > this.x && bird.x < this.x + this.w) {
        this.highlight = true;
        return true;
      }
    } else {
      this.highlight = false;

      return false;
    }
  }
}
