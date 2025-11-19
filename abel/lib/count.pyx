# cython: language_level=3

from cython.parallel import parallel, threadid
from libc.stdio cimport printf

with nogil, parallel(num_threads=5):
    printf("Thread %d\n", threadid())
