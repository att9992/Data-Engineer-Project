class DataValidationQueries:

    gh_repos_table = """
        SELECT count(*) != 0
        FROM github_repos
    """

    gh_users_table = """
        SELECT count(*) != 0
        FROM github_users
    """

    hn_posts_table = """
        SELECT count(*) != 0
        FROM hacker_news_posts
    """

    gh_repos_popularity_table = """
        SELECT count(*) != 0
        FROM github_repo_popularity
    """

    gh_repos_owner_null = """
        SELECT count(*)
        FROM github_repos
        WHERE owner_id is NULL
    """

    gh_repos_name_null = """
        SELECT count(*)
        FROM github_repos
        WHERE full_name is NULL
            OR full_name = ''
    """

    gh_users_name_null = """
        SELECT count(*)
        FROM github_users
        WHERE name is NULL
            OR name = ''
    """

    hn_posts_ref_github_exist = """
        SELECT count(*) != 0
        FROM hacker_news_posts
        WHERE github_repo_full_name is NULL
            OR github_repo_full_name = ''
    """

    hn_posts_points_null = """
        SELECT count(*)
        FROM hacker_news_posts
        WHERE points is NULL
    """
