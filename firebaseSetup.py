import streamlit as st
import pyrebase


# hash_config {
#   algorithm: SCRYPT,
#   base64_signer_key: qygZ6DK/OWzwF9sU0yPGUpd3dAzrTiSkLv01D75DmIuQaYFZgzC8OHfEz19PbZE79VLjDwAFqb4BOClfecTkPg==,
#   base64_salt_separator: Bw==,
#   rounds: 8,
#   mem_cost: 14,
# }
import pyrebase
import streamlit as st
from faker import Faker
from pybloom_live import ScalableBloomFilter

# Assuming you've stored your config in environment variables or set them directly here
firebaseConfig = {
    "apiKey": "AIzaSyAxFhMJQRp1pS9tpg77VbGa4aO2_9eEwdk",
    "authDomain": "tradewise-92bb9.firebaseapp.com",
    "databaseURL": "https://tradewise-92bb9.firebaseio.com",  # Example URL
    "projectId": "tradewise-92bb9",
    "storageBucket": "tradewise-92bb9.appspot.com",
    "messagingSenderId": "30883923905",
    "appId": "1:30883923905:web:xxxxxxx",
    "measurementId": "G-xxxxxxxx"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

fake = Faker()
bloom_filter = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)

# Generate fake user data and add email addresses to the Bloom filter
for _ in range(10000):
    email = fake.email()
    bloom_filter.add(email)

# def populate_bloom_filter():
#     # Code to fetch all user emails from Firebase and add to the Bloom filter
#     all_users = auth.list_users()
#     for user in all_users:
#         bloom_filter.add(user.email)

# Call this function when your app starts
# populate_bloom_filter()


def sign_up():
    st.subheader("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if email:  # Check if email field is not empty
            # Check if the email might exist in the Bloom filter
            if email in bloom_filter:
                st.error("Email may already exist. Please use a different email.")
                st.write("Debug: Email is potentially in the Bloom filter.")
            else:
                # If not in Bloom filter, attempt to create the user in Firebase
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("You have successfully created an account")
                    bloom_filter.add(email)  # Add email to Bloom filter
                    st.write("Debug: Email added to the Bloom filter.")
                except Exception as e:
                    # Improved error handling
                    error_json = json.loads(e.args[1])
                    error_message = error_json['error']['message']
                    st.error(f"Failed to create user account: {error_message}")
        else:
            st.error("Please enter an email address.")

def login():
    st.subheader("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            st.session_state['user'] = user
            st.success("Logged in successfully")
        except:
            st.error("Failed to login, check your email and password")

def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "SignUp":
        sign_up()
    elif choice == "Login":
        login()
    else:
        st.subheader("Home Page")

    if 'user' in st.session_state:
        st.sidebar.success("Logged In as {}".format(st.session_state['user']['email']))
        if st.sidebar.button("Logout"):
            del st.session_state['user']
            st.experimental_rerun()

if __name__ == '__main__':
    main()
