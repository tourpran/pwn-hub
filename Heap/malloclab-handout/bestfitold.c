/*
tourpran's DMA

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
    "test",
    /* First member's full name */
    "test",
    /* First member's email address */
    "test",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""
};

// Variables & Macros:

#define ALIGNMENT 16 // 16 byte aligned heap structure.
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~15) // align 16 heap sizes
#define SIZE_T_SIZE 8 // size field in the chunk
#define INITIAL_SIZE 1024*2// initial heap memory (4096)
#define PACK(size, alloc) ((size) | (alloc)) // make a size field with size and allocated bit set
#define QSIZE 8 // each qword size
#define GET(p) (*(unsigned int *)(p)) // get the value at the address
#define PUT(p, val) (*(unsigned int*)(p) = (val)) // set the value at the address
#define HDRP(bp) ((char *)(bp) - QSIZE) //get header of the new chunk
#define ISALLOC(p) (*(unsigned int *)(p))
#define SETFWD(p, val) (*(unsigned int *)(p+8) = (val)) // set the forward pointer for the free chunk
#define SETBACK(p, val) (*(unsigned int *)(p+16) = (val)) // set the backward pointer for the free chunk
#define GETFWD(p) (*(unsigned int *)(p+8))
#define GETBACK(p) (*(unsigned int *)(p+16))


// static void* heap_listp;
// static char* mem_heap;
static char* mem_brk;
// static char* mem_max_addr;
static void* lastfreedchunk;
static int called_mminit = 0;
/*
* extend_heap - get more space in the virtual memory.
*/
void* extend_heap(size_t size){
    char* bp;
    if((long)(bp = mem_sbrk(size)) == -1){
        return NULL;
    }
    //size field
    PUT(bp, PACK(size, 0));
    mem_brk = bp + size;
    return bp;
}

/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    if(called_mminit == 1){
        return 0;
    }
    called_mminit = 1;
    PUT(mem_sbrk(8), PACK(0x5452, 0));
    if((lastfreedchunk = extend_heap(INITIAL_SIZE)) == NULL){
        return -1;
    }
    return 0;
}

/*
* place - makes the malloced area as in-use.
*/
void* place(void* ptr, size_t size){
    PUT(ptr, PACK(size, 1));
    return ptr;
}

/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{

    int newsize = ALIGN(size + SIZE_T_SIZE);

    int min = INITIAL_SIZE;
    void* bestfit = lastfreedchunk;
    void* ptr;
    void* current = lastfreedchunk;

    while(current != 0){
        if((GET(current)-newsize) < min && (GET(current) - newsize) > 0){
            min = GET(current)-newsize;
            bestfit = current;
        }
        current = GETFWD(current);
        printf("%p", current);
    }
    if(GET(bestfit) < newsize){
        return place(extend_heap(newsize), newsize) + 8;
    }
    int old_size = (GET(bestfit)-newsize);

        if(bestfit == lastfreedchunk){
            if(GETFWD(lastfreedchunk) != 0){
                SETBACK(GETFWD(lastfreedchunk), 0);
                lastfreedchunk = GETFWD(lastfreedchunk);
        } 
        ptr = place(bestfit, newsize);
        ptr += 8;
    }
    else{
        if(GETFWD(bestfit) == 0){
            SETFWD(GETBACK(bestfit), 0);
            ptr = place(bestfit, newsize);
            ptr += 8;
        }
        else{
            void* prevchunk = GETBACK(bestfit);
            void* nextchunk = GETFWD(bestfit);
            SETFWD(prevchunk, nextchunk);
            SETBACK(nextchunk, prevchunk);
            ptr = place(bestfit, newsize);
            ptr += 8;
        }
    }
    // Fragmentation
    if(old_size > 0){
        PUT((bestfit + newsize), PACK(old_size, 0));
        lastfreedchunk = bestfit + newsize;
    }

    // top chunk is gone like bruh.
    if(old_size == 0 && GETFWD(lastfreedchunk) == 0){
        void* newheap = extend_heap(INITIAL_SIZE);
        PUT(newheap, INITIAL_SIZE);
        mm_free(newheap +  8);
    }

    return ptr;
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *ptr)
{
    // printf("<- %p - %p ->", ptr, lastfreedchunk);
    ptr -= 8;
    memset(ptr+8, 0, GET(ptr)-8);
    SETFWD(ptr, lastfreedchunk);
    SETBACK(ptr, 0);
    SETBACK(lastfreedchunk, ptr);
    lastfreedchunk = ptr;
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