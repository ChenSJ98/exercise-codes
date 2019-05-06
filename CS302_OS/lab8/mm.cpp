//#include<bits/stdc++.h>
#include<unistd.h>
#include<iostream>
#include <stdio.h>
using namespace std;

#define PROCESS_NAME_LEN 32 //进程名最大长度
#define MIN_SLICE 10 //内碎片最大大小
#define DEFAULT_MEM_SIZE 1024  //总内存大小
#define DEFAULT_MEM_START 0  //内存开始分配时的起始地址

typedef pair<int, string> My_algo;

int mem_size = DEFAULT_MEM_SIZE;
bool flag = 0; //当内存以及被分配了之后，不允许更改总内存大小的flag
static int pid = 1;
My_algo algo[123];

static int algorithm = 1; // use first fit by default
static int num_algo = 2; // number of algorithms 1: First Fit 	2: Best Fit

struct free_block{	//空闲数据块
	int size;
	int start_addr;
	struct free_block *next;
};

struct allocated_block{ //已分配的数据块
	int pid;
	int size;
	int start_addr;
	char process_name[PROCESS_NAME_LEN];
	int *data;
	struct allocated_block *next;
};

free_block *free_block_head; //空闲数据块首指针
allocated_block *allocated_block_head = NULL; //分配块首指针

allocated_block *find_process(int id); //寻找pid为id的分配块
free_block *init_free_block(int mem_size); //空闲块初始化
void display_menu(); //显示选项菜单
void set_mem_size(); //设置内存大小
int allocate_mem(allocated_block *ab); //为制定块分配内存
void rearrange(); // 对块进行重新分配
int create_new_process(); //创建新的进程
int free_mem(allocated_block *ab); //释放分配块
void swap(int *p, int *q); //交换地址
int dispose(allocated_block *ab); //释放分配块结构体
void display_mem_usage(); //显示内存情况
void kill_process(); //杀死对应进程并释放其空间与结构体
void Usemy_algo(int id); //使用对应的分配算法
void set_algorithm(); 

//主函数
int main(){
	int op;
	pid = 1;
	free_block_head = init_free_block(mem_size); //初始化一个可以使用的内存块，类似与操作系统可用的总存储空间
	for(;;){
		sleep(1);
		display_menu();
		fflush(stdin);
		scanf("%d", &op);
		switch (op){
			case 1:{ set_mem_size(); break; }
			case 2:{ set_algorithm(); break; }
			case 3:{ create_new_process(); break; }
			case 4:{ kill_process(); break; }
			case 5:{ display_mem_usage(); break; }
			case 233:{ puts("bye...."); sleep(1); return 0; }
			defaut: break;
		}
	}
}

void set_algorithm() {
	printf("Please choose an algorithm:");
	printf("1) First Fit");
	printf("2) Best Fit");	
	int t;
	scanf("%d", &t);
	if(t < 0 || t > num_algo) {
		printf("No such algorithm!");
		return;
	}
	algorithm = t;
}
/**
 * TODO
 * return pointer to the corresponding allocated_block struct
 * return NULL on failure
 */
allocated_block *find_process(int id){ //循环遍历分配块链表，寻找pid=id的进程所对应的块
	allocated_block *p = allocated_block_head;
	while(p != NULL) {
		if(p->pid == id) {
			return p;
		}
		p = p->next;
	}
	return p;
}

free_block *init_free_block(int mem_size){ //初始化空闲块，这里的mem_size表示允许的最大虚拟内存大小
	free_block *p;
	p = (free_block *)malloc(sizeof(free_block));
	if (p == NULL){
		puts("No memory left");
		return NULL;
	}
	p->size = mem_size;
	p->start_addr = DEFAULT_MEM_START;
	p->next = NULL;
	return p;
}

void display_menu(){
	puts("\n\n******************menu*******************");
	printf("1) Set memory size (default = %d)\n", DEFAULT_MEM_SIZE);
	printf("2) Set memory allocation algorithm\n");
	printf("3) Create a new process\n");
	printf("4) Kill a process\n");
	printf("5) Display memory usage\n");
	printf("233) Exit\n");
}
// TODO
void set_mem_size(){ //更改最大内存大小
	int t;
	scanf("%d", &t);
	if(t > 0) {
		mem_size = t;
	}
	free(free_block_head);
	free_block_head = init_free_block(mem_size);
}

free_block *get_free_block(allocated_block *ab) {
	free_block *p = (free_block*)malloc(sizeof(free_block));
	p->next = free_block_head;
	if(algorithm == 1) {
		// first fit
		while(p->next != NULL) {
			if(p->next->size >= ab->size) {
				return p;
			}
			p = p->next;
		}
		return NULL;
	} else if(algorithm == 2) {
		// best fit
		free_block *t = NULL;
		int gap = mem_size;
		while(p->next != NULL) {
			if(p->next->size >= ab->size) {
				if(gap > p->next->size - ab->size) {
					gap = p->next->size - ab->size;
					t = p;
				}
			}
			p = p->next;
		}
		return t;
	}
	return NULL;
}

// TODO
/**
 * add *ab to allocated
 * decrease free space
 * return -1 on failure
 */
