def find_show_id(title, cursor):
    """
    Returns show_ID for current show

    :param title: current broadcasts title
    :param cursor: db cursor

    :return: current broadcasts show_ID
    """

    find_show_record = ("SELECT show_ID "
                        "FROM shows "
                        "WHERE title = %s")

    cursor.execute(find_show_record, (title,))

    for (show_ID,) in cursor:
        return show_ID
