> main file: main [mm.c](./mm.c)

### Final Approach for my implementation:
* Used a doubly linked list to maintain all the freechunks. This metadata was stored in the chunk itself.
* Heap Structure:

> malloced
```
|0000000000000000|-size-(+in-use)-|
|0000000000000000|0000000000000000|
                ...
|0000000000000000|0000000000000000|
```

> Freed
```
|0000000000000000|-size-(not-use)-|
|Forward pointer-|Backward pointer|
                ...
|0000000000000000|0000000000000000|
```
* Here with the help of forward pointer I traverse the list and check for the best fit chunk.

### First approach (no score):

* Tried to create a singly linked list struct(explicitly) using extra space and not the metadata in the heap chunk.
* solution was incomplete moved on to next try.

### Second approach (54, 74 score):

* Here I implemented a doubly linked list structure with the help of heap chunk's metadata.
* This DMA is less efficient but faster than the final method since it takes the first chunk that is suitable. 
* After fragmentation a lot of chunk is free and since I didnt coalesce it will remain in bits and pieces.

### Final approach (93 score):

* Doubly linked list with best fit algorithm.
* This is slower in performance as it iterates through the entire free list and selects the suitable chunk for allocation.
* more memory efficient as during fragmentation only minimal amount of memory is fragment. 

### TO-DO:

* this solution will be better if I implement boundary tags (footer + header tags) and coalesce every time free is done.