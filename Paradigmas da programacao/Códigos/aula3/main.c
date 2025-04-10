#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int potencia(int base, int expoente){
    int x, potencia;

    x++;
    potencia++;

    while (x <= expoente){
        potencia = base * potencia;
        x++;
    }
    return potencia;
}

void main(){
    system("cls");
    int i, n, entrada, decimal;
    int binario[32];

    printf("Digite o Algorismo Binario: ");
    scanf("%d", &n);

    if (n <= 0 ) printf("Algarismo Invalido\n");

    else{
        i = 0;
        decimal = 0;
        while (i < n){
            printf("Digite o %d algarismo binario mais significativo: ",i + 1);
            scanf("%d", &entrada);
            if (entrada != 0 && entrada != 1){
                printf("Algarismo Invalido\n");
                break;
            }
            else{
                binario[i] = entrada; 
                i++;
            }
        }
        printf("\nO Algorismo Binario e: ");
        for (i = 0; i < n; i++){
            printf("%d", binario[i]);
            decimal += binario[i] * pow(2, (n - (i + 1)));
        }
        printf("\nO Algorismo Decimal e: %d\n", decimal);
    }
}