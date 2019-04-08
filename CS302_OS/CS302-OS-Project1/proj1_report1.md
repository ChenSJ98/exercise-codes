# CS302 OS Project 1 - Threads Design Report
<center> Shijie Chen 11612028</center>

## Task 1: Efficient Alarm Clock

### Data structures and functions
* Data structures:

    * `thread` structure in thread.c.
      ```C
      #typedef __int64_t int64_t;
      struct thread
      {
          tid_t tid;
          enum thread_status status;
          char name [16];
          uint8_t *stack;
          int priority;
          int64_t ticksblk;
          struct list_elem allelem;
          struct list_elem elem;

          #ifdef USERPROG
            uint32_t *pagedir;
          #endif

          unsigned magic
      };
      ```
    Add `int64_t ticksblk` to facilitate thread sleep scheduling.

* Functions:
  * `void timer_sleep (int64_t ticks)` in timer.c
  Set `ticksblk`.
  * `tid_t thread_create (const char *name, int priority, thread_func *, void*)` in thread.c
  Initialize `ticksblk`.
  * `static intr_handler_func timer_interrupt` in timer.c
  Check and update `ticksblk` of each thread in each tick.

### Algorithms

The efficient alarm clock is implemented by blocking the thread instead of keep yielding the CPU.

This is achived by adding an attribute `ticksblk` to the `thread` structure. `ticksblk` is initiated to 0 on the creation of a process and set to `ticks` when `timer_spleep` is called. Threads with positive `ticksblk` are blocked by the scheduler. In each `timer_interrupt`, `ticksblk` decreases by 1. When `ticksblk` is 0 the blocked thread is unblocked and added to the ready list. The scheduler then decides the next thread to run.

### Synchronization

The logic of the efficient alarm clock takes effect in a interrupt handler `timer_interrupt ()` that executes every tick. Synchronization issues should be prevented by disabling interrupt in `timer_interrupt`.

### Rationale

The efficient alarm clock implement thread sleeping by blocking rather than yielding the CPU. The blocked thread is absent in the ready list and thus invisible to the scheduler until the `ticksblk` becomes 0 over time.

The added cost is on the checking and updating `ticksblk` in `timer_interrupt ()` which has $O(N)$ complexity with $N$ threads in total.

A more efficient design is maintaining a list of sleeping threads and only deal with the list in `timer_interrupt`. However, the performance gain might be quite small considering the limited number of threads in total.

In addition, as we will discuss later, the scan of all threads can be used to update priority for every thread. So the cost of implementing efficient alarm clock is totally acceptable.


## Task 2: Priority Scheduler
### Data structures and functions
* Data Structures

    * `thread` structure in thread.c.
      ```C
      #typedef __int64_t int64_t;
      struct thread
      {
          tid_t tid;
          enum thread_status status;
          char name [16];
          uint8_t *stack;
          int priority;
          int64_t ticksblk;
          struct list_elem allelem;
          struct list_elem elem;

          struct list_elem alllocks;
          struct *waiton;
          int priority0;

          #ifdef USERPROG
            uint32_t *pagedir;
          #endif

          unsigned magic
      };
      ```
      Add `alllocks` (contains the locks a thread owns), `waiton` (points to the thread that the thread is waiting for) and `priority0` (the original priority without donation).

    * `lock` structure in synch.h
      ```C
      struct lock
      {
      struct thread *holder;
      struct semaphore semaphore;
      struct list_elem waitintlist;
      }
      ```
      Add `waitinglist`, which is a **priority queue** that holds all the threads waiting for the lock.

* Functions

    * `thread_init()`
    Changed to initialize add attributes.
    * `thread_unblock()`, `thread_yield()` and `thread_init()`
    Change `push_back()` to `insert_ordered()` to make sure that the ready list is a priority queue.
    * `lock_comp_prio()`, `cond_sema_comp_prio()`
    Created to facilitate sorting on locks and conditional semaphores. Further used in priority scheduling.
    * `set_priority()`
    Call `thread_yield()` if the created thread has a higher priority than the current thread.
    * `lock_acquire()` and `lock_release()`
    Changed to support priority donation and restoration.
    * `cond_signal()`, `cond_wait()`, `sema_up()` and `sema_down()`
    Changed to make sure that the waiting list for conditional variables and semaphores are priority queues.

### Algorithms
The scheduling in Pintos revolves around the **ready_list** which contains threads in READY state. The main goal is to make the ready_list a priority queue by add rules to insertion into the list. Similar idea is applied to priority scheduling of locks, condition variables and semaphores.

