'''CREATE DATABASE IF NOT EXISTS hbtn_0d_tvshows'''
CREATE database IF NOT EXISTS hbtn_0d_tvshows;

'''Create table named users with three input'''
CREATE TABLE IF NOT EXISTS users(
    id int AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email string(255) NOT NULL UNIQUE,
    name string(255),
);
