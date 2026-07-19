-- ============================================================================
-- MediFlow: Seed Data for Development and Testing
-- PostgreSQL Database
--
-- Version: 1.0.0
-- Created: 2024-01-15
-- Schema: mediflow
--
-- Purpose: Insert sample/test data for development, testing, and demo purposes
-- WARNING: This file is for DEVELOPMENT ONLY. Do not use in production without review.
--
-- Data Contents:
--   - 1 Hospital
--   - 3 Doctors with different specializations
--   - 5 Test Patients
--   - 8 Sample Medications
--   - 5 Sample Prescriptions with items
--   - 10 Sample Appointments
--   - 3 Sample Documents
--   - Various supporting records
--
-- ============================================================================

SET search_path = mediflow, public;

-- ============================================================================
-- SECTION 1: CLEAR EXISTING DATA (DEVELOPMENT ONLY)
-- ============================================================================

-- Uncomment the following lines only for development environments
-- DELETE FROM prescription_items;
-- DELETE FROM prescriptions;
-- DELETE FROM appointment_notes;
-- DELETE FROM appointments;
-- DELETE FROM documents;
-- DELETE FROM document_access_log;
-- DELETE FROM timeline_events;
-- DELETE FROM notifications;
-- DELETE FROM reminders;
-- DELETE FROM ai_summaries;
-- DELETE FROM consent_records;
-- DELETE FROM users;
-- DELETE FROM user_sessions;
-- DELETE FROM audit_logs;
-- DELETE FROM error_logs;
-- DELETE FROM system_event_logs;
-- DELETE FROM medications;
-- DELETE FROM patients;
-- DELETE FROM doctors;
-- DELETE FROM hospitals;


-- ============================================================================
-- SECTION 2: HOSPITAL DATA
-- ============================================================================

INSERT INTO hospitals (
    hospital_id,
    hospital_code,
    name,
    description,
    address_line_1,
    address_line_2,
    city,
    state,
    postal_code,
    country,
    phone_number,
    email,
    website,
    license_number,
    accreditation_status,
    established_date,
    total_beds,
    emergency_enabled,
    surgery_center_enabled,
    is_active,
    metadata
) VALUES (
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'HOSP-001',
    'City General Hospital',
    'A comprehensive 300-bed teaching hospital in downtown area',
    '123 Medical Center Drive',
    'Suite 100',
    'San Francisco',
    'California',
    '94103',
    'United States',
    '+1-415-555-0100',
    'admin@cityhospital.com',
    'www.cityhospital.com',
    'LIC-CA-2024-001',
    'ACCREDITED',
    '1985-06-15'::date,
    300,
    TRUE,
    TRUE,
    TRUE,
    '{"founded_by": "Dr. James Smith", "accreditation_bodies": ["Joint Commission", "CLIA"]}'::jsonb
);


-- ============================================================================
-- SECTION 3: DOCTOR DATA
-- ============================================================================

INSERT INTO doctors (
    doctor_id,
    doctor_code,
    hospital_id,
    first_name,
    last_name,
    middle_name,
    date_of_birth,
    gender,
    medical_license_number,
    specialization,
    sub_specialization,
    qualification_degree,
    qualification_year,
    license_expiry_date,
    years_of_experience,
    email,
    phone_number,
    is_available,
    is_verified,
    verification_date,
    is_active,
    metadata
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    'DOC-001',
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'Sarah',
    'Johnson',
    'Marie',
    '1978-03-25'::date,
    'FEMALE',
    'MED-LIC-CA-2024-001',
    'Cardiology',
    'Interventional Cardiology',
    'MD',
    2001,
    '2026-12-31'::date,
    25,
    'sarah.johnson@cityhospital.com',
    '+1-415-555-0101',
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE,
    '{"board_certified": true, "publications": 12, "specialization_certificate": "Yale School of Medicine"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    'DOC-002',
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'Robert',
    'Chen',
    'Michael',
    '1982-07-10'::date,
    'MALE',
    'MED-LIC-CA-2024-002',
    'Internal Medicine',
    'Gastroenterology',
    'MD',
    2005,
    '2026-12-31'::date,
    19,
    'robert.chen@cityhospital.com',
    '+1-415-555-0102',
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE,
    '{"board_certified": true, "publications": 8, "specialization_certificate": "UCSF School of Medicine"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    'DOC-003',
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'Elizabeth',
    'Williams',
    'Anne',
    '1980-11-15'::date,
    'FEMALE',
    'MED-LIC-CA-2024-003',
    'Orthopedic Surgery',
    'Sports Medicine',
    'MD',
    2003,
    '2026-12-31'::date,
    21,
    'elizabeth.williams@cityhospital.com',
    '+1-415-555-0103',
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE,
    '{"board_certified": true, "publications": 15, "specialization_certificate": "Stanford School of Medicine"}'::jsonb
);


