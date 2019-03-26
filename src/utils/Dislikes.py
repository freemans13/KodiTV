class Dislikes:
    """
    retrieves a list of all disliked shows from the database adn stores it in a list
    this acts as a cache, so we can access the table once and store the results in a list for access
    without going through database every time
    """
    def __init__(self, cursor):
        select_dislikes = ("SELECT title "
                           "FROM shows "
                           "WHERE disliked = 1")

        self.disliked_shows = []
        cursor.execute(select_dislikes)
        for (title,) in cursor:
            self.disliked_shows.append(title)
        print("dislikes = ", self.disliked_shows)

    def is_disliked(self, title):
        """
        tells whether a show is disliked or not

        :param title:
        :return: If title exists in list
        """
        return title in self.disliked_shows


