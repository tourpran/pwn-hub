#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct node{
	int id;
	char buffer[32];
	struct node* next;
	struct node* prev;
};

int bad(){
	printf("Nope\n");
	exit(0);
}

void (*function_pointer)()= &bad;
char array[50]={0};
struct node *head=NULL;

int insert(int id){
	struct node *temp = malloc(sizeof(struct node));
	temp->next = NULL;
	temp->id = id;
	if(head==NULL){
		head = temp;
		head->prev = NULL;
		return 1;
	}
	struct node *iter = head;
	while(iter->next != NULL){
		iter = iter->next;
	}
	iter->next = temp;
	temp->prev = iter;
	return 1;
}

int get_name(int id){
	struct node *temp = head;
	while(temp->id != id && temp->next != NULL)
		temp = temp->next;
	if(temp==NULL)
		return 0;
	fgets(temp->buffer,0x100,stdin);
	return 0;
}

int delete(int id){
	struct node *temp = head;
	while(temp->id != id && temp->next != NULL)
		temp = temp->next;
	if(temp==NULL)
		return 0;
	if(temp->next == NULL)
		temp->prev->next = NULL;
	if(temp->prev == NULL)
		temp->next->prev = NULL;
	if(temp->next != NULL && temp->prev != NULL){
		temp->prev->next = temp->next;
		temp->next->prev = temp->prev;
	}
	free(temp);
	return 0;
}

int main(){
	int i=0;
	fgets(array,50,stdin);
	for(i=0;i<3;i++)
		insert(i);
	get_name(0);
	get_name(2);
	get_name(1);
	delete(1);
	printf("%d\n",sizeof(struct node));
	(*function_pointer)();
	printf("%d\n",sizeof(struct node));
	return 0;
}
