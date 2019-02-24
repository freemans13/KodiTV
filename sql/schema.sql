create table history (
  history_ID int not null auto_increment,
  date datetime not null,
  title     varchar(255) not null,
  channel   varchar(255),
  channel_number int not null,
  event_type varchar(30)not null,
  constraint history_pk primary key (history_ID)
);
create  table genres (
  genre_ID int not null auto_increment,
  genre varchar(20) not null unique,
  constraint genres_pk primary key (genre_ID)
);
create table history_genre_map (
  genre_ID int not null,
  history_ID int not null,
  constraint history_genre_map_pk primary key (genre_ID, history_ID),
  INDEX history_genre_map_genre_id_ind (genre_ID),
    FOREIGN KEY (genre_ID)
        REFERENCES genres(genre_ID)
        ON DELETE CASCADE,
  INDEX history_genre_map_history_id_ind (history_ID),
    FOREIGN KEY (history_ID)
        REFERENCES history(history_ID)
        ON DELETE CASCADE
);
