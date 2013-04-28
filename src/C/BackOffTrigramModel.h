#include "Judy.h"
#include "zstr.h"

const static size_t MAXWORDSIZE=256;
const static size_t MAXUNIGRAMSIZE=17 + 256;
#define MAXBIGRAMSIZE ((size_t)(17 + 2 * MAXWORDSIZE))
#define MAXTRIGRAMSIZE ((size_t)(17 + 3 * MAXWORDSIZE))

const static uint8_t UNKBYTESTR[]={0xFF, 0};


void
read_arpa_file(FILE* arpafile, Pvoid_t* UP, Pvoid_t* UB, Pvoid_t* BP, Pvoid_t* BB, Pvoid_t* TP);

/**
 * The following three functions are defined by this equation:
 *
 * p(wd3|wd1,wd2)= if(trigram exists)           p_3(wd1,wd2,wd3)
 *                 else if(bigram w1,w2 exists) bo_wt_2(w1,w2)*p(wd3|wd2)
 *                 else                         p(wd3|w2)
 * 
 * p(wd2|wd1)= if(bigram exists) p_2(wd1,wd2)
 *            else              bo_wt_1(wd1)*p_1(wd2)
 * 
 */

int
unigram_in_vocab(size_t unigram_len, const char* unigram_buf, Pvoid_t* pUP);

double
unigram_prob_1(size_t unigram_len, const char* unigram_buf, Pvoid_t* pUP);

double
bigram_prob_2(size_t bigram_len, const char* bigram_buf, size_t unigram1_len, const char* unigram1_buf, size_t unigram2_len, const char* unigram2_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP);

/**
 * The data must be pre-unkified (using our 0xFF unk marker).
 */
double
trigram_prob_3(size_t trigram_len, const char* trigram_buf, size_t bigram1_len, const char* bigram1_buf, size_t bigram2_len, const char* bigram2_buf, size_t unigram1_len, const char* unigram1_buf, size_t unigram2_len, const char* unigram2_buf, size_t unigram3_len, const char* unigram3_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);

/* Set the .buf and .len members of pbi1, pbi2, puni1, puni2, and puni3 to 
 * point to the substrings of the trigram, as separated by the ' ' char.
 * In addition, test each unigram for knownness, if any of the unigrams are 
 * unknown, then create an unkified copy of tri in buf, and set the pointers 
 * of putri, pubi1, pubi2, puuni1, puuni2, and puuni3 to point into buf.
 * If all unigrams are known, then the pointers of the "pu" variables will be 
 * set to point into the original trigram in the tri variable instead.
 *
 * @precondition utri.buf points to space which is sufficient to hold a copy of tri
 */
void
split_trigram_and_unkify_in_place(size_t tri_len, const char* tri_buf, char* buf, size_t* pbi1_len_p, const char** pbi1_buf_p, size_t* pbi2_len_p, const char** pbi2_buf_p, size_t* puni1_len_p, const char** puni1_buf_p, size_t* punit2_len_p, const char** puni2_buf_p, size_t* puni3_len_p, const char** puni3_buf_p, size_t* putri_len_p, const char** putri_buf_p, size_t* pubi1_len_p, const char** pubi1_buf_p, size_t* pubi2_len_p, const char** pubi2_buf_p, size_t* puuni1_len_p, const char** puuni1_buf_p, size_t* puuni2_len_p, const char** puuni2_buf_p, size_t* puuni3_len_p, const char** puuni3_buf_p, Pvoid_t* pUP);

double 
trigram_split_unkify_prob_3(size_t tri_len, const char* tri_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);

double
three_unigrams_unkify_prob_3(size_t uni1_len, const char* uni1_buf, size_t uni2_len, const char* uni2_buf, size_t uni3_len, const char* uni3_buf, Pvoid_t* pUP, Pvoid_t* pUB, Pvoid_t* pBP, Pvoid_t* pBB, Pvoid_t* pTP);

