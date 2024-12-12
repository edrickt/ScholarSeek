<p align="center"><img src="./scholarseek/search/static/res/logo.png"></p>

<p align="center">
    <img src="https://img.shields.io/badge/development-stage-red?style=for-the-badge">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
    <a href="https://docs.djangoproject.com/en/4.2/"><img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"></a>
</p>

<p align="center">
ScholarSeek, developed using Django and PyTerrier, is a academic search engine. Designed for seamless access to a vast database of scholarly articles and academic papers, catering to researchers, educators, and students who seek efficient and precise academic resources.
</p>

# Installation
 - Git clone the repository: `git clone https://github.com/nihalafs11/cs6821-IR-Project`

 - Install Python and JDK

 - Note: If you're on M1 Mac you need to install an additional library called PCRE, This can be done with Homebrew `brew install pcre` 

 - Create a python virtual environment `python3 -m venv env`

 - Source and activate your python virtual environment `source env/bin/activate`

 - Install the necessary packages by running the following command: `pip3 install -r "requirements.txt"`

 - Run proper migrations `python manage.py makemigrations` and `python manage.py migrate`

 - Install [arXiv Dataset - arxiv-metadata-oai-snapshot.json](https://www.kaggle.com/datasets/Cornell-University/arxiv/download?datasetVersionNumber=154) into your local /scholarseek folder -> Your "search" folder and "manage.py" would also be in here.
   
 - Build the proper index for the arxiv-metadata-oai-snapshot.json data `python build_index.py` Note: Due to the huge amount of data, this may take some time to install

 - Run Django in debug mode with: `python manage.py runserver`


# Tasks

- Check out the Github Boards or Issues! 

