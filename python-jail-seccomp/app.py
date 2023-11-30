#!/usr/bin/env python3
import seccomp

if __name__ == '__main__':
    f = seccomp.SyscallFilter(defaction=seccomp.ALLOW)
    f.add_rule(seccomp.KILL, 'close')
    f.load()
    eval(input("code: "))
