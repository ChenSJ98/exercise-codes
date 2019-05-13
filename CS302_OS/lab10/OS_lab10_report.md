# <center> SUSTech CS302 OS Lab10 Report<center>

## Experiments:
1. Fundamentals:
   * According to the access mode, I/O devices can be classified as (1) **Sequential** (2) **Random** (3) **Interrupt**.
   * I/O control methods can be classified as (1) **I/O Interrupt** (2) **Polling**
   * Each physical record on the disk has a unique address that consists of three parts: (1) **Head identifier**(2) **Track identifier** (3) **Sector identifier**
   * Data READ/WRITE time = (1) **Seek time** + (2) **Rotation delay** + (3)  **Transfer time**
   * The metric for measuring I/Operformance are (1) **Latency**, (2)  **Throughput**
   * What are the work steps of the DMA controller? Please answer it and briefly describe the process of each step.
2. Application
   * If the C-SCAN algorithm is used to read the six sectors,
     * Write the track access sequence
     * How much time is required in total? The calculation process is required.
   * If using SSD, which scheduling algorithm do you think should be used? Explain why.
3. Programming
   |Algorithm/Test|1.in|2.in|3.in|
   |:-:|:-:|:-:|:-:|
   |FCFS|676|22173758|215124803|
   |SSTF|554|102429|95951|
   |SCAN|850|93760|95987|
   |C-SCAN|542|65445|65529|
   |LOOK|508|93744|95951|
   |C-LOOK|367|65301|65505|