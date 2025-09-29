# TODO: Fix Symptom Checker Confidence Issue

## Tasks
- [x] Fix ml_model.py to use dataset1.csv instead of Training.csv
- [x] Remove confidence check in backend/routes/symptom_checker.py to allow predictions with low confidence, matching notebook behavior
- [x] Remove confidence check in frontend/src/components/SymptomChecker.js to allow navigation to report page regardless of confidence
- [ ] Test the symptom checker endpoint to ensure predictions are returned
