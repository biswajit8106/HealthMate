from models.user_model import User
from models.disease_model import Disease

# Test User Creation
user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
user.save()

# Test Disease Creation
disease = Disease(name='Flu', description='Common viral infection', symptoms='Fever, Cough', treatment='Rest and hydration')
disease.save()

# Fetch and print all users and diseases
print("All Users:", User.get_all_users())
print("All Diseases:", Disease.get_all_diseases())
