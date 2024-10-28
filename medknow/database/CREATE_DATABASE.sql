-- \set dataBase db_operational
-- ;
-- \set userName postgres
-- ;
-- \connect :dataBase :userName
-- ;

-- Drop tables if they exist
DROP TABLE IF EXISTS public.appointments CASCADE;
DROP TABLE IF EXISTS public.patients CASCADE;
DROP TABLE IF EXISTS public.measurements CASCADE;
DROP TABLE IF EXISTS public.prescription_types CASCADE;
DROP TABLE IF EXISTS public.doctors CASCADE;
DROP TABLE IF EXISTS public.lens_type CASCADE;
DROP TABLE IF EXISTS public.tear_rates CASCADE;
DROP TABLE IF EXISTS public.ages CASCADE;

-- Create tables

-- Table: ages
create table public.ages
(
    age_id serial
        constraint ages_pk
            primary key,
    name   varchar
        constraint ages_pk_2
            unique
);


-- Table: tear_rates
create table public.tear_rates
(
    tear_rate_id serial
        constraint tear_rates_pk
            primary key,
    name         varchar not null
        constraint tear_rates_pk_2
            unique
);



-- Table: lens_type
create table public.lens_type
(
    lens_type_id serial
        constraint lens_type_pk
            primary key,
    name         varchar
);


-- Table: doctors
create table public.doctors
(
    doctor_id serial
        constraint doctors_pk
            primary key,
    name      varchar not null,
    surname  varchar not null
);


-- Table: prescription_types
create table public.prescription_types
(
    prescription_type_id serial
        constraint prescription_types_pk
            primary key,
    name                 varchar
);


-- Table: measurements
create table public.measurements
(
    measurement_id       serial
        constraint measurements_pk
            primary key,
    measurement_date     date    not null,
    expiration_date      date    not null,
    age_id               integer not null
        constraint measurements_ages_age_id_fk
            references public.ages,
    tear_rate_id         integer not null
        constraint measurements_tear_rates_tear_rate_id_fk
            references public.tear_rates,
    last_measurement_id  integer
        constraint measurements_measurements_measurement_id_fk
            references public.measurements,
    astigmatic            boolean not null,
    prescription_type_id integer not null
        constraint measurements_prescription_types_prescription_id_fk
            references public.prescription_types
);


-- Table: patients
create table public.patients
(
    patient_id          serial
        constraint patients_pk
            primary key,
    name                varchar not null,
    surname            varchar not null,
    birth_date          date    not null,
    last_measurement_id integer
        constraint patients_measurements_measurement_id_fk
            references public.measurements
);


-- Table: appointments
create table public.appointments
(
    patient_id          integer not null
        constraint appointments_patients_patient_id_fk
            references public.patients,
    doctor_id           integer not null
        constraint appointments_doctors_doctor_id_fk
            references public.doctors,
    appointment_date    date    not null,
    lens_type_id        integer not null
        constraint appointments_lens_type_lens_type_id_fk
            references public.lens_type,
    used_measurement_id integer not null
        constraint appointments_measurements_measurement_id_fk
            references public.measurements,
    constraint appointments_pk
        primary key (patient_id, appointment_date)
);

-- Inserting data

-- Inserting into ages
insert into public.ages (name) values
('young'),
('presbyopic'),
('pre-presbyopic');

-- Inserting into tear_rates
insert into public.tear_rates (name) values
('normal'),
('reduced');

-- Inserting into lens_type
insert into public.lens_type (name) values
('hard'),
('soft'),
('none');

-- Inserting into prescription_types
insert into public.prescription_types (name) values
('myope'),
('hypermetrope'),
('none');