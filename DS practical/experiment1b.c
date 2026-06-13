#include <stdio.h>
int main()
{
      int a[100], i, search, x = 0, s = 0, e = 9, m, n;

      printf("\n Please Enter the Size of an Array : ");
      scanf("%d", &n);

      printf("\nPlease Enter the Array Elements : \n");
      for (i = 0; i < n; i++)
            scanf("%d", &a[i]);

      printf("Enter a value for search : ");
      scanf("%d", &search);

      while (s <= e)
      {
            m = (s + e) / 2;
            if (a[m] == search)
            {
                  x = 1;
                  break;
            }
            else if (a[m] > search)
            {
                  e = m - 1;
            }
            else if (a[m] < search)
            {
                  s = m + 1;
            }
      }

      if (x == 1)
            printf("found\n");

      else
            printf("not found\n");
}
