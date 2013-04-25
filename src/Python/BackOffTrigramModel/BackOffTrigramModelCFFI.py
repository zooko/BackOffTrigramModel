from cffi import FFI

ffi = FFI()

ffi.cdef("""
typedef void* Pvoid_t;

void
read_arpa_file(FILE* arpafile, Pvoid_t* UP, Pvoid_t* UB, Pvoid_t* BP, Pvoid_t* BB, Pvoid_t* TP);

typedef char zbyte;

typedef struct {
size_t len; /* the length of the string (not counting the null-terminating character) */
zbyte* buf; /* pointer to the first byte */
} zstr;

double
unigram_prob_1(zstr unigram, Pvoid_t* pUP);
""")

C = ffi.verify("""
#include "Judy.h"
#include "BackOffTrigramModel.h"
""", 
include_dirs=['src/C/', 'src/util/libzstr/', 'src/util/libzutil/',],
library_dirs=['src/C/'],
libraries=['Judy', 'BackOffTrigramModel']
)

class BackOffTMCFFI:

    def __init__(self, pathtolangmod):
        inf = open(pathtolangmod, 'rU')
        self.UP = ffi.new("Pvoid_t *")
        self.UB = ffi.new("Pvoid_t *")
        self.BP = ffi.new("Pvoid_t *")
        self.BB = ffi.new("Pvoid_t *")
        self.TP = ffi.new("Pvoid_t *")

        C.read_arpa_file(inf, self.UP, self.UB, self.BP, self.BB, self.TP)

    def unigram_prob_1(self, unigram):
        C.unigram_prob_1((len(unigram), unigram), self.UP);

import sys
b = BackOffTMCFFI(sys.argv[1])

b.unigram_prob_1('test')

