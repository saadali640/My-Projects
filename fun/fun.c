#include <stdio.h>


int fun(int n)
{
    if (n == 1)
      //     0
     return 1;                                        //       4        fun(3)                    3
                                                     //        2   15  return 1 + fun(2)     return  3
    else                                            //          0    8    return 1 + fun(1)   return 2
    return 1 + fun(n - 1);                           //          1        return 1
  //       7           2
}


int main()
{
    int n = 3;
    printf("%d\n", fun(n));
                 // fun(4)
    return 0;

}