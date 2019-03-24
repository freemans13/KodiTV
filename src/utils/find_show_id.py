def find_show_id(title, cursor):

    find_show_record = ("SELECT show_ID "
                        "FROM shows "
                        "WHERE title = %s")

    cursor.execute(find_show_record, (title,))

    for (show_ID,) in cursor:
        return show_ID
