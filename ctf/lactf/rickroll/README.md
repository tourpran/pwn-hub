### Introduction:

Has a constraint on main, so when you return back to main exit will be called. 
- This can be bypassed if you overwrite any of the function in the got to main. 
- Hence you get multiple format string bugs.
- Finally leak libc address and maybe overwrite the got with one_gadget.