class Dislikes:

    def __init__(self, cursor):
        select_dislikes = ("select s.title "
                           "from shows s "
                           "inner join dislikes d on s.show_id = d.show_id")

        self.disliked_shows = []
        cursor.execute(select_dislikes)
        for (title,) in cursor:
            self.disliked_shows.append(title)
        print("dislikes = ", self.disliked_shows)

    def is_disliked(self, title):
        return title in self.disliked_shows


