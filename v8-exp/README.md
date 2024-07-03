# V8 Exploitation

## Topics here:

| Ignition - Interpreter: V8 Engine | description | 
| --- | --- |
|[horsepower - picoCTF](./horse_power/) | Exploiting an OOB read and write in array namespace to get shell |
|[*ctf](./starctf/)| Basic Challenge to exploit oob to change the map to get addrof/fakeobj primitive |

| Maglev - compiler: V8 Engine | description | 
| --- | --- |
|[cve-2024-0517](./cve-2024-0517/) | Exploiting `folded allocation`(optimization), causes UAF across Garbage Collection runs. |
|[ArrayShift](./ArrayShift/)| Exploiting a Race Condition between turbofan thread & Main thread through ArrayShift. (Double Reference)|

| Turbofan - JIT Compiler: V8 Engine| Description |
| --- | --- |
|[cve-2018-17463](./cve-2018-17463/)| Exploiting a unrecognised side effect in object.create, which helps to cause type confusion. |
|[math expm1](./expm1-35C3/)| Exploiting an incorrect Range Assumption in Typer.cc and operation-typer.cc. |

| Other JS Engines | Description |
| --- | --- |
|[serenity JIT](./hop/) | Integer Overflow in the assembler phase in the serenity JS Engine. | 
|[QuickJS](./quickJS-libwebp/)| Exploiting a out of bound write due to in sufficient checks in the huffman table generation. (CVE-2023-4863) |
|[General Notes](./note/)| Stuff I take down, during my research while learning v8 exploitation and exploring browsers.|

## Resources:

* jackHalon - https://jhalon.github.io/chrome-browser-exploitation-1/
* saelo     - http://www.phrack.org/issues/70/3.html

## PS

This is my current area of research so will be updating this later when I get time.