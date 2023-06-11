UPDATE episodes_target
SET status = '{{ params.status }}'
WHERE status = 'preprocessed'