/*
=> tourpran's DMA
* Simple Dynamic Memory Allocator with possible bugs.
* free: Focused on maintaining a doubly linked list.
* malloc: Uses the best fit algorithm to iterate through the free list and fit chunk to malloc.
*/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "bi0s",
    /* First member's full name */
    "tourpran",
    /* First member's email address */
    "random@random.ninja",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""
};

// Variables & Macros:

#define INT_MAX 2147483647 // a very big number
#define ALIGNMENT 16 // 16 byte aligned heap structure.
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~15) // align 16 heap sizes
#define SIZE_T_SIZE 8 // size field in the chunk
#define INITIAL_SIZE 32 // initial heap memory (???)
#define QSIZE 8 // each qword size
#define PACK(size, alloc) (size | alloc) //just set the 1 to indicate its in-use 
#define GET(p) (*(unsigned int *)(p)) // get the value at the address
#define PUT(p, val) (*(unsigned int*)(p) = (val)) // set the value at the address
#define SETFWD(p, val) (*(unsigned int *)(p+8) = (val)) // set the forward pointer for the free chunk
#define SETBACK(p, val) (*(unsigned int *)(p+16) = (val)) // set the backward pointer for the free chunk
#define GETFWD(p) (*(unsigned int *)(p+8)) // get the forward pointer
#define GETBACK(p) (*(unsigned int *)(p+16)) // get the backward pointer
#define FPACK(p) (((*(unsigned int *)(p))>>1)<<1) // just helps to make the in-use bit to 0 

static void* lastfreedchunk;
static int called_mminit = 0;
static int freechunkcount = 0;

/*
* extend_heap - get more space in the virtual memory.
*/
void* extend_heap(size_t size){
    char* bp;
    if((long)(bp = mem_sbrk(size)) == -1){
        return NULL;
    }
    //size field
    PUT(bp, size);
    return bp;
}

/* 
 * mm_init - initialize the malloc package.
 * Creates the first free chunk.
 */
int mm_init(void)
{
    if(called_mminit == 1){
        return 0;
    }
    called_mminit = 1;
    if((lastfreedchunk = extend_heap(INITIAL_SIZE)) == NULL){
        return -1;
    }
    return 0;
}

/*
* place - absolutely do nothing.
* also memset the area for fresh use
* this helps to clear out old dangling pointer.
*/
void* place(void* ptr, size_t size){
    PUT(ptr, PACK(size, 1));
    memset(ptr+8, 0, size-8);
    return ptr;
}

/* 
 * mm_malloc:
 * Find the suitable chunk to allocate using best fit algorithm.
 * change the free list.
 */
void *mm_malloc(size_t size)
{
    int newsize = ALIGN(size + SIZE_T_SIZE);

    if(lastfreedchunk == NULL){
        return (place(extend_heap(newsize), newsize)+8);
    }

    void* current = lastfreedchunk;
    void* bestfit = NULL;
    void* ptr;

    int min = INT_MAX;
    int tmp = 0;
    while(tmp < freechunkcount && current != NULL){
        if(((GET(current)-newsize) < min) && ((GET(current)-newsize) >= 0)){
            min = GET(current) - newsize;
            bestfit = current;
        }
        current = GETFWD(current);
        tmp++;
    }
    // two cases: found chunk or nope.
    int old_size = -1;
    if(bestfit == NULL){
        // no chunk found so no space.
        ptr = place(extend_heap(newsize), newsize);
    }
    else{
        freechunkcount--; //decrement since a new chunk is allocated from the free chunk.
        old_size = GET(bestfit) - newsize;
        //four cases: only chunk, head, middle, tail
        ptr = place(bestfit, newsize);
        if(GETBACK(lastfreedchunk) == 0 && GETFWD(lastfreedchunk) == 0){
            // my life be like ooooh aaaah
            lastfreedchunk = 0;
        }
        else if(GETBACK(lastfreedchunk) == 0){
            memset(GETFWD(lastfreedchunk)+16, 0, 8);
        }
        else if(GETFWD(lastfreedchunk) == 0){
            memset(GETBACK(lastfreedchunk)+8, 0, 8);
        }
        else{
            void* prev = GETBACK(lastfreedchunk);
            void* next = GETFWD(lastfreedchunk);
            SETBACK(next, prev);
            SETFWD(prev, next);
        }
        //Fragmentation:
        if(old_size > 0){
            PUT((bestfit + newsize), old_size);
            mm_free(bestfit+newsize+8);
        }
    }
    return (ptr+8);
}

/*
 * mm_free - Free a block:
 * zero out all the bytes
 * change the free list structure (lastfreechunk)
 */
void mm_free(void *ptr)
{
    ptr -= 8;
    PUT(ptr, FPACK(ptr));
    if(lastfreedchunk == NULL){
        lastfreedchunk = ptr;
        freechunkcount = 0;
        return;
    }

    //prevent double free like dugh.
    void* current = lastfreedchunk;
    int tmp = 0;
    while(current != NULL && tmp < freechunkcount){
        if(ptr == current){
            return;
        }
        current = GETFWD(current);
        tmp += 1;
    }
    //zero out only the FWD, BACK ptr :P
    if(GET(ptr) != 0){
        memset(ptr+8, 0, GET(ptr)-8);
    }
    SETFWD(ptr, lastfreedchunk);
    SETBACK(ptr, 0);
    SETBACK(lastfreedchunk, ptr);
    lastfreedchunk = ptr;
    freechunkcount++; //increment the counter
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    void *oldptr = ptr;
    void *newptr;
    size_t copySize;
    
    newptr = mm_malloc(size);
    if (newptr == NULL)
      return NULL;
    copySize = *(size_t *)((char *)oldptr - SIZE_T_SIZE);
    if (size < copySize)
      copySize = size;
    memcpy(newptr, oldptr, copySize);
    mm_free(oldptr);
    return newptr;
}