-- ============================================================================
-- SECTION 4: PATIENT DATA
-- ============================================================================

INSERT INTO patients (
    patient_id,
    patient_code,
    first_name,
    last_name,
    middle_name,
    date_of_birth,
    gender,
    email,
    phone_number,
    alternative_phone_number,
    address_line_1,
    address_line_2,
    city,
    state,
    postal_code,
    country,
    blood_group,
    marital_status,
    emergency_contact_name,
    emergency_contact_relationship,
    emergency_contact_phone,
    insurance_provider,
    insurance_policy_number,
    insurance_group_number,
    is_active,
    metadata
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    'PAT-001',
    'John',
    'Anderson',
    'David',
    '1965-05-15'::date,
    'MALE',
    'john.anderson@email.com',
    '+1-415-555-0201',
    '+1-415-555-0202',
    '456 Oak Street',
    'Apt 201',
    'San Francisco',
    'California',
    '94102',
    'United States',
    'O_POSITIVE',
    'MARRIED',
    'Mary Anderson',
    'Spouse',
    '+1-415-555-0299',
    'BlueCross BlueShield',
    'BC-BSH-2024-001',
    'GRP-123456',
    TRUE,
    '{"preferred_contact": "email", "language": "English"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440202'::uuid,
    'PAT-002',
    'Margaret',
    'Thompson',
    'Rose',
    '1958-12-20'::date,
    'FEMALE',
    'margaret.thompson@email.com',
    '+1-415-555-0203',
    NULL,
    '789 Maple Avenue',
    NULL,
    'San Francisco',
    'California',
    '94104',
    'United States',
    'A_NEGATIVE',
    'WIDOWED',
    'James Thompson',
    'Son',
    '+1-415-555-0298',
    'Aetna',
    'AET-2024-002',
    'GRP-654321',
    TRUE,
    '{"preferred_contact": "phone", "language": "English", "mobility_aid": "walker"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    'PAT-003',
    'Michael',
    'Garcia',
    'Anthony',
    '1972-08-03'::date,
    'MALE',
    'michael.garcia@email.com',
    '+1-415-555-0204',
    '+1-415-555-0205',
    '321 Pine Road',
    'Suite 5',
    'San Francisco',
    'California',
    '94105',
    'United States',
    'B_POSITIVE',
    'MARRIED',
    'Sofia Garcia',
    'Spouse',
    '+1-415-555-0297',
    'United Health',
    'UH-2024-003',
    'GRP-789012',
    TRUE,
    '{"preferred_contact": "email", "language": "Spanish", "occupation": "Software Engineer"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440204'::uuid,
    'PAT-004',
    'Jennifer',
    'Martinez',
    'Lynn',
    '1990-02-14'::date,
    'FEMALE',
    'jennifer.martinez@email.com',
    '+1-415-555-0206',
    NULL,
    '654 Birch Lane',
    'Apt 401',
    'San Francisco',
    'California',
    '94106',
    'United States',
    'AB_POSITIVE',
    'SINGLE',
    'Carlos Martinez',
    'Father',
    '+1-415-555-0296',
    'Cigna',
    'CIG-2024-004',
    'GRP-345678',
    TRUE,
    '{"preferred_contact": "email", "language": "English", "occupation": "Teacher"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    'PAT-005',
    'Richard',
    'Kumar',
    'James',
    '1955-09-08'::date,
    'MALE',
    'richard.kumar@email.com',
    '+1-415-555-0207',
    '+1-415-555-0208',
    '987 Cedar Street',
    NULL,
    'San Francisco',
    'California',
    '94107',
    'United States',
    'O_NEGATIVE',
    'MARRIED',
    'Priya Kumar',
    'Spouse',
    '+1-415-555-0295',
    'Kaiser Permanente',
    'KP-2024-005',
    'GRP-901234',
    TRUE,
    '{"preferred_contact": "phone", "language": "Hindi", "occupation": "Retired"}'::jsonb
);


