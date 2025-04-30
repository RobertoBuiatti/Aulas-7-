import java.util.Scanner;

public class ConversorNumerico {

    public static int potencia(int base, int expoente) {
        int resultado = 1;
        for (int i = 0; i < expoente; i++) {
            resultado *= base;
        }
        return resultado;
    }

    public static int binarioParaDecimal(int[] binario) {
        int decimal = 0;
        int n = binario.length;
        for (int i = 0; i < n; i++) {
            decimal += binario[i] * potencia(2, (n - (i + 1)));
        }
        return decimal;
    }

    public static void decimalParaBinario(int decimal) {
        if (decimal == 0) {
            System.out.println("Binario: 0");
            return;
        }

        StringBuilder binario = new StringBuilder();
        while (decimal > 0) {
            binario.insert(0, decimal % 2);
            decimal /= 2;
        }
        System.out.println("Binario: " + binario);
    }

    public static void decimalParaOctal(int decimal) {
        if (decimal == 0) {
            System.out.println("Octal: 0");
            return;
        }

        StringBuilder octal = new StringBuilder();
        while (decimal > 0) {
            octal.insert(0, decimal % 8);
            decimal /= 8;
        }
        System.out.println("Octal: " + octal);
    }

    public static int octalParaDecimal(int octal) {
        int decimal = 0;
        int base = 1;

        while (octal > 0) {
            int ultimoDigito = octal % 10;
            decimal += ultimoDigito * base;
            base *= 8;
            octal /= 10;
        }
        return decimal;
    }

    public static void decimalParaHexadecimal(int decimal) {
        if (decimal == 0) {
            System.out.println("Hexadecimal: 0");
            return;
        }

        StringBuilder hexadecimal = new StringBuilder();
        while (decimal > 0) {
            int resto = decimal % 16;
            if (resto < 10)
                hexadecimal.insert(0, (char)(resto + '0'));
            else
                hexadecimal.insert(0, (char)(resto - 10 + 'A'));
            decimal /= 16;
        }
        System.out.println("Hexadecimal: " + hexadecimal);
    }

    public static int hexadecimalParaDecimal(String hex) {
        int decimal = 0;
        int len = hex.length();

        for (int i = 0; i < len; i++) {
            char ch = hex.charAt(i);
            int valor;
            if (ch >= '0' && ch <= '9') {
                valor = ch - '0';
            } else if (ch >= 'A' && ch <= 'F') {
                valor = ch - 'A' + 10;
            } else if (ch >= 'a' && ch <= 'f') {
                valor = ch - 'a' + 10;
            } else {
                return -1;
            }
            decimal += valor * potencia(16, len - i - 1);
        }
        return decimal;
    }

    public static void binarioParaOctal(int[] binario) {
        int decimal = binarioParaDecimal(binario);
        decimalParaOctal(decimal);
    }

    public static void binarioParaHexadecimal(int[] binario) {
        int decimal = binarioParaDecimal(binario);
        decimalParaHexadecimal(decimal);
    }

    public static void octalParaBinario(int octal) {
        int decimal = octalParaDecimal(octal);
        System.out.println("Decimal intermediario: " + decimal);
        decimalParaBinario(decimal);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Escolha a conversao:");
        System.out.println("1 - Binario para Decimal");
        System.out.println("2 - Decimal para Binario");
        System.out.println("3 - Decimal para Octal");
        System.out.println("4 - Octal para Binario");
        System.out.println("5 - Decimal para Hexadecimal");
        System.out.println("6 - Hexadecimal para Decimal");
        System.out.println("7 - Binario para Octal");
        System.out.println("8 - Binario para Hexadecimal");
        System.out.println("9 - Octal para Decimal");
        System.out.print("Opcao: ");
        int opcao = sc.nextInt();

        switch (opcao) {
            case 1 -> {
                System.out.print("Digite a quantidade de bits: ");
                int n = sc.nextInt();
                if (n <= 0) {
                    System.out.println("Valor Invalido!");
                    return;
                }
                int[] binario = new int[n];
                for (int i = 0; i < n; i++) {
                    System.out.print("Digite o " + (i + 1) + " algarismo binario mais significativo: ");
                    int entrada = sc.nextInt();
                    if (entrada != 0 && entrada != 1) {
                        System.out.println("Valor Invalido!");
                        return;
                    }
                    binario[i] = entrada;
                }

                System.out.print("Valor binario: ");
                for (int bit : binario) {
                    System.out.print(bit);
                }

                int decimal = binarioParaDecimal(binario);
                System.out.println("\nValor decimal: " + decimal);
            }
            case 2 -> {
                System.out.print("Digite um numero decimal: ");
                int decimal = sc.nextInt();
                if (decimal < 0) {
                    System.out.println("Valor Invalido!");
                    return;
                }
                decimalParaBinario(decimal);
            }
            case 3 -> {
                System.out.print("Digite o numero decimal: ");
                int decimal = sc.nextInt();
                decimalParaOctal(decimal);
            }
            case 4 -> {
                System.out.print("Digite o numero octal: ");
                int octal = sc.nextInt();
                octalParaBinario(octal);
            }
            case 5 -> {
                System.out.print("Digite o numero decimal: ");
                int decimal = sc.nextInt();
                decimalParaHexadecimal(decimal);
            }
            case 6 -> {
                System.out.print("Digite o numero hexadecimal: ");
                String hex = sc.next();
                int decimal = hexadecimalParaDecimal(hex);
                if (decimal == -1)
                    System.out.println("Valor hexadecimal invalido!");
                else
                    System.out.println("Valor decimal: " + decimal);
            }
            case 7 -> {
                System.out.print("Digite a quantidade de bits: ");
                int n = sc.nextInt();
                if (n <= 0) {
                    System.out.println("Valor Invalido!");
                    return;
                }
                int[] binario = new int[n];
                for (int i = 0; i < n; i++) {
                    System.out.print("Digite o " + (i + 1) + " algarismo binario mais significativo: ");
                    int entrada = sc.nextInt();
                    if (entrada != 0 && entrada != 1) {
                        System.out.println("Valor Invalido!");
                        return;
                    }
                    binario[i] = entrada;
                }
                binarioParaOctal(binario);
            }
            case 8 -> {
                System.out.print("Digite a quantidade de bits: ");
                int n = sc.nextInt();
                if (n <= 0) {
                    System.out.println("Valor Invalido!");
                    return;
                }
                int[] binario = new int[n];
                for (int i = 0; i < n; i++) {
                    System.out.print("Digite o " + (i + 1) + " algarismo binario mais significativo: ");
                    int entrada = sc.nextInt();
                    if (entrada != 0 && entrada != 1) {
                        System.out.println("Valor Invalido!");
                        return;
                    }
                    binario[i] = entrada;
                }
                binarioParaHexadecimal(binario);
            }
            case 9 -> {
                System.out.print("Digite o numero octal: ");
                int octal = sc.nextInt();
                int decimal = octalParaDecimal(octal);
                System.out.println("Valor decimal: " + decimal);
            }
            default -> System.out.println("Opcao Invalida!");
        }

        sc.close();
    }
}
