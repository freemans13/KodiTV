class Dislikes:

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
        return title in self.disliked_shows


