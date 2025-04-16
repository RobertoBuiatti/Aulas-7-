#include <stdlib.h>
#include <stdio.h>

int potencia(int base, int expoente) {
    int resultado = 1;
    for (int i = 0; i < expoente; i++) {
        resultado *= base;
    }
    return resultado;
}

int binario_para_decimal(int binario[], int n) {
    int decimal = 0;
    for (int i = 0; i < n; i++) {
        decimal += binario[i] * potencia(2, (n - (i + 1)));
    }
    return decimal;
}

void decimal_para_binario(int decimal) {
    int binario[32];
    int i = 0;

    if (decimal == 0) {
        printf("Binario: 0\n");
        return;
    }

    while (decimal > 0) {
        binario[i] = decimal % 2;
        decimal = decimal / 2;
        i++;
    }

    printf("Binario: ");
    while (i > 0) {
        i--;
        printf("%d", binario[i]);
    }
    printf("\n");
}

int main() {
    int opcao;
    printf("Escolha a conversao:\n");
    printf("1 - Binario para Decimal\n");
    printf("2 - Decimal para Binario\n");
    printf("Opcao: ");
    scanf("%d", &opcao);

    if (opcao == 1) {
        int n, entrada, i = 0;

        printf("Digite a quantidade de bits: ");
        scanf("%d", &n);

        if (n <= 0) {
            printf("Valor Invalido!\n");
            return 0;
        }

        int binario[n];

        while (i < n) {
            printf("Digite o %d algarismo binario mais significativo: ", i + 1);
            scanf("%d", &entrada);
            if (entrada != 0 && entrada != 1) {
                printf("Valor Invalido!\n");
                return 0;
            } else {
                binario[i] = entrada;
                i++;
            }
        }

        printf("Valor binario: ");
        for (i = 0; i < n; i++) {
            printf("%d", binario[i]);
        }

        int decimal = binario_para_decimal(binario, n);
        printf("\nValor decimal: %d\n", decimal);

    } else if (opcao == 2) {
        int decimal;
        printf("Digite um numero decimal: ");
        scanf("%d", &decimal);

        if (decimal < 0) {
            printf("Valor Invalido!\n");
            return 0;
        }

        decimal_para_binario(decimal);

    } else {
        printf("Opcao Invalida!\n");
    }

    return 0;
}
