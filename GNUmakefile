NAME=BackOffTrigramModel

INCDIRS=-Isrc/util/libzutil/ -Isrc/util/libzstr/ $(EXTRA_INC_DIRS)
LIBDIRS=-Lsrc/util/libzutil/ -Lsrc/util/libzstr/ $(EXTRA_LIB_DIRS)
LIBS=-lzstr -lzutil -lJudy -lm

LIBPREFIX=lib
STATICLIBSUFFIX=.a
SHAREDLIBSUFFIX=.so

RANLIB=ranlib
AR=ar

DEBUGMODE=True
# DEBUGMODE=False

ifeq ($(DEBUGMODE),True)
CFLAGS=-Wall -O0 -Werror
CFLAGS += -g
LDFLAGS += -g
else
CFLAGS=-Wall -O2
endif

CFLAGS += -fPIC -std=c99

CFLAGS += $(INCDIRS)
LDFLAGS += $(LIBDIRS) $(LIBS)

# SRCS=$(wildcard *.c)
SRCS=src/C/BackOffTrigramModel.c
OBJS=$(SRCS:%.c=%.o)

STATICLIB=src/C/$(LIBPREFIX)$(NAME)$(STATICLIBSUFFIX)
SHAREDLIB=src/C/$(LIBPREFIX)$(NAME)$(SHAREDLIBSUFFIX)


all: $(SHAREDLIB) 

src/util/libzutil/libzutil.a: 
	cd src/util/libzutil && make libzutil.a

src/util/libzstr/libzstr.a: src/util/libzutil/libzutil.a
	cd src/util/libzstr && make libzstr.a

staticlib: $(STATICLIB)

sharedlib: $(SHAREDLIB)

ifeq ($(PYTHON),)
PYTHON=python
endif

$(STATICLIB): $(OBJS)
	$(AR) -r $@ $+
	$(RANLIB) $@

$(SHAREDLIB): $(OBJS) src/util/libzutil/libzutil.a src/util/libzstr/libzstr.a
	$(CC) -o $@ $+ -shared -fPIC $(LDFLAGS)

test:
	PATH=$(PATH):$(PWD)/bin ; export PATH ; cd src/Python/BackOffTrigramModel && $(PYTHON) -m unittest discover

clean:
	-rm $(STATICLIB) $(SHAREDLIB) $(OBJS) *.class 2>/dev/null

.PHONY: clean all staticlib sharedlib
