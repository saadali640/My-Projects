// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stddef.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 9999;

// Hash table
node *table[N];
int counter = 0;



// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    FILE *dictionaryy = fopen(dictionary, "r");
    if (dictionaryy == NULL)
    {
        return false;
    }

    char wordd[LENGTH + 1];

    while (fscanf(dictionaryy, "%s", wordd) != EOF)
    {
        counter++;
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, wordd);

        int hashword = hash(wordd);
        if (table[hashword] == NULL)
        {
            table[hashword] = n;
            n->next = NULL;
        }
        else
        {
            n->next = table[hashword];
            table[hashword] = n;
        }

    }

    fclose(dictionaryy);
    return true;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    int wordd = 0;
    int first = 0;
    int second = 0;
    int third = 0;
    for (int i = 0; i < strlen(word); i++)
        for (int j = i + 1; j < strlen(word); j++)
            for (int k = j + 1; k < strlen(word); k++)
            {
                first += tolower(word[i]);
                second += tolower(word[j]);
                third += tolower(word[k]);
                wordd += first + second + third;
            }

    return wordd % N;
}



// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}



// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashword = hash(word);
    node *ptr = table[hashword];
    while (ptr != NULL)
    {

        while (strcasecmp(ptr->word, word) == 0)
        {
            return true;
        }

        ptr = ptr->next;
    }

    return false;
}



// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {

        while (table[i] != NULL)
        {
            node *cursor = table[i];
            table[i] = table[i]->next;
            node *temp = cursor;
            free(temp);
        }

    }
    return true;
}
