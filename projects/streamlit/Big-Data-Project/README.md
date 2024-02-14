# Big-Data
The following project is a Big Data project using the Yelp dataset. 

This project aims to increase Yelps revenue by developing a dashboard that generates insights to target advertising campaigns.

This repository has:
1 Jupyter notebook:
  1. The process of adding the JSON data into the HDFS and then creating the tables in the Hive Warehouse - Project_Data_HDFS.ipynb

3 python scripts for the Streamlit dashboard, based in Python and Pyspark for data processing. 
1 main python script for the Streamlit dashboard

This project uses a docker container that can be found in my [Docker-For-Data-Science](https://github.com/Sebasc322/Docker-For-Data-Science/tree/main/Big-Data) repository!  

The data architecture of the following project looks like this:
![Architecture.jpg](https://github.com/Sebasc322/Big-Data/blob/main/Architecture.jpg)

The data can be found on the [Yelp dataset](https://www.yelp.com/dataset)


Go to the terminal and run:
```python 
streamlit run Yelp.py
```

This will run the Streamlit dashboard.

![home.jpg](https://github.com/Sebasc322/Big-Data-Project/blob/main/home.jpg)

