-- Inserting into doctors
INSERT INTO public.doctors (name, surname) VALUES
    ('Alice', 'Johnson'),
    ('Brian', 'Williams'),
    ('Catherine', 'Miller'),
    ('David', 'Brown'),
    ('Emma', 'Davis');

-- Inserting into measurements
INSERT INTO public.measurements (measurement_date, expiration_date, age_id, tear_rate_id, last_measurement_id, astigmatic, prescription_type_id) VALUES
    ('2024-10-01', '2025-10-01', 1, 1, NULL, TRUE, 1),
    ('2024-10-02', '2025-10-02', 1, 1, NULL, FALSE, 1),
    ('2024-10-03', '2025-10-03', 1, 2, NULL, TRUE, 2),
    ('2024-10-04', '2025-10-04', 1, 1, NULL, FALSE, 2),
    ('2024-10-05', '2025-10-05', 1, 2, NULL, FALSE, 2),
    ('2024-10-06', '2025-10-06', 2, 2, NULL, TRUE, 1),
    ('2024-10-07', '2025-10-07', 2, 1, NULL, TRUE, 1),
    ('2024-10-08', '2025-10-08', 2, 2, NULL, TRUE, 2),
    ('2024-10-09', '2025-10-09', 2, 1, NULL, TRUE, 2),
    ('2024-10-10', '2025-10-10', 2, 1, NULL, FALSE, 2),
    ('2024-10-11', '2025-10-11', 2, 2, NULL, FALSE, 2),
    ('2024-10-12', '2025-10-12', 3, 2, NULL, TRUE, 1),
    ('2024-10-13', '2025-10-13', 3, 1, NULL, TRUE, 1),
    ('2024-10-14', '2025-10-14', 3, 1, NULL, FALSE, 1),
    ('2024-10-15', '2025-10-15', 3, 1, NULL, TRUE, 2),
    ('2024-10-16', '2025-10-16', 3, 1, NULL, FALSE, 2);

-- Inserting into patients
INSERT INTO public.patients (name, surname, birth_date, last_measurement_id) VALUES
    ('Liam', 'Smith', '2004-05-15', 1),
    ('Olivia', 'Taylor', '2003-08-22', 2),
    ('Noah', 'Anderson', '2005-12-10', 3),
    ('Ava', 'Thomas', '2004-07-30', 4),
    ('Elijah', 'Jackson', '2005-03-25', 5),
    ('Sophia', 'White', '1964-11-05', 6),
    ('James', 'Harris', '1965-02-17', 7),
    ('Isabella', 'Martin', '1963-09-09', 8),
    ('Benjamin', 'Thompson', '1962-04-12', 9),
    ('Mia', 'Garcia', '1966-06-18', 10),
    ('Lucas', 'Martinez', '1961-01-30', 11),
    ('Charlotte', 'Robinson', '1979-03-14', 12),
    ('Mason', 'Clark', '1978-07-19', 13),
    ('Amelia', 'Rodriguez', '1980-10-23', 14),
    ('Ethan', 'Lewis', '1977-05-07', 15),
    ('Harper', 'Lee', '1981-11-29', 16);

-- Inserting into appointments
INSERT INTO public.appointments (patient_id, doctor_id, appointment_date, lens_type_id, used_measurement_id) VALUES
    (1, 1, '2024-10-20', 1, 1),
    (2, 2, '2024-10-21', 2, 2),
    (3, 3, '2024-10-22', 3, 3),
    (4, 1, '2024-10-23', 2, 4),
    (5, 2, '2024-10-24', 3, 5),
    (6, 4, '2024-10-25', 3, 6),
    (7, 5, '2024-10-26', 1, 7),
    (8, 2, '2024-10-27', 1, 8),
    (9, 3, '2024-10-28', 3, 9),
    (10, 1, '2024-10-29', 2, 10),
    (11, 4, '2024-10-30', 3, 11),
    (12, 5, '2024-10-31', 3, 12),
    (13, 1, '2024-11-01', 1, 13),
    (14, 2, '2024-11-02', 2, 14),
    (15, 3, '2024-11-03', 3, 15),
    (16, 5, '2024-11-04', 2, 16);