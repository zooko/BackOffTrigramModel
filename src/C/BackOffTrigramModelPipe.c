#include <string.h>
#include <stdio.h>

#include "zstr.h"

#include "BackOffTrigramModel.h"

#include "Judy.h"

#include <assert.h>

int
main(int argc, char** argv) {
        if (argc < 2) {
                printf("usage: BackOffTrigramModelPipe arpafile\n");
                return 1;
        }

        FILE* arpafile = fopen(argv[1], "r");

        Pvoid_t UP = (Pvoid_t) NULL; /* map from unigram to probability */
        Pvoid_t UB = (Pvoid_t) NULL; /* map from unigram to backoff */
        Pvoid_t BP = (Pvoid_t) NULL; /* map from bigram to probability */
        Pvoid_t BB = (Pvoid_t) NULL; /* map from bigram to backoff */
        Pvoid_t TP = (Pvoid_t) NULL; /* map from trigram to probability */

        read_arpa_file(arpafile, &UP, &UB, &BP, &BB, &TP);

        zbyte inputbuf[MAXTRIGRAMSIZE + 4];
        zbyte* p;
        PWord_t ptr;

        size_t i;
        do {
                fgets((char*)inputbuf, MAXTRIGRAMSIZE + 4, stdin);
                i = strlen((char*)inputbuf);
                if (inputbuf[i-1] == '\n') {
                        inputbuf[--i] = '\0';
                } else {
                        inputbuf[i] = '\0';
                }

                p = inputbuf;
                if (*p == 'u'){ // unigram probability
                        p+=2; // command and space
                        float uniprob = unigram_prob_1(cs_as_z((char*)p), &UP);
                        printf("%f\n", uniprob);
                        fflush(stdout);
                }

                else if (*p == 'o'){ // unigram backoff
                        p+=2; // command and space
                        JSLG(ptr, UB, p);
                        if (ptr == NULL) {
                            printf("1\n");
                            fflush(stdout);
                        }
                        else {
                            printf("%f\n", *(float*)ptr);
                            fflush(stdout);
                        }
                }

                else if (*p == 't') { // trigram probability
                        p+=2; // command and space
                        float triprob = trigram_split_unkify_prob_3(cs_as_z((char*)p), &UP, &UB, &BP, &BB, &TP);
                        printf("%f\n", triprob);
                        fflush(stdout);
                        /* printf(inputbuf); */
                }

                else if (*p == 'v') { // in vocabulary
                        p+=2; // command and space
                        JSLG(ptr, UP, p);
                        if (ptr == NULL) {
                                printf("0\n");
                                fflush(stdout);
                        }
                        else {
                                printf("1\n");
                                fflush(stdout);
                        }
                }

                else if (*p == 'w') { // trigram attested
                        p+=2; // command and space
                        JSLG(ptr, TP, p);
                        if (ptr == NULL) {
                                printf("0\n");
                                fflush(stdout);
                        }
                        else {
                                printf("1\n");
                                fflush(stdout);
                        }
                }

		else if (*p == 'U') { // is this a unk model? prob of unk?
			*p = UNKBYTESTR[0];
			JSLG(ptr, UP, p);
                        if (ptr == NULL) {
                                printf("None\n");
                                fflush(stdout);
                        }
                        else {
                                printf("%f\n", *(float*)ptr);
                                fflush(stdout);
                        }
		}
                else if (*p == 'p') { // in vocabulary
		  p+=2; // command and space
		  size_t prefixlength = i - 2;
		  zbyte prefix[MAXUNIGRAMSIZE];
		  memcpy (prefix, p, prefixlength);
		  JSLF(ptr, UP, p);
		  while ((ptr != NULL) && (memcmp(p, prefix, prefixlength) == 0)) {
		    printf("%s ", p);
		    fflush(stdout);
		    JSLN(ptr, UP, p);
		  }
		  printf("\n");
		  fflush(stdout);
		}
			


        } while (
            (i > 0) &&
            (feof(stdin) == 0) &&
            (ferror(stdin) == 0)
            );

        Word_t temp;
        JSLFA(temp, UP);
        JSLFA(temp, UB);
        JSLFA(temp, BP);
        JSLFA(temp, BB);
        JSLFA(temp, TP);

        fflush(stdout);
        return 0;
}
