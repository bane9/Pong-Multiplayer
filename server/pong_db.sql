drop database if exists pong_server;
create database pong_server;
use pong_server;

create table users(
	id int auto_increment,
	username varchar(25) not null,
    password varchar(25) not null,
    primary key(id)
);

SET GLOBAL log_bin_trust_function_creators = 1;

delimiter //
create function register_user(new_username varchar(25), new_password varchar(25))
returns varchar(25)
begin
	if exists(select username from users where username=new_username)
	then
		return "Username already exists";
	end if;
    
    insert into users (username, password)
    values (new_username, new_password);
    
	return "Ok";
end; //

create function login_user(login_username varchar(25), login_password varchar(25))
returns varchar(25)
begin
	declare uname, pwd varchar(25);

	if not exists(select username from users where username=login_username)
	then
		return "Username does not exist";
	end if;
    
    select username into uname from users where username=login_username;
    select password into pwd from users where username=login_username;
    
    if(pwd != login_password)
    then
		return "Invalid password";
	end if;
    
	return "Ok";
end; //

delimiter ;

select register_user("user1", "pwd1");
select register_user("user2", "pwd2");

-- select register_user("user2", "pwd2");

-- select login_user("user1", "pwd1");
-- select login_user("user2", "pwd2");

-- select login_user("rnd", "rnd");
-- select login_user("user1", "rnd");
