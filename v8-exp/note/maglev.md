# Maglev

## Design Docs:
- SSA compiler purely made for the speed compilation. Also Designed for concurrency.
- Graph building: Same as turbofan. (with suitable mergin of jump targets).
- Immediate lowering: with the feedback given from the initial stage we try to lower the instruction as much as possible. (Also using the IC stored properly).

## Code Generation:
- Preprocessing:
    - Assign ID to all the nodes.
    - Calculate the live range and know how long a node survives in the CFG ?
    - requirement of what the codegen are based on the input and output, helps the register allocator to resolve only specific registers.
- Register Allocations:
    - basically uses the regiters when a specific node needs, can also ask several regs for input.
- Machine code generation:
    - Converts the nodes into the specific machine code using the Macro-assembler. 
- Kicks in when there is around 400 invocations of a specific code. Sits after the sparkplug and the turbofan.

![](./image-1.png)

## OSR:
- if there is a function f() calling and a small function g() then in the stack there will be 2 seperate frames for f and g, which will be merged into 1, this is OSR.

## Code Audit (High Level): 
- compile:
    - Start the graph building phase:
        - Initializes and Allocates the registers whereever it is necessary, not sure.
        - loop peeling: bring some computation out of the loop, for better performance. Merges the above and below offsets that were peeled? 
        - Starting the collection of liveness for each node for build_merge_states
    - Also find some dead code points. too much complexity and depth so leaving as such.
    - phi untagging:
        - make the phi node untagged: meaning untag it from the input nodes they were born from. 
        - maglev removes untagged phi and keeps some of it which can't be untagged.
        - So where ever it is possible, it will convert the tagged phi to simpler types like smi, double ...

### Questions to asnwer:
- What is maglev:
- When does it kick in: 
- What is the high level architecture - (bytecode is converted to maglev IR -> lowered into assembly):
- What each file does on a high level:
- opt pipeline if any:
- where is the code gen: