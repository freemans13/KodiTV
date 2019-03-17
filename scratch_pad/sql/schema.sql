create table shows (
  show_ID int not null auto_increment,
  date datetime not null,
  title varchar(255) not null unique,
  channel varchar(255),
  channel_number int not null,
  constraint shows_pk primary key (show_ID)
);
create table genres (
  genre_ID int not null auto_increment,
  genre varchar(20) not null unique,
  constraint genres_pk primary key (genre_ID)
);
create table show_genre_map (
  genre_ID int not null,
  show_ID int not null,
  constraint show_genre_map_pk primary key (genre_ID, show_ID),
  INDEX show_genre_map_genre_id_ind (genre_ID),
    FOREIGN KEY (genre_ID)
        REFERENCES genres(genre_ID)
        ON DELETE CASCADE,
  INDEX show_genre_map_show_id_ind (show_ID),
    FOREIGN KEY (show_ID)
        REFERENCES shows(show_ID)
        ON DELETE CASCADE
);
create table episodes (
  show_ID int not null,
  season int not null,
  episode int not null,
  plot varchar(255),
  constraint shows_pk primary key (show_ID, season, episode, plot)
);
create table dislikes (
  show_ID int not null,
  constraint dislikes_pk primary key (show_ID)
);

