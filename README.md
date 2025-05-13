# Potential Indirect Vulnerability Index (PIVI)

This repository contains Python scripts used for the calculation of the potential indirect vulnerability index (PIVI), as part of our research project.

There are three scripts, which should be run sequentially, as the output of each step is used in the next.

Step 1: Extract USA Trade Data

We use the data of bilateral commodity trade flows from the United Nations Comtrade database (http://comtrade.un.org) and extract the import/export values of the US with partner countries. 


Step 2: FDI Couple Strength

We compute the FDI couple strength (inflow + outflow) using bilateral FDI flow data published annually by the United Nations.


Step 3: Calculate the Potential Indirect Vulnerability Index

Using the processed platinum and iridium trade and FDI data, we calculate the PIVI values arising through interdependent global networks of trade and investment.


# Reference

For more details, please refer to the published article:

Pourshahabi S, Shutters ST, Muneepeerakul R (2024) Quantifying economic vulnerabilities induced by interdependent networks. PLoS ONE 19(7): e0306893. https://doi.org/10.1371/journal.pone.0306893

# Contact

If you have any questions, feel free to contact: sh.p.shahabi@gmail.com