* Priority scheduling of threads
Thread scheduling is done by the `schedule()` function in thread.c in which the next thread to run is fetched by `next_thread_to_run()`. By default, `next_thread_to_run()` returns the first element in the ready_list or _idle_ when the read_list is empty.

  There are two cases that require immediate rescheduling. One is when a thread is created and has a higher priority than any other thread. Another one is when a thread's priority is updated to the highest value by `thread_set_priority()`. `thread_yield()` is called in both cases to ensure the right schedule order.

  We can implement priority scheduling by making the read_list a priority queue based on the priority value of threads. This can be done by replacing the push_back operation with insert_ordered whenever a thread is added to the queue.

* Acquiring a lock
There are two possible outcomes when a thread tries to acquire a lock. The thread may successfully acquire the lock. Alternatively, the threads fails to acquire the lock. In this case, priority donation happens when a thread with a higher priority tries to acquire a lock owned by a thread with lower priority.

  The details of priority donation are described below:
  1. Priority donation happens. The priority of the owner is set to the max priority between its effective priority and the priority of the acquirer. The acquirer is blocked and added to the waiting list (which is a priority queue) of the lock.
  2. If priority donation happens, the owner of the lock will try to donate the priority to the thread it's waiting on (if any). This process runs recursively to make sure the origin thread of waiting has the highest priority.
  3. `schedule()` is called at the end of `lock_acquire()` to reschedule according to the updated priority.

* Releasing a lock
  Releasing a lock is relatively simpler.
  1. Restore the priority of the owner to the maximum of its base priority and the highest priority among the threads waiting for the locks it has.
  2. The lock is removed from its owner's `alllocks`. The owner of the lock is set to **null**.
  3. By default, `lock_release()` will unblock the thread with the highest priority in the waiting list.

* Computing effective priority
  Priority scheduling of threads is based on the _effective priority_ of threads. The effective priority is the maximum between the base priority of the thread and the highest priority among the threads waiting for the locks the thread owns. Effective priority is updated each time a priority donation happens or a lock is released.

* Priority scheduling for condition variables and semaphores
  Similar to the scheduling of locks, the scheduling of condition variables and semaphores makes use of priority queues. By maintaining the waiting list as a priority queue, the thread with highest priority in the waiting list will be awaked. The property of priority queue is maintained during the course of insertion, using `insert_ordered()`.
### Synchronization

A race condition may happen when the doner and the thread itself tries to modify the thread's priority at the same time. In my implementation, I disable interrupt to avoid this problem. 

### Rationale
The performance may suffer since the priority queue is inplemented as a linked list and it takes $O(N)$
to insert and $O(NlogN)$ to sort. A heap can be used to accelerate but the implementation can be difficult since the number of threads are non-deterministic.
## Task 3: Multi-level Feedback Queue Scheduler (MLFQS)
### Data structures and functions
* Data structure
  * `thread` structure in thread.c.
      ```C
      #typedef __int64_t int64_t;
      struct thread
      {
          tid_t tid;
          enum thread_status status;
          char name [16];
          uint8_t *stack;
          int priority;
          int64_t ticksblk;
          struct list_elem allelem;
          struct list_elem elem;

          struct list_elem alllocks;
          struct *waiton;
          int priority0;

          int nice;
          fixed_t recentcpu;

          #ifdef USERPROG
            uint32_t *pagedir;
          #endif

          unsigned magic
      };
      ```
      Add attribute `nice` and `recentcpu` for calculation.
* Functions
  * `timer_interrupt()`
  Changed to update `recentcpu`, `nice` and `priority` according to the rules.
  * `thread_init()`
  Changed to initialize added attributes.

### Algorithms
The advanced scheduling is based on the basic priority scheduling but with a different measure of priority. It maintains the ready_list as a priority list and `thread_yield()` is called when a newly created thread has the highest priority. A thread can't set it's priority in MLFQS.

  As is described in the design document, priority of a thread depends on `recentcpu` and `nice` and is calculated every 4 timer ticks (timer_ticks() % 4 == 0). `recentcpu` further depends on the Load Average. Both values are calculated every second (timer_ticks() % TIMER_FREQ == 0). These values and priority are updated in `timer_interrupt`.

  There is no priority donation in MLFQS. The threads are scheduled only by their priorities calculated in the way described above. The threads are put in a priority queue as in the priority scheduling. The thread with the highest priority will run.

### Synchronization
There should be little concern regarding synchronization in MLFQS. The priority of a thread is changed in only 2 situations:
1. When the thread is created, its priority is initialized.
2. A thread's priority is updated by the `timer_interrupt()` according to the algorithm.
In case 1, only 1 thread's priority is changed. A reschedule is then requested if it's priority is higher than all threads in the ready_list.
In case 2, every thread's priority is updated. However, the priority calculation of one thread doesn't require any external information from other elements in the list. Therefore, the ready_list is thread-safe.
### Rationale
The design document propose an implementation using 64 ready_lists, one for each priority value. However, I use only one ready_list to reduce complexity. Since the ready_list itself is a priority queue, the order of different priority values is automatically maintained.
## Additional Questions

