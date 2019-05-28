# <center> SUSTech CS302 OS Lab10 Report<center>
Title: Disk Scheduling Algorithm

Name: Shijie Chen

ID: 11612028

Experimental Environment: Linux

## Experiments:
1. Fundamentals:
   * According to unit data read mode, I/O devices can be classified as (1) **Sequential** (2) **Random** (3) **Interrupt**.
   * I/O control methods can be classified as (1) **I/O Interrupt** (2) **Polling**
   * Each physical record on the disk has a unique address that consists of three parts: (1) **Head identifier**(2) **Track identifier** (3) **Sector identifier**
   * Data READ/WRITE time = (1) **Seek time** + (2) **Rotation delay** + (3)  **Transfer time**
   * The metric for measuring I/Operformance are (1) **Latency**, (2)  **Throughput**
   * What are the work steps of the DMA controller? Please answer it and briefly describe the process of each step.

      1. Device driver is told to transfer disk data to buffer at address X.
      2. Device driver tells disk controller to transfer C bytes from disk to buffer at address X.
      3. Disk controller initiates DMA transfer.
      4. Disk controller sends each byte to DMA controller.
      5. DMA controller transfers bytes to buffer X, increasing memory address and decreasing C until C = 0.
      6. When C = 0, DMA interrupts CPU to signal transfer completion.

2. Application
   * **If the C-SCAN algorithm is used to read the six sectors,**
     * Write the track access sequence
    
        100 -> 120 -> 20 -> 30 -> 60 -> 70 -> 90
     * How much time is required in total? The calculation process is required.

         Time needed to read a sector is $60/12000/100*1000 = 0.05ms$. To read the sector, we may have to access 1, 2, ... 100 sectors. On average, it takes $0.05 * 50 = 2.5ms$. Total load time $T_{load} = 2.5 * 6 = 15ms$.

         Head movement time is $T_{move} = (199 - 100) + (90 - 0) = 189ms$

         Total time $T_{total} = T_{load} + T_{move} = 15 + 189 = 214ms$.
   * **If using SSD, which scheduling algorithm do you think should be used? Explain why.**
      FCFS should be used. 
      
      Reason: SSDs don't have seek time and rotational delay. FCFS provides as good performance as other algorithms.
3. Programming
  
   Read the OS_lab10_DiskScheduling_guide_en.docx, finish Five Disk Schedule Algorithms (SSTF, SCAN, C-SCAN, LOOK, and C-LOOK) and fill the following table.


|Algorithm/Test|1.in|2.in|3.in|
|:-:|:-:|:-:|:-:|
|FCFS|676|22173758|215124803|
|SSTF|554|102429|95951|
|SCAN|850|93760|95987|
|C-SCAN|542|65445|65529|
|LOOK|508|93744|95951|
|C-LOOK|367|65301|65505|