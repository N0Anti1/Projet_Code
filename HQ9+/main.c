#include <stdio.h>
#include <stdlib.h>
#pragma warning(disable : 4996)


void function_H() {
	printf("Hello World");
}
void function_Q(char* name) {

	FILE* file = fopen(name, "r");
	char* line = malloc(30 * sizeof(char));
	while (fscanf(file, "%s\n", line) == 1) {
		printf("%s\n", line);
	}
	free(line);
}
void function_9() {
	printf("99 bottles of beer on the wall, 99 bottles of beer.\n");
	for (int i = 98; i > 1; i--) {
		printf("Take one down and pass it around, %d bottles of beer on the wall.\n", i);
		printf("%d bottles of beer on the wall, %d bottles of beer.\n", i, i);
	}
	printf("1 bottle of beer on the wall, 1 bottle of beer.\n");
	printf("Take one down and pass it around, no more bottles of beer on the wall.\n");
	printf("No more bottles of beer on the wall, no more bottles of beer.\n");
	printf("Go to the store and buy some more, 99 bottles of beer on the wall.");
}


int main() {

	FILE* file = fopen("code.txt", "r");
	char* line = malloc(30*sizeof(char));
	int pile = 0;
	while (fscanf(file, "%s\n", line) == 1) {
		char c = line[0];
		int i = 0;
		while (c != '\0' && c != 0) {
			c = line[i];
			i++;
			if (c == 'H' || c == 'h') {
				function_H();
			}
			else if (c == 'Q' || c == 'q')
			{
				function_Q("code.txt");
			}
			else if (c == '+')
			{
				pile++;
			}
			else if (c == '9') {
				function_9();
			}
		}
		printf("\n");
	}

	free(line);

	return EXIT_SUCCESS;
}
