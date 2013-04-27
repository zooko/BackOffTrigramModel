from cffi import FFI

ffi = FFI()

ffi.cdef("""
typedef void* Pvoid_t;

void
read_arpa_file(FILE* arpafile, Pvoid_t* UP, Pvoid_t* UB, Pvoid_t* BP, Pvoid_t* BB, Pvoid_t* TP);

int
unigram_in_vocab(size_t unigram_len, const char* unigram_buf, Pvoid_t* pUP);

double
unigram_prob_1(size_t unigram_len, const char* unigram_buf, Pvoid_t* pUP);

double
bigram_prob_2(size_t bigram_len, const char* bigram_buf, size_t unigram1_len, const char* unigram1_buf, size_t unigram2_len, const char* unigram2_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP);

double
trigram_prob_3(size_t trigram_len, const char* trigram_buf, size_t bigram1_len, const char* bigram1_buf, size_t bigram2_len, const char* bigram2_buf, size_t unigram1_len, const char* unigram1_buf, size_t unigram2_len, const char* unigram2_buf, size_t unigram3_len, const char* unigram3_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);

void
split_trigram_and_unkify_in_place(size_t tri_len, const char* tri_buf, char* buf, size_t* pbi1_len_p, const char** pbi1_buf_p, size_t* pbi2_len_p, const char** pbi2_buf_p, size_t* puni1_len_p, const char** puni1_buf_p, size_t* punit2_len_p, const char** puni2_buf_p, size_t* puni3_len_p, const char** puni3_buf_p, size_t* putri_len_p, const char** putri_buf_p, size_t* pubi1_len_p, const char** pubi1_buf_p, size_t* pubi2_len_p, const char** pubi2_buf_p, size_t* puuni1_len_p, const char** puuni1_buf_p, size_t* puuni2_len_p, const char** puuni2_buf_p, size_t* puuni3_len_p, const char** puuni3_buf_p, Pvoid_t* pUP);

double 
trigram_split_unkify_prob_3(size_t tri_len, const char* tri_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);
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

    def unigram_in_vocab(self, unigram):
        return C.unigram_in_vocab(len(unigram), unigram, self.UP);

    def unigram_prob_1(self, unigram):
        return C.unigram_prob_1(len(unigram), unigram, self.UP);


import sys
b = BackOffTMCFFI(sys.argv[1])

x = b.unigram_prob_1('JJR')

