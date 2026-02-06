CREATE TABLE billing (
    invoice_id   VARCHAR(50) PRIMARY KEY,
    patient_id   VARCHAR(50) NOT NULL,
    amount       NUMERIC(10,2) NOT NULL,
    status       VARCHAR(20) NOT NULL,
    paid_date    TIMESTAMP,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Optional FK constraint (if patients table exists)
    CONSTRAINT fk_billing_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);
