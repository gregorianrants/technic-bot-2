// const { motorFactory } = require("./Motor/Motor");
// const { MotorSpeed } = require("./MotorSpeed");

// async function main() {
//   console.log("asdfsadfsdfsdf");

//   try {
//     let motor = await motorFactory("C", "left");
//     motor.on("error", (err) => {
//       console.log(err);
//       motor.cleanUp();
//       process.exit(0);
//     });
//     motor.startDataStream();

//     let motorSpeed = new MotorSpeed(motor);
//     //motor.pwm(20);
//     motorSpeed.start();

//     setTimeout(() => {
//       //motor.pwm(0)
//       motor.cleanUp();
//     }, 5000);

//     // motor.on("encoder", (data) => {
//     //   console.log(data);
//     // });

//     process.on("SIGINT", () => {
//       console.info("SIGTERM signal received.");
//       motor.cleanUp();
//       process.exit(0);
//     });
//   } catch (error) {
//     console.log(error);
//     motor.cleanUp();
//   }
// }

// main();

const { motorFactory } = require("./Motor/Motor");
const { MotorSpeed } = require("./MotorSpeed");

function next(f) {
  () => {
    process.nextTick(f);
  };
}

async function main() {
  console.log("asdfsadfsdfsdf");

  try {
    let leftMotor = await motorFactory("C", "left");
    let rightMotor = await motorFactory("D", "right");
    leftMotor.startDataStream();
    rightMotor.startDataStream();

    let leftMotorSpeed = new MotorSpeed(leftMotor);
    let rightMotorSpeed = new MotorSpeed(rightMotor);
    //motor.pwm(20);
    leftMotorSpeed.start();
    rightMotorSpeed.start();

    function cleanUpAndExit() {
      process.nextTick(() => {
        leftMotorSpeed.stop();
        rightMotorSpeed.stop();
        process.nextTick(() => {
          leftMotor.cleanUp();
          rightMotor.cleanUp();
          setTimeout(() => {
            process.exit(0);
          }, 500);
        });
      });
    }

    setTimeout(() => {
      cleanUpAndExit();
    }, 5000);

    process.on("SIGINT", () => {
      cleanUpAndExit();
    });
  } catch (error) {
    console.log(error);
    leftMotor.cleanUp();
    rightMotor.cleanUp();
  }
}

main();
