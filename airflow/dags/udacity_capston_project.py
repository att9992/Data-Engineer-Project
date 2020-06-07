from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators import (S3ToRedshiftOperator,LoadTableOperator,DataQualityOperator)
from airflow.operators.dummy_operator import DummyOperator

from helpers import SqlQueries, DataValidationQueries

default_args = {
    'owner': 'trananhtong',
    'start_date': datetime(2020, 6, 6),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
}

dag = DAG(
    'udacity-project-github',
    default_args=default_args,
    description='Full ETL pipeline to load and process data',
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
)

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

load_s3_gh_to_redshift = S3ToRedshiftOperator(
    task_id='Load_gh_repos',
    dag=dag,
    table='staging_github_repos',
    create_table_sql=SqlQueries.create_staging_github_repos,
    s3_key='github-repositories.csv',
)

load_s3_hn_to_redshift = S3ToRedshiftOperator(
    task_id='Load_hn_posts',
    dag=dag,
    table='staging_hacker_news_posts',
    create_table_sql=SqlQueries.create_staging_hacker_news_posts,
    s3_key='hn.csv',
)

load_github_repos_table = LoadTableOperator(
    task_id='Load_github_repos_table',
    dag=dag,
    destination_table='github_repos',
    select_query=SqlQueries.insert_github_repos,
    create_table_sql=SqlQueries.create_github_repos,
)

load_github_users_table = LoadTableOperator(
    task_id='Load_github_users_table',
    dag=dag,
    destination_table='github_users',
    select_query=SqlQueries.insert_github_users,
    create_table_sql=SqlQueries.create_github_users,
)

load_hn_posts = LoadTableOperator(
    task_id='Load_hacker_news_posts',
    dag=dag,
    destination_table='hacker_news_posts',
    select_query=SqlQueries.insert_hacker_news_posts,
    create_table_sql=SqlQueries.create_hacker_news_posts,
)

github_repo_popularity = LoadTableOperator(
    task_id='Compute_github_repo_popularity',
    dag=dag,
    destination_table='github_repo_popularity',
    select_query=SqlQueries.insert_github_repo_popularity,
    create_table_sql=SqlQueries.create_github_repo_popularity,
)

validation_github_repos = DataQualityOperator(
    task_id='Data_validation_github_repos',
    dag=dag,
    checks=[
        (DataValidationQueries.gh_repos_table, True),
        (DataValidationQueries.gh_repos_owner_null, 0),
        (DataValidationQueries.gh_repos_name_null, 0),
    ],
)

validation_github_users = DataQualityOperator(
    task_id='Data_validation_github_users',
    dag=dag,
    checks=[
        (DataValidationQueries.gh_users_table, True),
        (DataValidationQueries.gh_users_name_null, 0),
    ],
)

validation_hn_posts = DataQualityOperator(
    task_id='Data_validation_hacker_news_posts',
    dag=dag,
    checks=[
        (DataValidationQueries.hn_posts_table, True),
        (DataValidationQueries.hn_posts_ref_github_exist, True),
        (DataValidationQueries.hn_posts_points_null, 0),
    ],
)

validation_github_repo_popularity = DataQualityOperator(
    task_id='Data_validation_github_repo_popularity',
    dag=dag,
    checks=[
        (DataValidationQueries.gh_repos_popularity_table, True)
    ],
)

end_operator = DummyOperator(task_id='End_execution',dag=dag)


start_operator >> [load_s3_gh_to_redshift,load_s3_hn_to_redshift]


load_s3_gh_to_redshift >> [load_github_repos_table,load_github_users_table]

load_s3_hn_to_redshift >> load_hn_posts


load_github_repos_table >> validation_github_repos
load_github_users_table >> validation_github_users

load_hn_posts >> validation_hn_posts


[validation_github_repos, validation_github_users,validation_hn_posts] >> github_repo_popularity

github_repo_popularity >> validation_github_repo_popularity >> end_operator
