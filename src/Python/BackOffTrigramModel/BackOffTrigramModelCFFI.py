from cffi import FFI

ffi = FFI()

ffi.cdef("""
typedef void* Pvoid_t;
void
read_arpa_file(FILE* arpafile, Pvoid_t* UP, Pvoid_t* UB, Pvoid_t* BP, Pvoid_t* BB, Pvoid_t* TP);
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
        UP = None
        UB = None
        BP = None
        BB = None
        TP = None

        ffi.read_arpa_file(inf, UP, UB, BP, BB, TP)
