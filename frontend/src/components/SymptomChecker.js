import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../style/components/SymptomChecker.css';

const SymptomChecker = () => {
    const [name, setName] = useState('');
    const [gender, setGender] = useState('');
    const [age, setAge] = useState('');
    const [symptoms, setSymptoms] = useState([]);
    const [symptomInputs, setSymptomInputs] = useState(['']);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const symptomList = [
        "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing",
        "shivering", "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue",
        "muscle_wasting", "vomiting", "burning_micturition", "spotting_ urination", "fatigue",
        "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss",
        "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough",
        "high_fever", "sunken_eyes", "breathlessness", "sweating", "dehydration", "indigestion",
        "headache", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite",
        "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea",
        "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure",
        "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes", "malaise",
        "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes",
        "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs",
        "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool",
        "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", "obesity",
        "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid",
        "brittle_nails", "swollen_extremeties", "excessive_hunger", "extra_marital_contacts",
        "drying_and_tingling_lips", "slurred_speech", "knee_pain", "hip_joint_pain",
        "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness",
        "spinning_movements", "loss_of_balance", "unsteadiness", "weakness_of_one_body_side",
        "loss_of_smell", "bladder_discomfort", "foul_smell_of urine", "continuous_feel_of_urine",
        "passage_of_gases", "internal_itching", "toxic_look_(typhos)", "depression",
        "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain",
        "abnormal_menstruation", "dischromic _patches", "watering_from_eyes", "increased_appetite",
        "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration",
        "visual_disturbances", "receiving_blood_transfusion", "receiving_unsterile_injections",
        "coma", "stomach_bleeding", "distention_of_abdomen", "history_of_alcohol_consumption",
        "fluid_overload", "blood_in_sputum", "prominent_veins_on_calf", "palpitations",
        "painful_walking", "pus_filled_pimples", "blackheads", "scurring", "skin_peeling",
        "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister",
        "red_sore_around_nose", "yellow_crust_ooze",
    ];

    const handleSymptomChange = (index, value) => {
        const updatedInputs = [...symptomInputs];
        updatedInputs[index] = value;

        const filtered = updatedInputs.filter(
            (symptom, i) =>
                symptom.trim() !== '' &&
                updatedInputs.indexOf(symptom) === i
        );

        setSymptomInputs(updatedInputs);
        setSymptoms(filtered);
    };

    const handleAddSymptomInput = () => {
        setSymptomInputs([...symptomInputs, '']);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!name || !gender || !age) {
            setError('Please fill in all fields.');
            return;
        }

        if (symptoms.length < 2) {
            setError('Please provide at least two symptoms.');
            return;
        }

        const validSymptomSet = new Set(symptomList.map(sym => sym.toLowerCase()));
        const normalizedSymptoms = symptoms.map(s => s.toLowerCase());
        const invalidSymptoms = normalizedSymptoms.filter(sym => !validSymptomSet.has(sym));

        if (invalidSymptoms.length > 0) {
            setError(`Invalid symptoms: ${invalidSymptoms.join(', ')}`);
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post('http://localhost:5000/predict', {
                name,
                gender,
                age,
                symptoms: normalizedSymptoms,
            });
            setLoading(false);

            if (response.data) {
                const {
                    predicted_disease,
                    confidence,
                    description,
                    precautions = [],
                    medications = [],
                    diets = [],
                    workouts = []
                } = response.data;

                const fullResult = {
                    name,
                    age,
                    gender,
                    symptoms: normalizedSymptoms,
                    predicted_disease,
                    confidence,
                    description,
                    precautions,
                    medications,
                    diets,
                    workouts
                };

                setResult(fullResult);
                setError(null);

                if (fullResult.confidence >= 0.2) {
                    //  Save report to backend
await axios.post('http://localhost:5000/report/save', fullResult, { withCredentials: true });
                    //  Navigate to Report page
                    navigate('/report', { state: fullResult });
                } else {
                    setError('Insufficient confidence in prediction. Please provide more symptoms.');
                }
            } else {
                setError(response.data.error || 'Something went wrong!');
                setResult(null);
            }
        } catch (err) {
            setLoading(false);
            setError('Could not connect to the server.');
            setResult(null);
        }
    };

    return (
        <div className="symptom-checker">
            <h2>Symptom Diagnosis</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your name"
                    required
                />

                <div>
                    <label>
                        <input
                            type="radio"
                            value="Male"
                            checked={gender === 'Male'}
                            onChange={(e) => setGender(e.target.value)}
                        /> Male
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="Female"
                            checked={gender === 'Female'}
                            onChange={(e) => setGender(e.target.value)}
                        /> Female
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="Other"
                            checked={gender === 'Other'}
                            onChange={(e) => setGender(e.target.value)}
                        /> Other
                    </label>
                </div>

                <input
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    placeholder="Enter your age"
                    min="0"
                    max="120"
                    required
                />

                {symptomInputs.map((symptom, index) => (
                    <input
                        key={index}
                        type="text"
                        value={symptom}
                        onChange={(e) => handleSymptomChange(index, e.target.value)}
                        placeholder="Type a symptom"
                        list="symptom-suggestions"
                    />
                ))}

                <datalist id="symptom-suggestions">
                    {symptomList.map((symptom, index) => (
                        <option key={index} value={symptom} />
                    ))}
                </datalist>

                <button type="button" onClick={handleAddSymptomInput}>Add Symptom</button>
                <button type="submit">Check Symptoms</button>
            </form>

            {loading && <p style={{ color: 'blue' }}>Checking symptoms, please wait...</p>}
            {error && <p className="error" style={{ color: 'red' }}>{error}</p>}

            {result && result.confidence < 0.2 && (
                <div style={{
                    backgroundColor: '#fff3cd',
                    color: '#856404',
                    padding: '15px',
                    border: '1px solid #ffeeba',
                    borderRadius: '6px',
                    fontWeight: 'bold',
                    marginTop: '10px'
                }}>
                    ⚠️ Insufficient confidence in prediction. Please provide more symptoms.
                </div>
            )}
        </div>
    );
};

export default SymptomChecker;
