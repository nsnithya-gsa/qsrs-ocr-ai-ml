CREATE TABLE t_ai_model
(
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(50),
    model_start_date date,
    model_stop_date date
);