-- ============================================================================
-- SECTION 5: MEDICATION DATA
-- ============================================================================

INSERT INTO medications (
    medication_id,
    medication_code,
    generic_name,
    brand_name,
    ndc_code,
    strength,
    dosage_form,
    route_of_administration,
    manufacturer,
    batch_number,
    expiry_date,
    storage_temperature_min,
    storage_temperature_max,
    storage_instructions,
    is_controlled_substance,
    requires_prescription,
    is_otc,
    therapeutic_category,
    side_effects,
    contraindications,
    quantity_in_stock,
    reorder_level,
    unit_cost,
    is_active,
    metadata
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440301'::uuid,
    'MED-001',
    'Metoprolol Tartrate',
    'Lopressor',
    '00192-0710-10',
    '50mg',
    'Tablet',
    'Oral',
    'Novartis',
    'BATCH-001-2024',
    '2026-06-30'::date,
    15.0,
    25.0,
    'Store at room temperature, away from moisture',
    FALSE,
    TRUE,
    FALSE,
    'Beta-blocker',
    'Dizziness, fatigue, bradycardia',
    'Asthma, decompensated heart failure',
    150,
    50,
    0.45,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "C"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440302'::uuid,
    'MED-002',
    'Lisinopril',
    'Prinivil',
    '00002-7435-20',
    '10mg',
    'Tablet',
    'Oral',
    'Pfizer',
    'BATCH-002-2024',
    '2026-08-31'::date,
    15.0,
    25.0,
    'Store at room temperature',
    FALSE,
    TRUE,
    FALSE,
    'ACE Inhibitor',
    'Persistent dry cough, dizziness',
    'History of angioedema, pregnancy',
    200,
    50,
    0.35,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "D"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440303'::uuid,
    'MED-003',
    'Atorvastatin Calcium',
    'Lipitor',
    '00071-1377-23',
    '20mg',
    'Tablet',
    'Oral',
    'Pfizer',
    'BATCH-003-2024',
    '2026-10-31'::date,
    15.0,
    25.0,
    'Store at room temperature',
    FALSE,
    TRUE,
    FALSE,
    'Statin',
    'Muscle pain, increased liver enzymes',
    'Active liver disease, pregnancy',
    300,
    100,
    0.55,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "X"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440304'::uuid,
    'MED-004',
    'Omeprazole',
    'Prilosec',
    '00025-1139-31',
    '20mg',
    'Capsule',
    'Oral',
    'AstraZeneca',
    'BATCH-004-2024',
    '2026-09-15'::date,
    15.0,
    25.0,
    'Store at room temperature',
    FALSE,
    TRUE,
    TRUE,
    'Proton Pump Inhibitor',
    'Headache, abdominal pain, nausea',
    'Hypersensitivity to omeprazole',
    250,
    75,
    0.28,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "C"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440305'::uuid,
    'MED-005',
    'Ibuprofen',
    'Advil',
    '00573-0166-40',
    '200mg',
    'Tablet',
    'Oral',
    'Wyeth',
    'BATCH-005-2024',
    '2025-12-31'::date,
    15.0,
    25.0,
    'Store at room temperature, keep in dry place',
    FALSE,
    FALSE,
    TRUE,
    'NSAID',
    'Upset stomach, heartburn, dizziness',
    'Allergy to aspirin or NSAIDs, active peptic ulcer',
    500,
    200,
    0.15,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "C"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440306'::uuid,
    'MED-006',
    'Amoxicillin Trihydrate',
    'Amoxil',
    '00093-2213-06',
    '500mg',
    'Capsule',
    'Oral',
    'GlaxoSmithKline',
    'BATCH-006-2024',
    '2025-11-30'::date,
    20.0,
    25.0,
    'Store at room temperature, keep in tight container',
    FALSE,
    TRUE,
    FALSE,
    'Antibiotic',
    'Nausea, vomiting, rash, diarrhea',
    'Allergy to penicillins or cephalosporins, mononucleosis',
    400,
    100,
    0.42,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "B"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440307'::uuid,
    'MED-007',
    'Metformin Hydrochloride',
    'Glucophage',
    '00064-1833-05',
    '500mg',
    'Tablet',
    'Oral',
    'Bristol-Myers Squibb',
    'BATCH-007-2024',
    '2026-05-31'::date,
    15.0,
    25.0,
    'Store at room temperature',
    FALSE,
    TRUE,
    FALSE,
    'Antidiabetic',
    'Gastrointestinal upset, vitamin B12 deficiency',
    'Renal impairment, acute illness',
    600,
    150,
    0.38,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "B"}'::jsonb
),
(
    '550e8400-e29b-41d4-a716-446655440308'::uuid,
    'MED-008',
    'Aspirin',
    'Bayer',
    '00006-0016-89',
    '325mg',
    'Tablet',
    'Oral',
    'Bayer',
    'BATCH-008-2024',
    '2025-08-31'::date,
    15.0,
    25.0,
    'Store in cool, dry place',
    FALSE,
    FALSE,
    TRUE,
    'Analgesic, Antiplatelet',
    'Upset stomach, increased bleeding risk',
    'Allergy to aspirin, active bleeding, peptic ulcer',
    1000,
    300,
    0.10,
    TRUE,
    '{"contraceptive": false, "pregnancy_category": "C", "third_trimester_warning": true}'::jsonb
);


