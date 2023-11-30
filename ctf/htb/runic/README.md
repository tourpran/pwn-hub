# Challenge Analysis

## Bug:

* The edit function has a bug as they calculate hash after a strcpy there by taking the size field of another chunk and using it or the current chunk.