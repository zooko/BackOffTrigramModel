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
three_unigrams_unkify_prob_3(size_t uni1_len, const char* uni1_buf, size_t uni2_len, const char* uni2_buf, size_t uni3_len, const char* uni3_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);

typedef void ** PPvoid_t;
typedef const void * Pcvoid_t;

typedef unsigned long    Word_t, * PWord_t;

typedef enum            // uint8_t -- but C does not support this type of enum.
{

        JU_ERRNO_NONE           = 0,
        JU_ERRNO_FULL           = 1,
        JU_ERRNO_NFMAX          = 1,
        JU_ERRNO_NOMEM          = 2,
        JU_ERRNO_NULLPPARRAY    = 3,
        JU_ERRNO_NONNULLPARRAY  = 10,
        JU_ERRNO_NULLPINDEX     = 4,
        JU_ERRNO_NULLPVALUE     = 11,
        JU_ERRNO_NOTJUDY1       = 5,
        JU_ERRNO_NOTJUDYL       = 6,
        JU_ERRNO_NOTJUDYSL      = 7,
        JU_ERRNO_UNSORTED       = 12,
        JU_ERRNO_OVERRUN        = 8,
        JU_ERRNO_CORRUPT        = 9
} JU_Errno_t;

typedef struct J_UDY_ERROR_STRUCT
{
        JU_Errno_t je_Errno;            // one of the enums above.
        int        je_ErrID;            // often an internal source line number.
        Word_t     je_reserved[4];      // for future backward compatibility.
} JError_t, * PJError_t;

PPvoid_t JudySLFirst(     Pcvoid_t,       uint8_t * Index, PJError_t PJError);
PPvoid_t JudySLNext(      Pcvoid_t,       uint8_t * Index, PJError_t PJError);

""")

C = ffi.verify("""
#include "Judy.h"
#include "BackOffTrigramModel.h"
""", 
include_dirs=['/home/zooko/playground/BackOffTrigramModel/src/C/', '/home/zooko/playground/BackOffTrigramModel/src/util/libzstr/', '/home/zooko/playground/BackOffTrigramModel/src/util/libzutil/',],
library_dirs=['/home/zooko/playground/BackOffTrigramModel/src/C/'],
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

    def in_vocabulary(self, unigram):
        return C.unigram_in_vocab(len(unigram.encode('utf-8')), unigram.encode('utf-8'), self.UP);

    def vocabulary_with_prefix(self, prefix):
        assert len(prefix) < 274, len(prefix)
        palimpsest = ffi.new("char[274]")
        assert len(prefix) < len(palimpsest), (len(prefix), len(palimpsest))
        bufo = ffi.buffer(palimpsest)
        assert len(bufo) > len(prefix), (len(bufo), len(prefix))
        bufo[:len(prefix)] = prefix

        ptr = C.JudySLFirst(self.UP[0], palimpsest, ffi.NULL)
        while (ptr is not ffi.NULL):
            pstr = ffi.string(palimpsest)
            if pstr[:len(prefix)] == prefix:
                yield pstr.decode('utf-8')
                ptr = C.JudySLNext(self.UP[0], palimpsest, ffi.NULL)
            else:
                break

    def unigram_probability(self, unigram):
        return C.unigram_prob_1(len(unigram.encode('utf-8')), unigram.encode('utf-8'), self.UP);
        # if C.unigram_in_vocab(len(unigram.encode('utf-8')), unigram.encode('utf-8'), self.UP):
        #     return C.unigram_prob_1(len(unigram.encode('utf-8')), unigram.encode('utf-8'), self.UP);
        # else:
        #     return 0; # XXX What's the right backoff here?

    def trigram_probability(self, unigram1, unigram2, unigram3):
        return C.three_unigrams_unkify_prob_3(len(unigram1.encode('utf-8')), unigram1.encode('utf-8'), len(unigram2.encode('utf-8')), unigram2.encode('utf-8'), len(unigram3.encode('utf-8')), unigram3.encode('utf-8'), self.UP, self.UB, self.BP, self.BB, self.TP);

def test(arpafile):
    b = BackOffTMCFFI(arpafile)

    WORD='ad'


    print "before, WORD: %s" % (WORD,)
    if b.in_vocabulary(WORD):
        print "after, WORD: %s" % (WORD,)
        x = b.unigram_probability(WORD)
        print "%s has prob: %s" % (WORD, x)
    else:
        print "%s does not appear in the corpus" % (WORD,)
    print "after, WORD: %s" % (WORD,)

    print "Okay, now I'm going to try to find all words that begin with the prefix \"%s\"..." % (WORD,)

    z = b.vocabulary_with_prefix(WORD)
    print "z is %s %r :: %s" % (z, z, type(z))

    for x in z:
        print "FOUND ONE! This is so exciting! %r" % (x,)

    print "Okay how about trigram probability..."
    print "a normal word ", b.trigram_probability("a", "normal", "word")
    print "a nice day ", b.trigram_probability("a", "nice", "day")
    print "a good idea", b.trigram_probability("a", "good", "idea")
    print "a bad idea", b.trigram_probability("a", "bad", "idea")
    print "easy angry line", b.trigram_probability("easy", "angry", "line")
    x = b.trigram_probability("contractors", "desktop", "eight")
    print "contractors desktop eight", repr(x)
    x = b.trigram_probability("have", "yet", "to")
    print "have yet to", repr(x)
    assert abs(x + 0.147123) < 0.000001, x


if __name__ == '__main__':
    import sys
    test(sys.argv[1])
