const { SerialPort, ReadlineParser } = require("serialport");
const util = require("util");
const { EventEmitter } = require("events");
const { mainModule } = require("process");

// const port = new SerialPort({
//   path: "/dev/serial0",
//   baudRate: 115200,
// })
// const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }))
// parser.on('data', console.log)

// const message = Buffer.from('list\r')

// port.write(message,(err)=>{
//   if(err){
//     console.log(err)
//   }
//   console.log('it is written')
// })

// port.on('open', function() {
//   console.log('open')
// })

// class Serial extends EventEmitter{
//   constructor(){
//     super()
//     this.port = new SerialPort({
//       path: "/dev/serial0",
//       baudRate: 115200,
//     })

//     this.port.on('open', ()=> {
//       this.emit('open',()=>{})
//     })
//   }

//   ready(){
//     let p = new Promise((res,rej)=>{
//       this.port.on('open', ()=> {
//         this.emit('open',()=>{})
//         res('open')
//       })
//     })
//     return p
//   }

//   write(data){
//     console.log(data)
//     let p = new Promise((resolve,reject)=>{
//       this.port.write(data,(err,result)=>{
//         if(err){
//           return reject(err)
//         }
//         resolve(result)
//       })
//     })
//     return p

//   }
// }

let port = new SerialPort({
  path: "/dev/serial0",
  baudRate: 115200,
});

function ready() {
  let p = new Promise((res, rej) => {
    port.on("open", () => {
      res("open");
    });
  });
  return p;
}

function write(data) {
  let p = new Promise((resolve, reject) => {
    port.write(data, (err, result) => {
      if (err) {
        return reject(err);
      }
      resolve(result);
    });
  });
  return p;
}

const readLine = port.pipe(new ReadlineParser({ delimiter: "\r\n" }));

module.exports = { ready, write, readLine };
