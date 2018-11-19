drop table s_c_map;
drop table c_p_map;
drop table course;
drop table student;

create table student (
	s_id varchar(10) not null,
	s_name varchar(50) not null,
	s_phone varchar(10) not null,
	s_email varchar(50) not null,
	s_password varchar(50) not null,
	PRIMARY key(s_id)
);

create table course (
	c_id varchar(10) not null,
	c_name varchar(50) not null,
	sem int not null,
	elective binary not null,
	pool int not null,
	primary key(c_id)
);

create table c_p_map (
	c_id varchar(10) not null,
	p_id varchar(10) not null,
	primary key(c_id, p_id),
	foreign KEY (c_id) references course(c_id),
	foreign key (p_id) references course(c_id)
);

create table s_c_map (
	s_c_id int not null auto_increment,
	marks int not null,
	c_id varchar(10) not null,
	s_id varchar(10) not null,
	year int not null,
	primary key(s_c_id),
	foreign KEY (c_id) references course(c_id),
	foreign key(s_id) references student(s_id)
);
