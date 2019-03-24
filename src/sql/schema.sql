create table shows (
  show_ID int not null auto_increment,
  date timestamp not null default current_timestamp,
  title varchar(255) not null unique,
  disliked tinyint(1) not null default 0 check(disliked = 0 or disliked = 1),
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
  date timestamp not null default current_timestamp,
  show_ID int not null,
  season int not null,
  episode int not null,
  plot varchar(255),
  constraint shows_pk primary key (show_ID, season, episode),
  INDEX episodes_show_id_ind (show_ID),
    FOREIGN KEY (show_ID)
        REFERENCES shows(show_ID)
        ON DELETE CASCADE
);
create table channels (
  channel_ID int not null auto_increment,
  channel varchar(255) not null unique,
  constraint channels_pk primary key(channel_ID)
);
create table show_channel_map (
  channel_ID int not null,
  show_ID int not null,
  constraint show_channel_map_pk primary key (channel_ID, show_ID),
  INDEX show_channel_map_channel_id_ind (channel_ID),
    FOREIGN KEY (channel_ID)
      REFERENCES channels(channel_ID)
      ON DELETE CASCADE,
  INDEX show_channel_map_show_id_ind (show_ID),
    FOREIGN KEY (show_ID)
      REFERENCES shows(show_ID)
      ON DELETE CASCADE
);
