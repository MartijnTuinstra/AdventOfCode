#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"
#include <stdint.h>

#include "AoCLib.c"

int Ncups = 1000001;
int Nmoves = 10000000;

struct linkedlist {
  int value;
  struct linkedlist * next;
};

int findCup(int cup, int *cups, int len){
  int i = 0;
  while( i < len ){
    if (cups[i] == cup) return i;
    i++;
  }
  return -1;
}

// Print first 100 elements
void printCups(struct linkedlist *cups){
  struct linkedlist *head = &(cups[0]);
  struct linkedlist *ptr = &cups[0];
  printf("Cups: {");
  int x = 0;
  do {
    printf("%d, ", ptr->value);
    ptr = ptr->next;
  }
  while(head != ptr && ptr && x++ < 100);

  printf("}\n");
}

int isInList(struct linkedlist cup, struct linkedlist *cups) {
  struct linkedlist *ptr = &cups[0];
  do {
    if (ptr->value == cup.value) return true;
    ptr = ptr->next;
  }
  while(ptr);

  return 0;
}

void iterate(struct linkedlist *cups, struct linkedlist **currentCup) {

  struct linkedlist *selected_cups = 0;
  // remove the elements
  selected_cups = (*currentCup)->next;
  (*currentCup)->next = (*currentCup)->next->next->next->next;
  selected_cups->next->next->next = 0;

  // Calculate destination element
  int destinationValue = (*currentCup)->value - 1;
  while( isInList(cups[destinationValue], selected_cups) || destinationValue == 0) {
    destinationValue--;
    if (destinationValue <= 0) {
      destinationValue = Ncups - 1;
    }
  }

  struct linkedlist * destinationElement = &cups[destinationValue];

  // Put in cups
  struct linkedlist * tmp = destinationElement->next;
  destinationElement->next = selected_cups;
  selected_cups->next->next->next = tmp;
 
}

int main(int argc, char **argv) {

  AoC_Input inData = initAoC(argc, argv);

  if (inData.challengeNr == 1) {
    Ncups = strlen(inData.line->line) + 1;
    Nmoves = 10;
  }
  else {
    Ncups = 1000001;
    Nmoves = 10000000;
  }

  // Initialize array
  struct linkedlist *cups = calloc(Ncups, sizeof(struct linkedlist));

  for (int i = 0; i < strlen(inData.line->line); i++){
    cups[i+1].value = i+1;
    
    char d = inData.line->line[i] - '0';
    char dnext = inData.line->line[i+1];

    if (dnext != '\0'){
      cups[d].next = &cups[dnext - '0'];
    }
    else {
      cups[d].next = &cups[inData.line->line[0] - '0'];
    }
  }

  if (inData.challengeNr == 2) {
    int ix = strlen(inData.line->line)-1;
    char d = inData.line->line[ix] - '0';
    cups[d].next = &cups[10];

    for (int i = 10; i < Ncups; i++){
      cups[i].value = i;
      cups[i].next = &cups[(i+1)%Ncups];
    }
    cups[Ncups - 1].next = &cups[1];
  }

  printCups(&cups[1]);

  struct linkedlist *currentCup = &cups[inData.line->line[0]-'0'];
  for(int i = 0; i < Nmoves; i++) {
    iterate(cups, &currentCup);
    currentCup = currentCup->next;

    if( i % 1000000 == 0)
      printf("%d/%d moves\n", i, Nmoves);


    //printCups(&cups[1]);
  }

  if (inData.challengeNr == 1){
    printCups(&cups[1]);
  }
  else {
    printf(" %d | %d | %d \n", cups[1].value, cups[1].next->value, cups[1].next->next->value);
    printf("%lld\n", (uint64_t)cups[1].next->value * (uint64_t)cups[1].next->next->value);
  }

  return 1;
}  
