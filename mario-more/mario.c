#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    // prompt user if hight is less than one or greater than eight
    while (n < 1 || n > 8);
    // # per row
    for (int i = 1; i <= n; i++)
    {
        // number of spaces on the left
        for (int s = 1; s < n - i + 1; s++)
        {

            printf(" ");
        }

     // left column
        for (int j = 1; j <= i; j++)
        {


            printf("#");
        }
        // print two spaces between the columns
        printf("  ");
        // right column
        for (int j = 1; j <= i; j++)
        {

            printf("#");
        }
        printf("\n");
    }
}