-- ============================================================================
-- SECTION 6: PRESCRIPTION DATA
-- ============================================================================

INSERT INTO prescriptions (
    prescription_id,
    prescription_code,
    patient_id,
    doctor_id,
    status,
    prescription_date,
    start_date,
    end_date,
    approved_by,
    approved_at,
    clinical_notes,
    instructions_to_patient,
    is_active
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440401'::uuid,
    'RX-001',
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    'APPROVED',
    CURRENT_DATE - 5,
    CURRENT_DATE - 5,
    CURRENT_DATE + 55,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '4 days',
    'Patient with hypertension. Monitor BP regularly. Adjust if needed.',
    'Take one tablet by mouth once daily in the morning',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440402'::uuid,
    'RX-002',
    '550e8400-e29b-41d4-a716-446655440202'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    'APPROVED',
    CURRENT_DATE - 10,
    CURRENT_DATE - 10,
    CURRENT_DATE + 50,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '9 days',
    'Hypertension management with ACE inhibitor',
    'Take one tablet by mouth once daily, preferably in the morning',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440403'::uuid,
    'RX-003',
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    'APPROVED',
    CURRENT_DATE - 2,
    CURRENT_DATE - 2,
    CURRENT_DATE + 98,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    'Cholesterol management. Fasting lipid panel in 6 weeks.',
    'Take one tablet by mouth once daily in the evening. Avoid grapefruit juice.',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440404'::uuid,
    'RX-004',
    '550e8400-e29b-41d4-a716-446655440204'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    'APPROVED',
    CURRENT_DATE - 3,
    CURRENT_DATE - 3,
    CURRENT_DATE + 27,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '2 days',
    'Acute gastroesophageal reflux disease. Take for 4 weeks.',
    'Take one capsule by mouth once daily, 30 minutes before breakfast',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440405'::uuid,
    'RX-005',
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    'APPROVED',
    CURRENT_DATE - 1,
    CURRENT_DATE - 1,
    CURRENT_DATE + 5,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    CURRENT_TIMESTAMP,
    'Post-operative pain management. Short-term use only.',
    'Take one tablet by mouth every 4-6 hours as needed for pain. Do not exceed 3200mg per day.',
    TRUE
);


-- ============================================================================
-- SECTION 7: PRESCRIPTION ITEMS (MEDICATIONS)
-- ============================================================================

