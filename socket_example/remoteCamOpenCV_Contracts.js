// var t1 = new Date().getTime();
// var t1 = Date.now();

var Web3 = require('web3');
var loadContract = require('./loadContract');
var exec = require('child_process').execSync; //子进程异步执行

// var web3;
//   if (typeof web !== 'undefined')
//       web3 = new Web3(web3.currentProvider);
//   else
//       web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:42024"));

// Web3 1.0
// var account = web3.eth.getBlockNumber(function(err, accounts) { console.log(err, accounts); });
// var account = web3.eth.getCoinbase(function(err, cb) { console.log(err, cb); });
// var account = web3.eth.getAccounts().then(console.log);


var abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":false,"inputs":[{"name":"receiver","type":"address"},{"name":"amount","type":"uint256"}],"name":"sendCoin","outputs":[{"name":"sufficient","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"getTrustLevel","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]';
var abiArray = JSON.parse(abi);
var address = '0x681b34c36f471413492cb262338d1f8e0f61ddda';
var account = "0xc968efa8019d670db8a6a3da22f30613db6a8447";
var otheraccount = account;
var instance = loadContract(abi, address);

// var events = instance.allEvents();
// events.watch(function(error, result){
//   if(!error)
//   console.log(result);
// });

var balance = instance.getBalance(otheraccount);

// console.log("Now IoT device "+ otheraccount+ " is capturing image.\n");
// run the python script1 to capture image from web camera.
var pyscript1 = './pythonScript/client.py';

// nodejs会等待python执行完毕
// nodejs waits for the end of the python script

console.log("\nInteracting with Smart Contract to get computing resources....\n");
console.log("Now the Creditcoin balance is", balance.toNumber(),"Trustcoin");

var trustLevel = instance.getTrustLevel(otheraccount).toNumber();
while(1){
	if( trustLevel != 4 ){
	  console.log("\nThe IoT device does not have enough Credits, service request Denied.\n");
	}else{
	  console.log("*************************************");
	  console.log("\nEnough Credits, service request Accepted.\n");
	  console.log("*************************************");
	  var result = exec('python'+' '+pyscript1 ).toString();
	  console.log(result);
	  // var obj = JSON.parse(result);
	  // console.log("\n@@@\nProcess Result: ", obj.result);


	}
}


// var t2 = new Date().getTime();
// var t2 = Date.now();
// console.log("Execution time: ", t2 - t1);

