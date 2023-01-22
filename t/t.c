#include <stdio.h>
#include <cs50.h>
#include <math.h>
int main(void)


    {
    int remainder;
    int remainder2;
    int remainder3;
    int calculate_quarters;
    int calculate_dimes;
    int calculate_nickels;
    int calculate_pennies;
    int coins;
    int get_cents;

do
    get_cents = get_int("cents: ");
    while (get_cents < 0);



    calculate_quarters = get_cents / 25;



    remainder = get_cents - (25 * calculate_quarters);
    calculate_dimes = remainder / 10;



    remainder2 = remainder - (10 * calculate_dimes);
    calculate_nickels = remainder2 / 5;



    remainder3 = remainder2 - (5 * calculate_nickels);
    calculate_pennies = remainder3 / 1;

 coins = calculate_quarters + calculate_dimes + calculate_nickels + calculate_pennies;


    printf("number of coins = %i\n", coins);




    }