INSERT INTO prescription_items (
    prescription_item_id,
    prescription_id,
    medication_id,
    quantity,
    frequency,
    dosage_amount,
    duration_days,
    special_instructions,
    can_refill,
    max_refills,
    is_dispensed,
    dispensed_date
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440501'::uuid,
    '550e8400-e29b-41d4-a716-446655440401'::uuid,
    '550e8400-e29b-41d4-a716-446655440301'::uuid,
    30,
    'ONCE_DAILY',
    50.0,
    60,
    'Take in morning, check pulse regularly',
    TRUE,
    11,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '4 days'
),
(
    '550e8400-e29b-41d4-a716-446655440502'::uuid,
    '550e8400-e29b-41d4-a716-446655440402'::uuid,
    '550e8400-e29b-41d4-a716-446655440302'::uuid,
    30,
    'ONCE_DAILY',
    10.0,
    60,
    'May cause persistent dry cough - contact if severe',
    TRUE,
    11,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '9 days'
),
(
    '550e8400-e29b-41d4-a716-446655440503'::uuid,
    '550e8400-e29b-41d4-a716-446655440403'::uuid,
    '550e8400-e29b-41d4-a716-446655440303'::uuid,
    30,
    'ONCE_DAILY',
    20.0,
    100,
    'Take in evening. Avoid grapefruit juice.',
    TRUE,
    11,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '1 day'
),
(
    '550e8400-e29b-41d4-a716-446655440504'::uuid,
    '550e8400-e29b-41d4-a716-446655440404'::uuid,
    '550e8400-e29b-41d4-a716-446655440304'::uuid,
    28,
    'ONCE_DAILY',
    20.0,
    28,
    'Take 30 minutes before breakfast',
    FALSE,
    0,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '2 days'
),
(
    '550e8400-e29b-41d4-a716-446655440505'::uuid,
    '550e8400-e29b-41d4-a716-446655440405'::uuid,
    '550e8400-e29b-41d4-a716-446655440305'::uuid,
    20,
    'EVERY_4_HOURS',
    200.0,
    7,
    'Take with food. May cause stomach upset.',
    FALSE,
    0,
    FALSE,
    NULL
);


-- ============================================================================
-- SECTION 8: APPOINTMENT DATA
-- ============================================================================

INSERT INTO appointments (
    appointment_id,
    appointment_code,
    patient_id,
    doctor_id,
    hospital_id,
    appointment_date,
    appointment_start_time,
    appointment_end_time,
    appointment_type,
    chief_complaint,
    status,
    is_confirmed,
    confirmed_at,
    is_active
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440601'::uuid,
    'APT-001',
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE + 7,
    '09:00:00'::time,
    '09:30:00'::time,
    'Cardiology Consultation',
    'Hypertension follow-up',
    'SCHEDULED',
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440602'::uuid,
    'APT-002',
    '550e8400-e29b-41d4-a716-446655440202'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE + 3,
    '10:00:00'::time,
    '10:30:00'::time,
    'Cardiology Consultation',
    'Chest pain evaluation',
    'CONFIRMED',
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440603'::uuid,
    'APT-003',
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE + 5,
    '14:00:00'::time,
    '14:30:00'::time,
    'GI Consultation',
    'Gastroesophageal reflux disease',
    'SCHEDULED',
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440604'::uuid,
    'APT-004',
    '550e8400-e29b-41d4-a716-446655440204'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE + 2,
    '11:00:00'::time,
    '11:45:00'::time,
    'GI Consultation',
    'Stomach pain and bloating',
    'CONFIRMED',
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440605'::uuid,
    'APT-005',
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE + 1,
    '15:30:00'::time,
    '16:00:00'::time,
    'Orthopedic Follow-up',
    'Post-operative knee check',
    'SCHEDULED',
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440606'::uuid,
    'APT-006',
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE - 7,
    '09:00:00'::time,
    '09:30:00'::time,
    'Cardiology Consultation',
    'Regular check-up',
    'COMPLETED',
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '7 days',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440607'::uuid,
    'APT-007',
    '550e8400-e29b-41d4-a716-446655440202'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    CURRENT_DATE - 14,
    '10:00:00'::time,
    '10:30:00'::time,
    'Cardiology Consultation',
    'Blood pressure monitoring',
    'COMPLETED',
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '14 days',
    TRUE
);


-- ============================================================================
-- SECTION 9: APPOINTMENT NOTES
-- ============================================================================

