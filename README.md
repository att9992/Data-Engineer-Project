# Udacity Data Engineering Capstone Project

## Project description

The aim for this project is to answer such as:

* Which Github repository are the most popular according to Hacker News activity?
* Which Github users are generating the most activity on Hacker News?

Data is downloaded from Kaggle's sources:

* List of GitHub repositories created between 29 Oct 2007 and 12 Nov 2010 - https://www.kaggle.com/qopuir/github-repositories
* Hacker News posts (all posts since 2006) - https://www.kaggle.com/santiagobasulto/all-hacker-news-posts-stories-askshow-hn-polls

## Tooling

The tools used on this project are the same as we have been learning during the Data Engineer Nanodegree course.

* Amazon S3 for File Storage
* Amazon Redshift for Data Storage
* Apache Airflow as an Orchestration Tool

Those tools are widely used and considered as industry standards. The community is massive and the tools provide support to several features. Apache Airflow, in special, gives freedom to create new plugins and adapt it to any needs that we might have. 

## Data assessment

* The GitHub repo data is just for a repository created between certain dates so I decided to limit the date range for which we pull in Hacker News data. 
* The language, license, size, stars, forks, open_issues and created_at columns for Github repository data are sometimes empty
* The num_comments column for Hacker News posts can sometimes be empty.
* Some of the Hacker News URLs are very long, hence the maximum field length for this column has been set to 8192.
* To analyse Hacker News activity related to GitHub repository, rows are filtered for which the URL contains a GitHub URL. This is done when loading data from the staging table into the hacker_news_posts dimension table using a regular expression.


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

## Data Dictionary

***github_repos*** table
| Field         | Type          | PK    |
| ------------- |:-------------:| -----:|
| id            | int | Yes|
| owner_id      | int      |    |
| full_name     | varchar      |    |
|repo_detail_url| varchar   |   |
|is_fork | boolean |   |
|repo_commits_url| varchar    |   |
|language| varchar   |   |
|license | varchar   |    |
|size  |  int   |   |
|stars |  int   |    |
|forks |  int    |     |
|open_issues| int  |   |
|created_at| timestamp    |     |

***github_user*** table
| Field         | Type          | PK    |
| ------------- |:-------------:| -----:|
| id            | int | Yes|
| name      | varchar      |    |

***github_repo_popularity*** table
| Field         | Type          | PK    |
| ------------- |:-------------:| -----:|
| github_repo_id| int | Yes|
| starts    | int      |    |
|forks|int|  |
|total_hn_points|int|   |
|total_hn_comment| int  |  |

***hacker_new_posts_ref_github*** table
| Field         | Type          | PK    |
| ------------- |:-------------:| -----:|
| id            | int | Yes|
| title      | varchar      |    |
|post_type|varchar  | |
|author|varchar   |   |
|created_at| timestamp |   |
|url  | varchar   |   |
|github_repo_full_name|  varchar    |   |
|points|  int    |     |
|num_comments|  int  |


## Scenarios
* Data increase by 100x. 
  + Redshift: Analytical database, optimized for aggregation, also good performance for read-heavy workloads
  + Increase EMR cluster size to handle bigger volume of data

* Pipelines would be run on 7 am daily. 
  + DAG is scheduled to run every 5 minutes and can be configured to run every morning at 7 AM if required.
  + Data quality operators are used at appropriate position. In case of DAG failures email triggers can be configured to let the team know about pipeline failures.

* Make it available to 100+ people
  + The more people accessing the database the more cpu resources you need to get a fast experience. By using a distributed database you can improve your replications and partitioning to get faster query results for each user.
  + We can set the concurrency limit for your Amazon Redshift cluster. While the concurrency limit is 50 parallel queries for a single period of time, this is on a per cluster basis, meaning you can launch as many clusters as fit for you business.
  
