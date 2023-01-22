#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text;
    int count_letters(string text);
    int count_words(string text);
    int count_sentences(string text);
    float sumL;
    float sumS;
    float index;
    int grade;



    // get string

    {

        text = get_string("Text: ");

    }


    // calculate number of letters
    int count_letters(string text);

    float countL = 0;
    {
        for (int i = 0; i < strlen(text); i++)

            if ((text[i] >= 'a' || text[i] >= 'A') && (text[i] <= 'z' || text[i] <= 'Z'))

                 countL++;
    }


    // calculate number of words
    int count_words(string text);

    float countW = 1;
    {

        for (int i = 0; i < strlen(text); i++)

            if (text[i] == ' ')

                 countW++;
     }

    // calculate number of sentences
    int count_sentences(string text);
    float countS = 0;
    {

        for (int i = 0; i < strlen(text); i++)

            if (text[i] == '.' || text[i] == '!' || text[i] == '?')




               countS++;




    }

    // get sum of letters
    {

        sumL = countL / countW * 100;

    }

    // get sum of sentences
    {


        sumS = countS / countW * 100;

    }
    // get index result
    {
        index = 0.0588 * sumL - 0.296 * sumS - 15.8;
        index = roundf(index);
        grade = index;


    }

    // printf


    {
      if (grade > 16)

          printf("Grade 16+\n");

          else if (grade < 1)

              printf("Before Grade 1\n");


         else

              printf("Grade %i\n", grade);
        }
}

