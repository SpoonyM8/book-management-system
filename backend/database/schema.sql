drop table if exists Users;
create table Users (
    username varchar(50) not null,
    firstName varchar(50) not null,
    lastName varchar(50) not null,
    email varchar(50) not null,
    userPassword varchar(30) not null,
    primary key (username)
);

drop table if exists Books;
create table Books (
    bookID varchar(36) not null,
    title varchar(50) not null,
    author varchar(100),
    yearPublished int,
    publisher varchar(50),
    coverImage varchar(100),
    numRead int default 0,
    averageRating float default 0.0,
    numRatings int default 0,
    genre varchar(50) default "Fiction",
    primary key (bookID),
    check (numRead >= 0),
    check (averageRating >= 0 and averageRating <= 5),
    check (numRatings >= 0)
);

drop table if exists Reviews;
create table Reviews (
    username varchar(36) not null,
    bookID varchar(36) not null,
    rating float not null,
    comment varchar(1000),
    timeAdded datetime not null,
    primary key (username, bookID),
    foreign key (username) references Users(username),
    foreign key (bookID) references Books(bookID),
    check (rating >= 0 and rating <= 5)
);

drop table if exists Collections;
create table Collections (
    collectionID varchar(36) not null,
    username varchar(36) not null,
    collectionName varchar(50) not null,
    primary key (collectionID),
    foreign key (username) references Users(username)
);

drop table if exists CollectionBooks;
create table CollectionBooks (
    bookID varchar(36) not null,
    collectionID varchar(36) not null,
    timeAdded datetime not null,
    primary key (bookID, collectionID),
    foreign key (bookID) references Books(bookID),
    foreign key (collectionID) references Collections(collectionID)
);

drop table if exists UserGoals;
create table UserGoals (
    goalID varchar(36) not null,
    username varchar(36) not null,
    numRead integer not null,
    numTarget integer not null,
    numMonth integer not null,
    numYear integer not null,
    primary key (username, numMonth, numYear),
    foreign key (username) references Users(username),
    check (numTarget >= 0),
    check (numMonth >= 1 and numMonth <= 12)
);

drop table if exists hasRead;
create table hasRead (
    username varchar(36) not null,
    bookID varchar(36) not null,
    numMonth integer not null,
    numYear integer not null,
    primary key (username, bookID),
    foreign key (username) references UserGoals(username),
    foreign key (bookID) references Books(bookID)
);

drop table if exists SharedCollections;
create table SharedCollections (
    collectionID varchar(36) not null,
    collectionName varchar(50) not null,
    collectionOwner varchar(36) not null,
    primary key (collectionID, collectionOwner),
    foreign key (collectionOwner) references Users(username)
);

drop table if exists SharedCollectionMembers;
create table SharedCollectionMembers (
    collectionID varchar(36) not null,
    member varchar(36) not null,
    primary key (collectionID, member),
    foreign key (collectionID) references SharedCollections(collectionID),
    foreign key (member) references Users(username)
);

drop table if exists SharedCollectionBooks;
create table SharedCollectionBooks (
    bookID varchar(36) not null,
    collectionID varchar(36) not null,
    member varchar(36) not null,
    timeAdded datetime,
    primary key (bookID, collectionID, member),
    foreign key (bookID) references Books(bookID),
    foreign key (collectionID) references SharedCollections(collectionID),
    foreign key (member) references Users(username)
);

drop table if exists Follows;
create table Follows (
    username1 varchar(36) not null,
    username2 varchar(36) not null,
    primary key (username1, username2),
    foreign key (username1) references Users(username),
    foreign key (username2) references Users(username)
)