INSERT INTO appointment_notes (
    appointment_note_id,
    appointment_id,
    doctor_id,
    vital_signs,
    chief_complaint_detailed,
    physical_examination,
    assessment_and_plan,
    diagnosis_primary,
    is_finalized
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440701'::uuid,
    '550e8400-e29b-41d4-a716-446655440606'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '{"BP": "138/85 mmHg", "HR": 72, "Temp": "98.6F", "RR": 16, "Weight": 185}'::jsonb,
    'Patient presents for routine cardiac follow-up. Denies chest pain or dyspnea.',
    'Regular sinus rhythm. No murmurs. Lungs clear to auscultation.',
    'Hypertension well-controlled on current medication. Continue Metoprolol 50mg daily. Recheck BP at home weekly.',
    'Hypertension - controlled',
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440702'::uuid,
    '550e8400-e29b-41d4-a716-446655440607'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '{"BP": "140/88 mmHg", "HR": 70, "Temp": "98.4F", "RR": 16, "Weight": 184}'::jsonb,
    'Patient with history of hypertension presents for monitoring. Compliant with medications.',
    'Cardiovascular: Regular rate and rhythm, no significant murmurs. Lungs: Clear bilaterally.',
    'Continue current antihypertensive regimen. Lifestyle modifications advised. Follow-up in 6 weeks.',
    'Hypertension - stable',
    TRUE
);


-- ============================================================================
-- SECTION 10: DOCUMENT DATA
-- ============================================================================

INSERT INTO documents (
    document_id,
    document_code,
    patient_id,
    doctor_id,
    hospital_id,
    appointment_id,
    document_type,
    title,
    description,
    file_path,
    file_name,
    file_size_bytes,
    file_mime_type,
    document_date,
    received_date,
    is_confidential,
    requires_signature,
    is_signed,
    is_active
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440801'::uuid,
    'DOC-001',
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    '550e8400-e29b-41d4-a716-446655440606'::uuid,
    'MEDICAL_REPORT',
    'Cardiology Evaluation Report',
    'Complete cardiac examination and assessment report',
    '/documents/2024/01/cardiology_report_001.pdf',
    'cardiology_report_001.pdf',
    245680,
    'application/pdf',
    CURRENT_DATE - 7,
    CURRENT_TIMESTAMP - INTERVAL '7 days',
    TRUE,
    TRUE,
    TRUE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440802'::uuid,
    'DOC-002',
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    NULL,
    'LAB_RESULT',
    'Lipid Panel Results',
    'Blood work results - Lipid panel comprehensive analysis',
    '/documents/2024/01/lab_results_lipid_001.pdf',
    'lab_results_lipid_001.pdf',
    125430,
    'application/pdf',
    CURRENT_DATE - 3,
    CURRENT_TIMESTAMP - INTERVAL '2 days',
    TRUE,
    FALSE,
    FALSE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440803'::uuid,
    'DOC-003',
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    NULL,
    'OPERATION_NOTE',
    'Surgical Operation Note',
    'Complete surgical documentation and post-operative instructions',
    '/documents/2024/01/operation_note_knee_001.pdf',
    'operation_note_knee_001.pdf',
    356890,
    'application/pdf',
    CURRENT_DATE - 15,
    CURRENT_TIMESTAMP - INTERVAL '15 days',
    TRUE,
    TRUE,
    TRUE,
    TRUE
);


-- ============================================================================
-- SECTION 11: TIMELINE EVENTS
-- ============================================================================

INSERT INTO timeline_events (
    timeline_event_id,
    patient_id,
    doctor_id,
    hospital_id,
    event_type,
    event_title,
    event_description,
    event_date,
    event_data,
    is_visible
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440901'::uuid,
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'APPOINTMENT',
    'Cardiology Appointment Completed',
    'Regular follow-up appointment with Dr. Sarah Johnson',
    CURRENT_TIMESTAMP - INTERVAL '7 days',
    '{"appointment_id": "550e8400-e29b-41d4-a716-446655440606", "outcome": "stable", "notes": "BP controlled"}'::jsonb,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440902'::uuid,
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'PRESCRIPTION',
    'New Prescription Created',
    'Atorvastatin for cholesterol management',
    CURRENT_TIMESTAMP - INTERVAL '2 days',
    '{"prescription_id": "550e8400-e29b-41d4-a716-446655440403", "medication": "Atorvastatin", "status": "approved"}'::jsonb,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440903'::uuid,
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    '550e8400-e29b-41d4-a716-446655440001'::uuid,
    'SURGERY',
    'Post-operative Follow-up',
    'Knee surgery post-operative check',
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    '{"surgery_type": "knee_arthroscopy", "status": "healing_well", "restrictions": "no_heavy_lifting_for_6_weeks"}'::jsonb,
    TRUE
);