int allocate_mem(allocated_block *ab){ //为块分配内存，真正的操作系统会在这里进行置换等操作
	free_block *p = get_free_block(ab);
	if(p != NULL) {
		ab->start_addr = p->next->start_addr;
		if(p->next->size == ab->size) {
			// delete free block
			free_block *t = p->next;
			if(p->next == free_block_head) {
				free_block_head = p->next->next;
			}
			p->next = t->next;
			free(t);
			t = NULL;
		} else {
			// shrink free block
			p->next->start_addr += ab->size;
			p->next->size -= ab->size;
		}
		allocated_block *t = allocated_block_head;
		ab->next = t;
		allocated_block_head = ab;
		if(p->next == free_block_head)
			free(p);
		return 1;
	}
	return 0;
}
// TODO
/**
 * new allocated struct
 * allocate memory for the struct
 * return -1 on failure
 */
int create_new_process(){ //创建新进程
	allocated_block *blk = (allocated_block*)malloc(sizeof(allocated_block));
	int t;
	scanf("%d", &t);
	if(t < 0) {
		printf(" ERROR!!! A positive integer is expected!");
		return 0;
	}
	if(t > mem_size) {
		printf("ERROR!!! Exceeds max memory of the system!");
		return 0;
	}
	blk->size = t;
	blk->next = NULL;
	blk->data = NULL;

	if(!allocate_mem(blk)) {
		printf("ERROR!!! Insufficient free memory!");
		free(blk);
		return 0;
	}
	blk->pid = pid++;
	return 1;
}

void swap(int *p, int *q){
	int tmp = *p;
	*p = *q;
	*q = tmp;
	return;
}

void rearrange(){ //将块按照地址大小进行排序
	free_block *tmp, *tmpx;
	puts("Rearrange begins...");
	puts("Rearrange by address...");
	tmp = free_block_head;
	while(tmp != NULL){
		tmpx = tmp->next;
		while (tmpx != NULL){
			if (tmpx->start_addr < tmp->start_addr){
				swap(&tmp->start_addr, &tmpx->start_addr);
				swap(&tmp->size, &tmpx->size);
			}
			tmpx = tmpx->next;
		}
		tmp = tmp->next;
	}
	usleep(500);
	puts("Rearrange Done.");
}

// TODO
/**
 * alter liked list
 * delete from allocated
 * find & merge with prior free block
 */ 
int free_mem(allocated_block *ab){ //释放某一块的内存 
	// see if the free_block_head should be changed
	if(free_block_head == NULL || free_block_head->start_addr > ab->start_addr) {
		if(free_block_head && free_block_head->start_addr == ab->start_addr + ab->size) {
			// extend free_block_head
			free_block_head->start_addr = ab->start_addr;
			free_block_head->size += ab->size;
		} else {
			// new free_block_head
			free_block *head = (free_block*)malloc(sizeof(free_block));
			head->start_addr = ab->start_addr;
			head->size = ab->size;
			head->next = free_block_head;
			free_block_head = head;
		}
	} else {
		free_block *p = (free_block*)malloc(sizeof(free_block));
		p->next = free_block_head;
		
		while(p->next != NULL) {
			if(p->next->start_addr < ab->start_addr && (p->next->next == NULL || p->next->next->start_addr > ab->start_addr)) { // found
				if(p->next->next == NULL) {
					p->next->size += ab->size;
				} else {
					if(p->next->start_addr + p->next->size == ab->start_addr) {
						// 1. free space merge with left
						p->next->size += ab->size;
					} else {
						// 2. new free space and insert
						free_block *new_block = (free_block*)malloc(sizeof(free_block));
						new_block->start_addr = ab->start_addr;
						new_block->size = ab->size;
						new_block->next = p->next->next;
						p->next->next = new_block;
						p = p->next;
					}
					if(NULL != p->next->next && p->next->start_addr + p->next->size == p->next->next->start_addr) { 
						// 3. (after 1 or 2) merge with right
						p->next->size += p->next->next->size;
						free_block *t = p->next->next;
						p->next->next = t->next;
						free(t);
						t = NULL;
					}
					
				}
				break;
			}
			p = p->next;
		}
	}
	return 1;
}


int dispose(allocated_block *fab){ //释放结构体所占的内存
	allocated_block *pre, *ab;
	if (fab == allocated_block_head){
		allocated_block_head = allocated_block_head->next;
		free(fab);
		return 1;
	}
	pre = allocated_block_head;
	ab = allocated_block_head->next;
	while (ab != fab){ pre = ab; ab = ab->next;}
	pre->next = ab->next;
	free(ab);
	return 2;
}

void display_mem_usage(){
	free_block *fb = free_block_head;
	allocated_block *ab = allocated_block_head;
	puts("*********************Free Memory*********************");
	printf("%20s %20s\n", "start_addr", "size");
	int cnt = 0;
	while (fb != NULL){
		cnt++;
		printf("%20d %20d\n", fb->start_addr, fb->size);
		fb = fb->next;
	}
	if (!cnt) puts("No Free Memory");
	else printf("Totaly %d free blocks\n", cnt);
	puts("");
	puts("*******************Used Memory*********************");
	printf("%10s %20s %10s %20s\n", "PID", "ProcessName", "start_addr", "size");
	cnt = 0;
	while (ab != NULL){
		cnt++;
		printf("%10d %20s %10d %20d\n", ab->pid, ab->process_name, ab->start_addr, ab->size);
		ab = ab->next;
	}
	if (!cnt) puts("No allocated block");
	else printf("Totaly %d allocated blocks\n", cnt);
	return;
}

void kill_process(){ //杀死某个进程
	allocated_block *ab;
	int pid;
	puts("Please input the pid of Killed process");
	scanf("%d", &pid);
	ab = find_process(pid);
	if (ab != NULL){
		free_mem(ab);
		dispose(ab);
	} else {
		printf("ERROR!!! Process is not found!");
	}
}



