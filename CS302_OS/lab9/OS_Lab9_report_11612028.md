# <center> SUSTech CS302 OS Lan9 Report </center>

Title: Page-replacement Algorithm

Name: Shijie Chen, Student ID: 11612028

Experimental Environment: Linux and C++11
## Experiments
1. Algorithms
   * FIFO algorithm and its complexity
   * MIN algorithm and its complexity
   * LRU algorithm and its complexity
   * Clock algorithm and its complexity
   * Second-Chance algorithm and its complexity
2. Fundamenal
   * In theory, the optimal page-replacement algorithm is **MIN**, and prove it:
   * Can the FIFO page-replacement algorithm be improved? If yes, please provide a plan; If no, please give your proof.
   * Can the LRU page-replacement algorithm be improved? If yes, please provide a plan; If no, please give your proof.
3. Problems and Solutions
   
4. Program running result: (hit percentage)
   |Algorithm/ test|1.in|2.in|3.in|
   |:-:|:-:|:-:|:-:|
   |FIFO|11.98%|11.85%|82.36%|
   |MIN|42.40%|43.27%|88.58%|
   |LRU|11.76%|11.85%|82.39%|
   |Clock|11.77%|11.83%|82.38%|
   |Second-chance|11.85%|11.85%|82.39%|