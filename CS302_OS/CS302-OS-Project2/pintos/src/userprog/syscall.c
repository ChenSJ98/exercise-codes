#include "userprog/syscall.h"
#include <stdio.h>
#include <syscall-nr.h>
#include <devices/shutdown.h>
#include <threads/vaddr.h>
#include <filesys/file.h>
#include <filesys/filesys.h>
#include <string.h>
#include <devices/input.h>
#include <threads/palloc.h>
#include <threads/malloc.h>
#include "threads/interrupt.h"
#include "threads/thread.h"
#include "process.h"
#include "pagedir.h"

static void syscall_handler (struct intr_frame *);

void
syscall_init (void) 
{
  intr_register_int (0x30, 3, INTR_ON, syscall_handler, "syscall");
}

void bad_exit(void);
struct opened_file* search_file(int);
bool is_valid_address(void *);
int write(struct intr_frame *);
int open(const char *);
int filesize(int);
int create(const char *, int);
static void
syscall_handler (struct intr_frame *f UNUSED) 
{
  

  int *sp = f->esp;
  if(!is_valid_address(sp))
    bad_exit();
  int opt = *sp++;
  switch(opt) {
    case SYS_HALT:
      shutdown_power_off();
      break;
    case SYS_EXIT:
      thread_current()->exit_status = *sp;
      thread_exit ();
      break;
    case SYS_EXEC:
      if(!is_valid_address((void *)*sp))
      {
        bad_exit();
      }
        
      f->eax = process_execute((char*)*sp);
      break;
      break;
    case SYS_WAIT:
      if(!is_valid_address((void *)sp))
        bad_exit();
      f->eax = process_wait(*sp);
      break;
    case SYS_CREATE:
      if(!is_valid_address(sp) || !is_valid_address(sp + 1))
        bad_exit();
      f->eax = create((const char*)*sp, *(sp+1));
      break;
    case SYS_REMOVE:
      break;
    case SYS_OPEN:
      if(!is_valid_address((void *)sp))
        bad_exit();
      f->eax = open((const char*)*sp);
      break;
    case SYS_FILESIZE:
      if(!is_valid_address((void *)sp))
        bad_exit();
      f->eax = filesize(*sp);
      break;
    case SYS_READ:
      break;
    case SYS_WRITE:
      
      f->eax = write(f);
      break;
    case SYS_SEEK:
      break;
    case SYS_TELL:
      break;
    case SYS_CLOSE:
      break;
    
  }
  //thread_exit ();
}

void bad_exit()
{
  thread_current()->exit_status = -1;
  thread_exit();
}
bool is_valid_address(void* p)
{
  if(!p || !is_user_vaddr(p) || !is_user_vaddr(p + 4) || !is_user_vaddr(p+1) || (pagedir_get_page(thread_current()->pagedir, p) == NULL))
  {
    return false;
  }
  return true;
}

int write(struct intr_frame *f) 
{
  int fd;
  void* buffer;
  unsigned size;
  fd = *((int*)f->esp + 1);
  buffer = (void*) (*((int*)f->esp + 2));
  size = *((unsigned*)f->esp + 3);
  int code = 0;
  if(fd == 1)
  {
    putbuf(buffer, size);
    return size;
  }
  else
  {
    struct opened_file *opened_file_ = search_file(fd);
    if(opened_file_ != NULL)
    {
      acquire_file_lock();
      code = file_write(opened_file_->file, buffer, size);
      release_file_lock();
    }
  }
  return code;
}
/* Create a file. */
int create(const char* name, int size)
{
  
  acquire_file_lock();
  int code = filesys_create(name, size);
  release_file_lock();
  return code;
}
/* Open a file. Return the file descriptor. */
int open(const char *file_name)
{
  
  if(file_name == NULL)
    return -1;
  if(!is_valid_address((void*)file_name))
    bad_exit();
  acquire_file_lock();
  struct file* file_ = filesys_open(file_name);
  release_file_lock();
  if(file_ != NULL) {
    struct opened_file *new_file = palloc_get_page(0);
    new_file->fd = thread_current()->fd_next++;
    new_file->file = file_;
    list_push_back(&thread_current()->files, &new_file->file_elem);
    return new_file->fd;
  }
  else
  {
    return -1;
  }
}

int filesize(int fd)
{
  struct opened_file * opened_file_ = search_file(fd);
  if(opened_file_ != NULL)
  {
    return file_length(opened_file_->file);
  }
  else
  {
    return -1;
  }
  
}


struct opened_file* fild_file(int fd)
{
  struct list_elem *elem;
  struct opened_file *opened_file_;
  struct list files = thread_current()->files;
  for(elem = list_begin(&files); elem != list_back(&files); elem = list_next(elem))
  {
    opened_file_ = list_entry(elem, struct opened_file, file_elem);
    if(opened_file_->fd == fd)
    return opened_file_;
  }
  return NULL;
}