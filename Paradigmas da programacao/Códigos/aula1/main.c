#include <stdio.h>

void main()
{
	int linhas, colunas;
	printf("Digite o numero de Linhas: ");
	scanf("%d", &linhas);
	printf("Digite o numero de Colunas: ");
	scanf("%d", &colunas);

	int matriz[linhas][colunas];
	printf("Digite a Matriz:\n");
	for (int i = 0; i < linhas; i++){
		printf("Linha %d \n", i + 1);
		for (int j = 0; j < colunas; j++){
			scanf("%d", &matriz[i][j]);
		}
	}
	printf("\n");
	printf("Matriz: \n");
	for (int i = 0; i < linhas; i++){
		for (int j = 0; j < colunas; j++)
		{
			printf("[%d]", matriz[i][j]);
		}
		printf("\n");
	}
}