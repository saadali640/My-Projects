#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    {

        for (int i = 0; i < height; i++)
            for (int j = 0; j < width; j++)
            {
                float rgbt = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue);

               float average = rgbt / 3;

              average = round(average);


                {
                    image[i][j].rgbtRed = average;
                    image[i][j].rgbtGreen = average;
                    image[i][j].rgbtBlue = average;
                }
            }

    }



    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    {

        for (int i = 0; i < height; i++)
            for (int j = 0; j < width; j++)
            {
                float newred = ((image[i][j].rgbtRed * 0.393) + (image[i][j].rgbtGreen * 0.769) + (image[i][j].rgbtBlue * 0.189));
                float newgreen = ((image[i][j].rgbtRed * 0.349) + (image[i][j].rgbtGreen * 0.686) + (image[i][j].rgbtBlue * 0.168));
                float newblue = ((image[i][j].rgbtRed * 0.272) + (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtBlue * 0.131));

                newred = round(newred);
                newgreen = round(newgreen);
                newblue = round(newblue);



                {
                    if (newred > 255)

                                   newred = 255;

                    image[i][j].rgbtRed = newred;

                    if (newgreen > 255)

                                   newgreen = 255;

                    image[i][j].rgbtGreen = newgreen;

                    if (newblue > 255)

                                   newblue = 255;

                    image[i][j].rgbtBlue = newblue;
       }
    }

    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width / 2; j++)
        {

            RGBTRIPLE temp = image[i][width - j - 1];
            image[i][width - j - 1] = image[i][j];
            image[i][j] = temp;

        }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
   RGBTRIPLE temp[height][width];
   {
       for (int i = 0; i < height; i++)
       for (int j = 0; j < width; j++)
        {

                temp[i][j].rgbtRed = image[i][j].rgbtRed;
                temp[i][j].rgbtGreen = image[i][j].rgbtGreen;
                temp[i][j].rgbtBlue = image[i][j].rgbtBlue;

        }
  }

  {
        for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
{
                float newred = 0.00;
                float newgreen = 0.00;
                float newblue = 0.00;
                float counter = 0.00;

                for (int x = - 1; x < 2; x++)
                    for (int y = - 1; y < 2; y++)
                    {

                                     int X = i + x;
                                     int Y = j + y;

                                     if (X < 0 || X > height - 1 || Y < 0 || Y > width - 1)

                                     continue;

         {

                            newred += image[X][Y].rgbtRed;

                            newgreen += image[X][Y].rgbtGreen;

                            newblue += image[X][Y].rgbtBlue;

                            counter++;

                            {

                                temp[i][j].rgbtRed = round(newred / counter);
                                temp[i][j].rgbtGreen = round(newgreen / counter);
                                temp[i][j].rgbtBlue = round(newblue / counter);

                            }
                        }
                    }
            }
    }



   {
      for (int i = 0; i < height; i++)
      for (int j = 0; j < width; j++)
            {

                image[i][j].rgbtRed = temp[i][j].rgbtRed;
                image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
                image[i][j].rgbtBlue = temp[i][j].rgbtBlue;

            }
           }

    return;
}
