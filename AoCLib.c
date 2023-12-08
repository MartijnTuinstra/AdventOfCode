#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"
#include "stdint.h"
#include "string.h"

typedef struct TextLineStruct TextLine;

struct TextLineStruct {
  char * line;
  TextLine * next;
};

typedef struct {
  char * inData;
  TextLine * line;

  int challengeNr;
} AoC_Input;

AoC_Input initAoC(int argc, char **argv) {
  AoC_Input in = {NULL, NULL, -1};

  if (argc < 2) {
    printf("Not enough arguments");
    return in;
  }

  in.challengeNr = atoi(argv[1]);

  FILE *fptr;
  fptr = fopen(argv[2], "r");

  if (!fptr) {
    printf("Cannot open file %s\n", argv[2]);
    return in;
  }

  fseek(fptr, 0L, SEEK_END);
  int size = ftell(fptr);
  fseek(fptr, 0L, SEEK_SET);

  in.inData = calloc( size+5, sizeof(char) );

  fgets(in.inData, size+5, fptr);

  fclose(fptr);

  TextLine ** ptr = &in.line;
  char * token = strtok(in.inData, "\n");
  while ( token != NULL ) {
    *ptr = malloc( sizeof(TextLine) );

    (*ptr)->line = token;
    (*ptr)->next = NULL;
    ptr = &((*ptr)->next);

    token = strtok(NULL, "\n");
  }

  return in;
}
