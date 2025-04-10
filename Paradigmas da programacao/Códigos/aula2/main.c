#include <stdio.h>
#include <math.h>

int main(){
	int i, quoc, rest,bi;
	
	printf("Digite o numero decimal entre 0 e 255 para a conversao binaria: ");
	scanf("%d", &quoc);
	
	if(quoc < 0 || quoc > 255){
		printf("Animal coloca entre 0 e 255\n");
		return 1;
	}

	bi = ceil(log2(quoc)) + 1;
	
	int bin[bi];

	printf("bi: %d\n", bi);

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
	printf("\n");
	return 1;
}