* (This question uses the MLFQS scheduler.) Suppose threads A, B, C have nice values 0, 1 and 2. Each has a **recent_cpu** value of 0. Fill in the table below showing the scheduling decision and the **recent_cpu** and **priority** values for each thread after each given number of timer ticks. We can use **R(A)** and **P(A)** to denote the **recent_cpu** and **priority** values of thread A, for brevity.

  | timer ticks | R(A) | R(B) | R(C) | P(A) | P(B) | P(C) | thread to run |
  | :---------: | :--: | :--: | :--: | :--: | :--: | :--: | :-----------: |
  |      0      |  0   |  0   |  0   |  63  |  61  |  59  |       A       |
  |      4      |  4   |  0   |  0   |  62  |  61  |  59  |       A       |
  |      8      |  8   |  0   |  0   |  61  |  61  |  59  |       B       |
  |     12      |  8   |  4   |  0   |  61  |  60  |  59  |       A       |
  |     16      |  12  |  4   |  0   |  60  |  60  |  59  |       B       |
  |     20      |  12  |  8   |  0   |  60  |  59  |  59  |       A       |
  |     24      |  16  |  8   |  0   |  59  |  59  |  59  |       C       |
  |     28      |  16  |  8   |  4   |  59  |  59  |  58  |       B       |
  |     32      |  16  |  12  |  4   |  59  |  58  |  58  |       A       |
  |     36      |  20  |  12  |  4   |  58  |  58  |  58  |       C       |

    * **Did any ambiguities in the scheduler specification make values in the table (in previous question) uncertain? If so, what rule did you use to resolve them?**

      In some time ticks, there are threads with the same priority value which makes it hard to decide which thread to run. I used the round-robin rule to solve this problem.

* **How does Pintos start the first thread in its thread system?**
  Pintos starts the first thread by calling `thread_start (void)` in thread.c. The following things are done:
    1. Create and initialize a semaphore `idle_started`.
    2. Create the `idle` thread with lowest priority.
    3. Enable system

* **Consider priority scheduling, how does pintos keep running a ready thread with highest priority after its time tick reaching TIME_SLICE?**
  `timer_interrupt()` runs every tick and calls `thread_ticks()`. `thread_tick()` will call `intr_yield_on_return()` which sets `yield_on_return` to true. In this case, the interrupt handler `intr_handler()` will call `thread_yield()` and the thread is rescheduled to run again. Note that `intr_handler()` deals with all interrupts and is called by the assembly language interrupt stubs.

* **What will pintos do when switching from one thread to the other? By calling what functions and doing what?**
  In `schedule()`, `switch_threads()` and `thread_schedule_tail()` are called after we get the next thread to run.

  `switch_threads` is an assembly language routine defined in `switch.s`. It saves the register state of current thread. `thread_schedule_tail()` activates the next thread by marking it as _THREAD_RUNNING_ and starting a new time slice. If the previous thread is marked as _THREAD_DYING_, its struct thread is destroyed.

* **How does pintos implement floating point number operation**
  Pintos implements floating point number operation by pretending floating point numbers to be integers. Then apply shift operation to obtain its integer part and conform floating point numbers and integers in calculations.

* **What do priority-donation test cases(priority-donate-chain and priority-donate-nest) do and illustrate the running process**

  * **priority-donate-chain**
    Description: This test verifies the priority donation in a chain.
    Illustration:
  1. The test creates 7 threads with priority 3, 6, 9, 12, 15, 18, 21 and another 7 threads for print logs with priority of 1 less than the previous threads. It also creates 7 locks divided into 7 groups: (1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(null,6). This creates a chain of waiting. Each thread owns their first lock and waits for the second one.
  2. The later created threads keep donating priority until the last one (21). Then, the main loop exits and test program releases lock[0].
  3. When lock[0] is released, thread 1, 2, 3, 4, 5, 6, 7 got their second locks subsequently and are waked up to print logs.
  4. At last, the priority of the threads are restored to their initial value. The threads and corresponding _interloper_ threads run in the reverse order and print finishing log messages.

  * **priority-donate-nest**
    Description: This test verifies the priority donation with more than one locks.
    Illustration:
  1. Original_thread creates two locks (a and b) and acquires a.
  2. Original_thread creates thread _medium_ with priority PRI_DEFAULT+1. _medium_ acquires lock b, but is blocked while acquiring lock a.
  3. Original_thread keeps going with priority donated to PRI_DEFAULT+1. It creates a thread _high_ with priority PRI_DEFAULT+2. _high_ tries to acquire lock b and got blocked.
  4. Original_thread and _medium_ both have priority PRI_DEFAULT+2 donated by _high_. Original_thread releases lock a. Then, _medium_ preempts and releases lock b. At last, _high_ preemts and finish. After that, _medium_ and Original_thread finishes subsequently.
