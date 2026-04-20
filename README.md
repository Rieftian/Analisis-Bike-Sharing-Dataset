# Dicoding Collection Dashboard

## Setup Environment - Anaconda
git clone https://github.com/Rieftian/Analisis-Bike-Sharing-Dataset.git  
conda create --name main-ds python=3.9  
conda activate main-ds     
pip install -r requirements.txt  

## Setup Environment - Terminal/Shell
git clone https://github.com/Rieftian/Analisis-Bike-Sharing-Dataset.git  
cd Analisis-Bike-Sharing-Dataset  
pip install pipenv  
pipenv shell  
pip install -r requirements.txt  

## Run Streamlit App
streamlit run dashboard/dashboard.py
