from django.db import connection


def table_exists(table_name):
    """
    Checks if a database table exists.

    Args:
        table_name (str): Name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                );
                """,
            [table_name],
        )
        return cursor.fetchone()[0]
