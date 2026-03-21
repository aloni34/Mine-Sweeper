
# **Minesweeper AI \& Simulation Sandbox**



## **1. Project Overview**



This project is an advanced implementation of the classic Minesweeper game, engineered as a **Dual-Mode System:**



**Interactive Gameplay:** A fully-featured GUI experience with custom controls and modern UI.



**Autonomous Research Sandbox:** A "Headless" simulation engine capable of processing millions of games to benchmark AI efficiency.



The project is built on a custom **MVC++ Architecture**, decoupling the logical engine from the graphical interface to allow for high-velocity data generation and statistical analysis.





## **2. Core Features**

**Deterministic Statistical Marker (DSM) AI:** A heuristic-driven solver that utilizes probability elimination to achieve high-density win rates.



**10M+ Batch Simulation:** Support for massive automated testing cycles with data persistence.



**Recursive Flood-Fill (DFS):** Optimized depth-first search for rapid board expansion.



**Deferred Mine Placement:** Guaranteed 100% safety on the first move by generating the board after the initial interaction.



**Excel Integration:** Automated export of game metrics (Win Rate, $PB$ density, move count) for post-run analysis.





## **3. Technical Architecture**

The system follows a modular design to ensure scalability and maintainability.



**Model** (mine\_sweeper.py): The logical "Source of Truth." Handles 2D grid calculations and mine proximity mapping.



**View** (view.py): The Tkinter-based presentation layer.



**Connector** (connector.py): The centralized hub managing event-driven communication between logic and UI.



**AI Engine** (brain.py): Contains specialized solving variants including DSM-SC (Start-Center) and DSM-SE (Start-Edge).



**Analytics** (test.py): Manages the simulation lifecycle and Excel data logging.





## **4. Installation \& Setup**



**Prerequisites**



Ensure you have Python 3.x installed along with the following dependencies:



**pandas numpy openpyxl**



**Execution**



**Launch GUI:** Run python main.py to play the game manually.



**Run Simulations:** Configure values.py (Set IS\_TO\_VIEW = False) and execute the test suite to begin headless data generation.





## **5. Statistical Insights (PB Analysis)**



Through the analysis of over 10 million iterations, this project identifies the **Critical Threshold** of Minesweeper solvability.





## **6. Configuration (values.py)**

Users can modify the environment via the **SettingValues** class:



**NUMBER\_OF\_TESTS:** Quantity of games per batch.



**STEP:** Incremental difficulty increase between batches.



**BOARD\_HEIGHT / WIDTH:** Customize the grid scale.



**IS\_TO\_SAVE:** Toggle automated Excel logging.



