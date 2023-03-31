const serial = require("../Serial");
const { EventEmitter } = require("events");
const { resolve } = require("path");
const { MotorSpeed } = require("../MotorSpeed");

MODES = {
  PWM: "PWM",
};

class Motor extends EventEmitter {
  constructor(port, serial, direction = 1) {
    super();
    this.serial = serial;
    const portLetters = ["A", "B", "C", "D"];
    this.portLetter = port;
    this.direction = direction;
    let portIndex = portLetters.indexOf(this.portLetter);
    if (portIndex === "-1") {
      throw new Error("you must provide a valid port letter");
    }
    this.portIndex = portIndex;
    this.handleData.bind(this);
    this.wheelDiameter = 276; //mm
    this.on("error", (err) => {
      console.error(err);
      this.cleanUp();
    });
    //this.motor_speed = MotorSpeed()
    this.mode = MODES.PWM;
    this._pwm = 0;
  }

  write(data) {
    let str = `port ${this.portIndex}; ${data}\r`;
    let buf = Buffer.from(str);
    return this.serial
      .write(buf)
      .then((res) => {})
      .catch((err) => {
        console.log("fuck", err);
      });
  }

  getDistance(pos) {
    const distance = (pos / 360) * this.wheel_diameter;
    return distance;
  }

  calculateSpeed(aSpeed) {
    const speed = (aSpeed / 360) * this.wheelDiameter;
    return speed;
  }

  setBias(bias = 0.4) {
    let data = `bias ${bias}`;
    return this.serial.write(data);
  }

  setPlimit(plimit = 1) {
    let data = `plimit ${plimit}`;
    return this.serial.write(data);
  }

  set pwm(power) {
    //console.log("pwm", power);
    power = (power * this.direction) / 100;
    if (power > 1 || power < -1) {
      this.emit("error", new Error("power must be between -1 and 1"));
    }
    let data = `pwm; set ${power}`;
    return this.write(data).then(() => (this._pwm = power));
  }

  get pwm() {
    return this._pwm * 100;
  }

  handleData = (line) => {
    try {
      if (line.slice(0, 5) == `P${this.portIndex.toString()}C0:`) {
        let [portInfo, speed, pos, apos] = line.split(/\s+/);
        [speed, pos, apos] = [speed, pos, apos].map(
          (val) => Number(val) * this.direction
        );
        speed = this.calculateSpeed(speed);
        const data = { portIndex: this.portIndex, speed, pos, apos };
        //console.log(data);
        this.emit("encoder", data);
      }
    } catch (err) {
      this.emit("error", err);
    }
  };

  startDataStream() {
    let data = `select 0; selrate 10`;
    this.write(data);
    serial.readLine.on("data", this.handleData);
  }

  stopDataStream() {
    this.write("select");
    //TODO remove readline listener as well
    serial.readLine.removeListener("data", this.handleData);
  }

  cleanUp() {
    console.log("in clean");
    this.stopDataStream();
    this.pwm = 0;
  }
}

const serialIsReady = serial.ready();

async function motorFactory(port, side) {
  if (side == "left") {
    direction = -1;
  } else {
    direction = 1;
  }
  const motor = new Motor(port, serial, direction);
  console.log("asdfsadfsdf");
  await serialIsReady;
  await motor.setBias();
  await motor.setPlimit();
  return motor;
}

module.exports = { motorFactory };
