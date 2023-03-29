const { motorFactory } = require("./Motor");

async function main() {
  console.log("asdfsadfsdfsdf");

  try {
    let motor = await motorFactory("C", "left");
    motor.startDataStream();
    motor.pwm(40);

    setTimeout(() => {
      //motor.pwm(0)
      motor.cleanUp();
    }, 5000);

    motor.on("encoder", (data) => {
      console.log(data);
    });

    process.on("SIGINT", () => {
      console.info("SIGTERM signal received.");
      motor.cleanUp();
      process.exit(0);
    });
  } catch (error) {
    motor.cleanUp();
  }
}

main();
