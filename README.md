## Russian Authors on the Internet

Data and scripts for the PhD thesis "Web texten. Text leben. Leben Weben. (Auto-)Biographische Praktiken im literarischen Runet" by Gernot Howanitz, University of Passau 2017. Uses Python 2.7 and Jupyter notebooks for visualisation.

## Installation

1. Download and install Anaconda, a Python release for data scientists, make sure you got the Python 2.7 version (not Python 3.6!): https://www.continuum.io/downloads 

2. Install additional Python packages using conda:
  a. Start the program "Anaconda prompt"
  b. Enter the following line and press "Enter": conda install qgrid gensim
  c. Enter the following line and press "Enter": jupyter nbextension enable --py widgetsnbextension
  d. If any of this fails, you might need to run the Anaconda prompt as administrator

## Usage

After the setup procedure, copy all data from the DVD to your home folder. Open "Anaconda prompt", enter the following line and press "Enter:

jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10

A browser window will open. Browse to the folder with the copied DVD content and click on "corpus.ipynb" for browsing the corpus or "create_lda.ipynb" for creating a new topic model of the corpus.