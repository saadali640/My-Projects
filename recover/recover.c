#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define SIZE 512

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    FILE *inputfile = fopen(argv[1], "r");


    if (inputfile == NULL)
    {
        printf("Invalid\n");
        return 1;

    }


    int counter = 0;
    uint8_t buffer[SIZE];
    char file[8];
    FILE *outputfile = NULL;

    while (fread(buffer, sizeof(uint8_t), SIZE, inputfile) == SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0 ) == 0xe0)

        {

            sprintf(file, "%03i.jpg", counter);
            outputfile = fopen(file, "w");
            counter++;
        }

        if (outputfile != NULL)

        {
            fwrite(buffer, sizeof(uint8_t), SIZE, outputfile);
        }
    }


    fclose(inputfile);
    fclose(outputfile);

    return 0;

}