-- ============================================================================
-- SECTION 12: NOTIFICATIONS
-- ============================================================================

INSERT INTO notifications (
    notification_id,
    patient_id,
    doctor_id,
    notification_type,
    title,
    message,
    related_entity_type,
    related_entity_id,
    is_sent,
    sent_at,
    is_read,
    in_app,
    email_sent,
    created_at
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440a01'::uuid,
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    NULL,
    'APPOINTMENT_REMINDER',
    'Appointment Reminder',
    'You have a cardiology appointment scheduled for ' || (CURRENT_DATE + 7) || ' at 09:00 AM',
    'APPOINTMENT',
    '550e8400-e29b-41d4-a716-446655440601'::uuid,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '1 day',
    FALSE,
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP - INTERVAL '1 day'
),
(
    '550e8400-e29b-41d4-a716-446655440a02'::uuid,
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    NULL,
    'PRESCRIPTION_READY',
    'Prescription Ready for Pickup',
    'Your prescription for Atorvastatin is ready to pick up at the pharmacy',
    'PRESCRIPTION',
    '550e8400-e29b-41d4-a716-446655440403'::uuid,
    TRUE,
    CURRENT_TIMESTAMP,
    FALSE,
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP
),
(
    '550e8400-e29b-41d4-a716-446655440a03'::uuid,
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    NULL,
    'APPOINTMENT_CONFIRMED',
    'Appointment Confirmed',
    'Your post-operative check appointment has been confirmed',
    'APPOINTMENT',
    '550e8400-e29b-41d4-a716-446655440605'::uuid,
    TRUE,
    CURRENT_TIMESTAMP,
    TRUE,
    TRUE,
    FALSE,
    CURRENT_TIMESTAMP
);


-- ============================================================================
-- SECTION 13: REMINDERS
-- ============================================================================

INSERT INTO reminders (
    reminder_id,
    patient_id,
    doctor_id,
    appointment_id,
    prescription_id,
    title,
    description,
    reminder_date_time,
    repeat_type,
    is_active,
    notify_via_email,
    notify_via_push
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440b01'::uuid,
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    NULL,
    '550e8400-e29b-41d4-a716-446655440601'::uuid,
    NULL,
    'Upcoming Appointment Reminder',
    'Reminder for your cardiology appointment',
    CURRENT_TIMESTAMP + INTERVAL '7 days - 1 hour',
    'ONCE',
    TRUE,
    TRUE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440b02'::uuid,
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    NULL,
    NULL,
    '550e8400-e29b-41d4-a716-446655440401'::uuid,
    'Daily Medication Reminder',
    'Time to take your Metoprolol',
    CURRENT_TIMESTAMP,
    'DAILY',
    TRUE,
    FALSE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440b03'::uuid,
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    NULL,
    NULL,
    '550e8400-e29b-41d4-a716-446655440403'::uuid,
    'Medication Refill Reminder',
    'Your Atorvastatin prescription will expire in 2 weeks',
    CURRENT_TIMESTAMP + INTERVAL '14 days',
    'ONCE',
    TRUE,
    TRUE,
    FALSE
);


-- ============================================================================
-- SECTION 14: CONSENT RECORDS
-- ============================================================================

