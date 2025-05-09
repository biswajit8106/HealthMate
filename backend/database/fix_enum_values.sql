-- Update enum values in medication_reminders table
UPDATE medication_reminders
SET status = 'TAKEN'
WHERE status = 'Taken';

UPDATE medication_reminders
SET status = 'NOT_TAKEN'
WHERE status IN ('Not_taken', 'Not_Taken', 'Not taken', 'not_taken', 'not taken');

UPDATE medication_reminders
SET status = 'MISSED'
WHERE status = 'Missed';

UPDATE medication_reminders
SET status = 'SKIPPED'
WHERE status = 'Skipped';

-- Update enum values in reminder_history table
UPDATE reminder_history
SET status = 'TAKEN'
WHERE status = 'Taken';

UPDATE reminder_history
SET status = 'NOT_TAKEN'
WHERE status IN ('Not_taken', 'Not_Taken', 'Not taken', 'not_taken', 'not taken');

UPDATE reminder_history
SET status = 'MISSED'
WHERE status = 'Missed';

UPDATE reminder_history
SET status = 'SKIPPED'
WHERE status = 'Skipped';
