## Plan to Convert Jupyter Notebook to Python Script

1.  **Read Notebook Content:** Read the content of the `online_banking.ipynb` file. (This has already been done)
2.  **Create Python Script:** Create a new file named `online_banking.py` in the current directory.
3.  **Iterate Through Cells:** Iterate through each cell in the notebook.
4.  **Code Cells:** Extract the code from code cells and append it to the `online_banking.py` file.
5.  **Markdown Cells:** Convert the content of markdown cells into Python comments and append them to the `online_banking.py` file.
6.  **Handle Interactive Input:** Since the user wants to keep the interactive parts, leave the input code as is.
7.  **Finalize Script:**
    *   Add a shebang line (`#!/usr/bin/env python3`) at the beginning of the script to make it executable.
    *   Ensure that the `private/import/import.csv` file exists, as the script reads data from it.
8.  **Save Script:** Save the `online_banking.py` file.

```mermaid
graph LR
    A[Read 'online_banking.ipynb' content] --> B(Create 'online_banking.py');
    B --> C{Iterate through notebook cells};
    C -- Code cell --> D[Extract code];
    C -- Markdown cell --> E[Convert to comment];
    D --> F(Append to 'online_banking.py');
    E --> F;
    F --> G{Handle interactive input};
    G -- Keep input --> H[Leave input code as is];
    H --> I(Finalize 'online_banking.py');
    G -- Remove input --> J[Remove input code];
    J --> I;
    I --> K[Add shebang line (#!/usr/bin/env python3)];
    K --> L[Ensure 'private/import/import.csv' exists];
    L --> M[Save 'online_banking.py'];