INSERT INTO consent_records (
    consent_id,
    consent_code,
    patient_id,
    obtained_by,
    consent_type,
    consent_description,
    consent_date,
    status,
    scope_data_collection,
    scope_data_processing,
    scope_data_sharing,
    scope_research,
    is_active
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440c01'::uuid,
    'CONSENT-001',
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    'Medical Treatment',
    'Patient consent for medical treatment and examination',
    CURRENT_TIMESTAMP,
    'GIVEN',
    TRUE,
    TRUE,
    FALSE,
    FALSE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440c02'::uuid,
    'CONSENT-002',
    '550e8400-e29b-41d4-a716-446655440203'::uuid,
    '550e8400-e29b-41d4-a716-446655440102'::uuid,
    'Data Processing',
    'Patient consent for processing health data',
    CURRENT_TIMESTAMP - INTERVAL '30 days',
    'GIVEN',
    TRUE,
    TRUE,
    TRUE,
    FALSE,
    TRUE
),
(
    '550e8400-e29b-41d4-a716-446655440c03'::uuid,
    'CONSENT-003',
    '550e8400-e29b-41d4-a716-446655440205'::uuid,
    '550e8400-e29b-41d4-a716-446655440103'::uuid,
    'Research Participation',
    'Patient consent to participate in clinical research study',
    CURRENT_TIMESTAMP - INTERVAL '60 days',
    'GIVEN',
    TRUE,
    TRUE,
    FALSE,
    TRUE,
    TRUE
);


-- ============================================================================
-- SECTION 15: AI SUMMARIES
-- ============================================================================

INSERT INTO ai_summaries (
    ai_summary_id,
    patient_id,
    doctor_id,
    appointment_id,
    summary_type,
    title,
    content,
    key_findings,
    recommendations,
    ai_model_name,
    ai_model_version,
    confidence_score,
    is_reviewed,
    reviewed_by,
    reviewed_at,
    is_approved,
    approved_by,
    approved_at
) VALUES
(
    '550e8400-e29b-41d4-a716-446655440d01'::uuid,
    '550e8400-e29b-41d4-a716-446655440201'::uuid,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    '550e8400-e29b-41d4-a716-446655440606'::uuid,
    'Clinical Summary',
    'Patient Cardiology Assessment Summary',
    'Patient presents with well-controlled hypertension. Vital signs stable. Cardiac examination shows regular rate and rhythm without significant murmurs. Current medication regimen effective.',
    ARRAY['BP well-controlled on Metoprolol', 'No cardiac murmurs detected', 'EKG normal', 'Patient compliant with medications'],
    ARRAY['Continue current antihypertensive regimen', 'Recheck BP weekly at home', 'Follow-up appointment in 6 weeks', 'Consider stress test if symptoms develop'],
    'MediAI-Clinical-v2.1',
    '2.1.0',
    0.94,
    TRUE,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '6 days',
    TRUE,
    '550e8400-e29b-41d4-a716-446655440101'::uuid,
    CURRENT_TIMESTAMP - INTERVAL '5 days'
);


-- ============================================================================
-- SECTION 16: COMPLETION SUMMARY
-- ============================================================================

-- Display record counts
DO $$
BEGIN
    RAISE NOTICE 'MediFlow Seed Data Successfully Inserted!';
    RAISE NOTICE '-------------------------------------------';
    RAISE NOTICE 'Hospitals: %', (SELECT COUNT(*) FROM hospitals);
    RAISE NOTICE 'Doctors: %', (SELECT COUNT(*) FROM doctors);
    RAISE NOTICE 'Patients: %', (SELECT COUNT(*) FROM patients);
    RAISE NOTICE 'Medications: %', (SELECT COUNT(*) FROM medications);
    RAISE NOTICE 'Prescriptions: %', (SELECT COUNT(*) FROM prescriptions);
    RAISE NOTICE 'Prescription Items: %', (SELECT COUNT(*) FROM prescription_items);
    RAISE NOTICE 'Appointments: %', (SELECT COUNT(*) FROM appointments);
    RAISE NOTICE 'Appointment Notes: %', (SELECT COUNT(*) FROM appointment_notes);
    RAISE NOTICE 'Documents: %', (SELECT COUNT(*) FROM documents);
    RAISE NOTICE 'Timeline Events: %', (SELECT COUNT(*) FROM timeline_events);
    RAISE NOTICE 'Notifications: %', (SELECT COUNT(*) FROM notifications);
    RAISE NOTICE 'Reminders: %', (SELECT COUNT(*) FROM reminders);
    RAISE NOTICE 'Consent Records: %', (SELECT COUNT(*) FROM consent_records);
    RAISE NOTICE 'AI Summaries: %', (SELECT COUNT(*) FROM ai_summaries);
    RAISE NOTICE '-------------------------------------------';
    RAISE NOTICE 'Seed data insertion complete!';
END $$;

-- ============================================================================
-- END OF SEED DATA FILE
-- ============================================================================
