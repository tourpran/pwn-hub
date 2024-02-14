### Bugs:
- get_name: overflow: Intended size is about 16 bytes but the program uses %s there is an overflow.
- fix_typo => setValues: OOB: 
    - check of newline (checks after the 16th byte if its newline or something else)
    - newline or above:
        - skip it.
    - something else:
        - offset = r8d = from 16th byte of our payload 
        - byte = rsi or sil = input byte (we can use this to overwrite the table index which call_indirect uses)
        - mov byte ptr [rcx + r8], sil (rcx is the base, r8: offset, sil: byte)
- Overwriting the call_indirect table:
    ```
    pub unsafe extern "C" fn table_get_lazy_init_func_ref(
        vmctx: *mut VMContext,
        table: u32,
        index: u32
    ) -> *mut u8    
    ```

### WASM:
- call:
    - contains a signature:
        - return type.
        - Argument types.
    - call is made with this signature.
- call_indirect:
    - makes use of a function table.
    - call rcx : for option 3, joke
    - call r11 : for option 2, math
