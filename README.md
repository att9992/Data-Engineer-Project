# Udacity Data Engineering Capstone Project

## Project description

The aim for this project is to pull in data from 2 different data sources:

* List of GitHub repositories created between 29 Oct 2007 and 12 Nov 2010 - https://www.kaggle.com/qopuir/github-repositories
* Hacker News posts (all posts since 2006) - https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls

This data will then be prepared for analysis to answer questions such as:

* Which Github repository are the most popular according to Hacker News activity?
* Which Github users are generating the most activity on Hacker News?

## Tooling

The tools used on this project are the same as we have been learning during the Data Engineer Nanodegree course.

* Amazon S3 for File Storage
* Amazon Redshift for Data Storage
* Apache Airflow as an Orchestration Tool

Those tools are widely used and considered as industry standards. The community is massive and the tools provide support to several features. Apache Airflow, in special, gives freedom to create new plugins and adapt it to any needs that we might have. 

## Data model
The final data model include four tables, being three of them dimensions and a fact table.

[<img src="https://github.com/att9992/Data-Engineer-Project/blob/master/DataModel.PNG">](https://github.com)

The two staging tables are on the left and represent the data from the source CSV files with data typing applied. The tables on the right represent the dimension tables and the fact table (github_repo_popularity). The fact table contains metrics of popularity for GitHub repositories.

## ETL pipeline
The ETL pipeline is ran via an Airflow DAG:

[<img src="https://github.com/att9992/Data-Engineer-Project/blob/master/ETL.png">](https://github.com)


The DAG is comprised of a few main stages:

* We first pull in the data from the two CSV files in S3 into two staging tables in Redshift; one for the GitHub repo data and one for the Hacker News posts.
* Data is then loaded into the three dimension tables: GitHub repos, GitHub users, and Hacker News posts
* Data quality checks are then performed on the data to ensure we have data in these tables and that we don't have any values that we're not expecting.
* The fact table, github_repo_popularity, is then built by joining data from two of the dimension tables.
* A final data validation check is performed on the fact table to ensure we have data.

