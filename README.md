# Potential Indirect Vulnerability Index (PIVI)

This repository contains Python scripts used for the calculation of the potential indirect vulnerability index (PIVI), as part of our research project. There are three scripts, which should be run sequentially, as the output of each step is used in the next.

Step 1_Extract_USA_Trade_Data: We use the data of bilateral commodity trade flows from the United Nations Comtrade database (http://comtrade.un.org). We extract the import/export values of the US with partner countries using this script. 


Step 2_FDI_Couple_Strength: We compute the FDI couple strength as the sum of inflow and outflow of FDI between the investing and intermediary countries using bilateral FDI flow data published annually by the United Nations (https://unctad.org/).


Step 3_USA_platinum_iridium_PIVI: Using the processed platinum and iridium trade and FDI data, we calculate the PIVI values arising through interdependent global networks of trade and investment.


# Reference

For more details, please refer to our published article:

Pourshahabi S, Shutters ST, Muneepeerakul R (2024) Quantifying economic vulnerabilities induced by interdependent networks. PLoS ONE 19(7): e0306893. https://doi.org/10.1371/journal.pone.0306893

# Contact

If you have any questions, feel free to contact: sh.p.shahabi@gmail.com
