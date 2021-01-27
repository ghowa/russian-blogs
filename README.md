## Russian Authors on the Internet

Data and scripts for the following monograph:

Howanitz, Gernot. 2020. *Leben Weben. (Auto-)Biographische Praktiken russischer Autorinnen und Autoren im Internet*. Bielefeld: transcript. (= PhD thesis, U of Passau 2017). [Available in Open Access](https://www.transcript-verlag.de/media/pdf/43/90/40/oa9783839451328.pdf)

Uses Python 3.9 and Jupyter notebooks for visualisation.

**Note: This repository is not updated anymore. Active development happens over [here](https://github.com/ghowa/generic-topic-modeling)

## Installation

0. Check out this repository

```
git init
git clone https://github.com/ghowa/russian-blogs.git
```
### Variant 1: Pip

1.1 Install required python packages

```
pip install -r requirements.txt
```

1.2 Activate qgrid:

```
jupyter nbextension enable --py --sys-prefix qgrid

# only required if you have not enabled the ipywidgets nbextension yet
jupyter nbextension enable --py --sys-prefix widgetsnbextension
```

### Variant 2: Anaconda

2.1 Install required python packages

```
conda env create -f environment.yml
```

## Usage

Start Jupyter notebook: 

```
jupyter notebook
```

A browser window will open. Select "corpus.ipynb" for browsing the corpus or "create_lda.ipynb" for creating a new topic model of the corpus.
