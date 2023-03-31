const { motorFactory } = require("./Motor/Motor");
const { MotorSpeed } = require("./MotorSpeed");
const { setTimeout } = require("timers/promises");

function next(f) {
  () => {
    process.nextTick(f);
  };
}

async function main() {
  console.log("asdfsadfsdfsdf");

  try {
    let leftMotor = await motorFactory("C", "left");
    //let rightMotor = await motorFactory("D", "right");
    leftMotor.startDataStream();
    //rightMotor.startDataStream();

    let leftMotorSpeed = new MotorSpeed(leftMotor);
    //let rightMotorSpeed = new MotorSpeed(rightMotor);
    //motor.pwm(20);
    leftMotorSpeed.start(20);
    //rightMotorSpeed.start(20);

    function cleanUpAndExit() {
      process.nextTick(() => {
        leftMotorSpeed.stop();
        //rightMotorSpeed.stop();
        process.nextTick(() => {
          leftMotor.cleanUp();
          //rightMotor.cleanUp();
          setTimeout(500).then(() => process.exit(0));
        });
      });
    }

    async function run() {
      leftMotorSpeed.start(30);
      //rightMotorSpeed.start(20);
      leftMotorSpeed.setPoint = 30;
      for (i = 0; i < 25; i++) {
        await setTimeout(200);
        leftMotorSpeed.setPoint += 1;
      }
      console.log("out of loop");

      //rightMotorSpeed.setPoint = 40;
      await setTimeout(5000);
      cleanUpAndExit();
    }

    run();

    process
      .on("SIGINT", () => {
        cleanUpAndExit();
      })
      .on("uncaughtException", (err) => {
        console.error(err, "Uncaught Exception thrown");
        cleanUpAndExit();
        process.exit(1);
      });
  } catch (error) {
    console.log(error);
    leftMotor.cleanUp();
    //rightMotor.cleanUp();
  }
}

main();
