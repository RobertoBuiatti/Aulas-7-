#include <stdio.h>
#include <math.h>

void converte(int quoc){
    int i, rest, bi = 8;
	int bin[bi];

	for(i=0; i<bi; i++){
		rest = quoc%2;
		printf("Quociente: %d, Resto: %d\n", quoc,rest);
		bin[i] = rest;
		quoc = floor(quoc/2);
	}
	printf("O valor binario corresponde a: ");
	for(i=bi-1; i>=0; i--){
		printf("%d ", bin[i]);
	}	
	printf(" ");

}

void main(){
	int v1,v2,v3,v4;
	
	printf("Digite v1: ");
	scanf("%d", &v1);
	
	printf("Digite v2: ");
	scanf("%d", &v2);
	
	printf("Digite v3: ");
	scanf("%d", &v3);
	
	printf("Digite v4: ");
	scanf("%d", &v4);
        
    converte(v1);
    converte(v2);
    converte(v3);
    converte(v4);

    printf("\n");
}

