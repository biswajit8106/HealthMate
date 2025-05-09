### Plan:
1. **Modify `Navbar.js`:**
   - Update the click handler for the "Symptom Checker" link to check if the user is logged in.
   - If the user is not logged in, trigger the login modal instead of navigating to the "Symptom Checker" page.
   - If the user is logged in, allow navigation to the "Symptom Checker" page.

2. **Update `LoginModal.js`:**
   - Modify the `handleSubmit` function to redirect the user to the "Symptom Checker" page after a successful login instead of the home page.

### Follow-up Steps:
- Test the changes to ensure that the login modal appears when the user is not logged in and that the user is redirected to the "Symptom Checker" page after a successful login.
