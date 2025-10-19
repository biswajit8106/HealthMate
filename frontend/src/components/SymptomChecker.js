import React, { useState, useEffect } from 'react';
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
    const [readOnlyFields, setReadOnlyFields] = useState(true); // New state for read-only toggle
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch user info from backend session API
        axios.get('http://localhost:5000/api/user/session', { withCredentials: true })
            .then(response => {
                if (response.data.logged_in) {
                    const user = response.data.user;
                    setName(user.name || '');
                    setGender(user.gender || '');
                    setAge(user.age || '');
                    setReadOnlyFields(true); // Set fields to read-only based on user preference
                }
            })
            .catch(error => {
                console.error('Error fetching user session:', error);
            });
    }, []);

    const symptomList = [
        'Body_Pain',
        'Burning_Sensation',
        'Itching',
        'Excessive_Hunger',
        'Frequent_Urination',
        'Eye_Problems',
        'Joint_Pain',
        'Numbness',
        'Weight_Gain',
        'Weight_Loss',
        'Fatigue',
        'Shortness_of_Breath',
        'Breast_Enlargement',
        'Memory_Loss',
        'Speech_Difficulty',
        'Hearing_Difficulty',
        'Sleep_Issues',
        'Cognitive_Decline',
        'Dizziness',
        'Loss_of_Balance',
        'Slurred_Speech',
        'Facial_Droop',
        'High_Fever',
        'Pain_Behind_Eyes',
        'Loss_of_Appetite',
        'Rash',
        'Anal_Burning',
        'Bloody_Stool',
        'Anal_Pain',
        'Painful_Defecation',
        'Rapid_Pulse',
        'Loss_of_Consciousness',
        'Vomiting_Blood',
        'Abdominal_Bloating',
        'Abdominal_Pain',
        'Acidity',
        'Burning_Urination',
        'Tongue_Ulcer',
        'Bloody_Diarrhea',
        'Indigestion',
        'Vomiting',
        'Weakness',
        'Small_Nail_Pits',
        'Dry_Skin',
        'Prickly_Heat_Rash',
        'Blisters',
        'Fever',
        'Difficulty_in_Defecation',
        'Abnormal_Menstruation',
        'Family_History',
        'Dehydration',
        'Red_Eyes',
        'Watery_Eyes',
        'Eye_Discomfort',
        'Swollen_Eyelids',
        'Eye_Pain',
        'Sticky_Eyelids',
        'Burning_Eyes',
        'Yellow_Eyes',
        'Muscle_Pain',
        'Headache',
        'Back_Pain',
        'Dry_skin',
        'Joint_Pain.1',
        'Swollen',
        'Inability_to_walk',
        'Diarrhea',
        'Chest_Pain',
        'Dislike_of_food',
        'Coughing_Blood',
        'Phlegm',
        'Cough',
        'Feel_Cold',
        'Nausea',
        'Rapid_Breathing',
        'Heaviness',
        'Chest_Pain_With_Pressure',
        'Sweating',
        'Head_Scratching',
        'Hearing_Loss',
        'Hearing Difficulty',
        'Tremors_in_hands_and_feet',
        'Strong_hands_and_feet',
        'Blurred_Vision',
        'Paralysis',
        'Poor_night_vision',
        'Double_vision',
        'Color_Fading_Appearance',
        'Sensitivity_to_Light',
        'Muscle_Weakness',
        'Tingling_in_hands_and_feet',
        'Weak_Joints',
        'Tooth_Brittle',
        'Brittle_Bones',
        'Bones_of_the_legs_curved_like_bow',
        'Sore_Throat',
        'Seizures',
        'Excessive_Salivation',
        'Difficulty_Swallowing',
        'Insomnia',
        'Coma',
        'Fear_of_the_Wind',
        'Cold',
        'Paralysed_Body',
        'Muscle_Weakness.1',
        'Pain_in_hands_and_feet',
        'Hard_Muscle',
        'Temporary_Distraction',
        'Deja_vu',
        'Anxiety',
        'Sudden_Uncontrolled_Electrical_Disturbances_in_the_brain',
        'Fainting',
        'Talking_Nonsense',
        'Hypertension',
        'Sweating.1',
        'Ear_Fluid_Drainage',
        'Ear_Pain',
        'Swollen_Tongue',
        'Soft_Tongue',
        'Sore_Tongue',
        'Pale_Spots_On_Skin',
        'Small_Boils_On_the_Skin',
        'Crippled',
        'Heartburn',
        'Bloating',
        'Anorexia',
        'Throbbing_around_the_lips',
        'Blisters_on_the_lips',
        'Blisters.1',
        'Open_Wound',
        'Genital_Pain',
        'Vaginal_Discharge',
        'Sore_Throat.1',
        'Bleeding_from_the_Navel',
        'Swollen_Ankles',
        'Swelling_of_the_Joints',
        'Excessive_Bleeding',
        'Sore',
        'Dark_Gums',
        'Brittle_Gums',
        'Gums_Swell',
        'Gingivitis',
        'Gum_Abscess',
        'Hole_in_the_Gum',
        'Loose_Tooth',
        'Pus_from_the_Gums',
        'Corneal_Damage',
        'Mucus_in_the_throat',
        'Loss_of_sense_of_smell_and_taste',
        'Body_Getting_Cold',
        'Coughing_With_Mucus',
        'Bladder_Insufficiency',
        'Inability_to_Focus',
        'Mood_Swings',
        'Enlarged_Liver',
        'Yellow_Skin',
        'Joint_Pain.2',
        'Dark_Colored_Urine',
        'Clay_Colored_Stool',
        'Neck_Pain',
        'Neck_Swelling',
        'Stiff_Neck',
        'Nasal_Inflammation',
        'Constipation',
        'Pulse_Rate_Decrease',
        'Continuous_Sneezing',
        'Cold.1',
        'Blood_Clot',
        'Pus_Filled_Pimple',
        'Rashes',
        'Mental_Anxiety',
        'White_Spots_on_Mouth'
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
        const lowerSymptoms = symptoms.map(s => s.toLowerCase());
        const invalidSymptoms = lowerSymptoms.filter(sym => !validSymptomSet.has(sym));

        if (invalidSymptoms.length > 0) {
            setError(`Invalid symptoms: ${invalidSymptoms.join(', ')}`);
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post('http://localhost:5000/predict', {
                symptoms: symptoms,
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
                    symptoms: symptoms,
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

                //  Save report to backend
await axios.post('http://localhost:5000/report/save', fullResult, { withCredentials: true });
                //  Navigate to Report page
                navigate('/report', { state: fullResult });
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
                    readOnly={readOnlyFields}
                />

                <div>
                    <label>
                        <input
                            type="radio"
                            value="Male"
                            checked={gender === 'Male'}
                            onChange={(e) => setGender(e.target.value)}
                            disabled={readOnlyFields}
                        /> Male
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="Female"
                            checked={gender === 'Female'}
                            onChange={(e) => setGender(e.target.value)}
                            disabled={readOnlyFields}
                        /> Female
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="Other"
                            checked={gender === 'Other'}
                            onChange={(e) => setGender(e.target.value)}
                            disabled={readOnlyFields}
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
                    readOnly={readOnlyFields}
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
                <p>Please enter at least two symptoms for better prediction.</p>

                <button type="button" onClick={handleAddSymptomInput}>Add Symptom</button>
                <button type="submit">Check Symptoms</button>
            </form>

            {loading && <p style={{ color: 'blue' }}>Checking symptoms, please wait...</p>}
            {error && <p className="error" style={{ color: 'red' }}>{error}</p>}

            {result && result.confidence < 0.09 && (
                <div style={{
                    backgroundColor: '#fff3cd',
                    color: '#856404',
                    padding: '15px',
                    border: '1px solid #ffeeba',
                    borderRadius: '6px',
                    fontWeight: 'bold',
                    marginTop: '10px'
                }}>
                    Low confidence prediction ({(result.confidence * 100).toFixed(2)}%). Consider providing more symptoms for better accuracy.
                </div>
            )}
        </div>
    );
};

export default SymptomChecker;
