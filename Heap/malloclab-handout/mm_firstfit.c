void *mm_malloc(size_t size)
{
    int newsize = ALIGN(size + SIZE_T_SIZE);
    void* current = lastfreedchunk;
    while(1==1){
        int ptr = GETFWD(current);

        if((GET(current)-newsize) >= 0){
            int old_size = (GET(current)-newsize);
            ptr = place(current, newsize);
            if(old_size != 0){
                PUT(ptr+newsize, PACK(old_size, 0));
            }
            lastfreedchunk = ptr+newsize;
            return ptr+8;
        }
        if((ptr == 0)){
            return place(extend_heap(newsize), newsize)+8;
        }
        current = ptr;
    }
}