#include <stdlib.h>
#include <stdio.h>
#include <string.h>

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

void decimal_para_octal(int decimal) {
    int octal[32];
    int i = 0;

    if (decimal == 0) {
        printf("Octal: 0\n");
        return;
    }

    while (decimal > 0) {
        octal[i] = decimal % 8;
        decimal = decimal / 8;
        i++;
    }

    printf("Octal: ");
    while (i > 0) {
        i--;
        printf("%d", octal[i]);
    }
    printf("\n");
}

int octal_para_decimal(int octal) {
    int decimal = 0;
    int base = 1;
    
    while (octal > 0) {
        int ultimo_digito = octal % 10;
        decimal += ultimo_digito * base;
        base *= 8;
        octal /= 10;
    }
    return decimal;
}

void decimal_para_hexadecimal(int decimal) {
    char hexadecimal[32];
    int i = 0;

    if (decimal == 0) {
        printf("Hexadecimal: 0\n");
        return;
    }

    while (decimal > 0) {
        int resto = decimal % 16;
        if (resto < 10)
            hexadecimal[i] = resto + '0';
        else
            hexadecimal[i] = resto + 'A' - 10;
        decimal = decimal / 16;
        i++;
    }

    printf("Hexadecimal: ");
    while (i > 0) {
        i--;
        printf("%c", hexadecimal[i]);
    }
    printf("\n");
}

int hexadecimal_para_decimal(char *hex) {
    int decimal = 0;
    int valor;
    int len = strlen(hex);
    
    for(int i = 0; hex[i] != '\0'; i++) {
        if(hex[i] >= '0' && hex[i] <= '9')
            valor = hex[i] - '0';
        else if(hex[i] >= 'A' && hex[i] <= 'F')
            valor = hex[i] - 'A' + 10;
        else if(hex[i] >= 'a' && hex[i] <= 'f')
            valor = hex[i] - 'a' + 10;
        else
            return -1;  
            
        decimal += valor * potencia(16, len - i - 1);
    }
    return decimal;
}

void binario_para_octal(int binario[], int n) {
    int decimal = binario_para_decimal(binario, n);
    decimal_para_octal(decimal);
}

void binario_para_hexadecimal(int binario[], int n) {
    int decimal = binario_para_decimal(binario, n);
    decimal_para_hexadecimal(decimal);
}

void octal_para_binario(int octal) {
    int decimal = octal_para_decimal(octal);
    printf("Decimal intermediario: %d\n", decimal);
    decimal_para_binario(decimal);
}

int main() {
    int opcao;
    printf("Escolha a conversao:\n");
    printf("1 - Binario para Decimal\n");
    printf("2 - Decimal para Binario\n");
    printf("3 - Decimal para Octal\n");
    printf("4 - Octal para Binario\n");
    printf("5 - Decimal para Hexadecimal\n");
    printf("6 - Hexadecimal para Decimal\n");
    printf("7 - Binario para Octal\n");
    printf("8 - Binario para Hexadecimal\n");
    printf("9 - Octal para Decimal\n");
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

    } else if (opcao == 3) {
        int decimal;
        printf("Digite o numero decimal: ");
        scanf("%d", &decimal);
        decimal_para_octal(decimal); 

    } else if (opcao == 4) {
        int octal;
        printf("Digite o numero octal: ");
        scanf("%d", &octal);
        octal_para_binario(octal);
        
    } else if (opcao == 5) {
        int decimal;
        printf("Digite o numero decimal: ");
        scanf("%d", &decimal);
        decimal_para_hexadecimal(decimal);
    } else if (opcao == 6) {
        char hex[32];
        printf("Digite o numero hexadecimal (em maiusculo): ");
        scanf("%s", hex);
        int decimal = hexadecimal_para_decimal(hex);
        if(decimal == -1)
            printf("Valor hexadecimal invalido!\n");
        else
            printf("Valor decimal: %d\n", decimal);
    } else if (opcao == 7) {
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
        
        binario_para_octal(binario, n);
    } else if (opcao == 8) {
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
        
        binario_para_hexadecimal(binario, n);
    } else if (opcao == 9) {
        int octal;
        printf("Digite o numero octal: ");
        scanf("%d", &octal);
        int decimal = octal_para_decimal(octal);
        printf("Valor decimal: %d\n", decimal);
    } else {        
        printf("Opcao Invalida!\n");
    }

    return 0;
}
