create table accounts
(
    account          varchar(20) not null
        primary key,
    sector           varchar(20) null,
    year_established int         null,
    revenue          double      null,
    empolyees        varchar(20) null,
    office_location  varchar(20) null,
    subsdiary_of     varchar(10) null
);

create table data_dictionary
(
    `table`     varchar(20) null,
    field       varchar(20) null,
    description varchar(50) null
);

create table dim_time
(
    time_date   date not null
        primary key,
    engage_date date null,
    close_date  date null,
    year        int  null,
    quater      int  null,
    month       int  null
);

create table products
(
    product     varchar(20) not null
        primary key,
    seriers     varchar(20) null,
    sales_price int         null
);

create table sales_teams
(
    sales_agent     varchar(20) not null
        primary key,
    manager         varchar(20) null,
    regional_office varchar(20) null
);

create table sales_pipeline
(
    opportunity_id varchar(20) null,
    sales_agent    varchar(20) null,
    product        varchar(20) null,
    account        varchar(20) null,
    deal_stage     varchar(20) null,
    engage_date    date        null,
    close_date     date        null,
    close_value    int         null,
    constraint sales_pipeline_ibfk_1
        foreign key (account) references accounts (account),
    constraint sales_pipeline_ibfk_2
        foreign key (product) references products (product),
    constraint sales_pipeline_ibfk_3
        foreign key (sales_agent) references sales_teams (sales_agent),
    constraint sales_pipeline_ibfk_4
        foreign key (engage_date) references dim_time (time_date),
    constraint sales_pipeline_ibfk_5
        foreign key (close_date) references dim_time (time_date)
);

create index account
    on sales_pipeline (account);

create index close_date
    on sales_pipeline (close_date);

create index engage_date
    on sales_pipeline (engage_date);

create index product
    on sales_pipeline (product);

create index sales_agent
    on sales_pipeline (sales_agent);


