#include <stdlib.h>
#include <math.h>
#include <stdio.h>


int potencia(int base, int expoente) {
    int resultado = 1;
    for (int i = 0; i < expoente; i++) {
        resultado *= base;
    }
    return resultado;
}

int main() {
    int i, n, entrada, decimal;
    
    
    printf("Digite a quantidade de bits: \n");
    scanf("%d", &n);

    if (n <= 0) {
        printf("Valor Invalido!\n");
    } else {
        
        int binario[n]; 

        i = 0;
        decimal = 0;

        
        while (i < n) {
            printf("Digite o %d algarismo binario mais significativo: ", i + 1);
            scanf("%d", &entrada);
            if (entrada != 0 && entrada != 1) {
                printf("Valor Invalido!\n");
            } else {
                binario[i] = entrada;
                i++;
            }
        }

        
        printf("\nValor binario: ");
        for (i = 0; i < n; i++) {
            printf("%d ", binario[i]);
            decimal += binario[i] * potencia(2, (n - (i + 1)));
        }

        
        printf("\nValor decimal: %d\n", decimal);
    }

    return 0; 
}
