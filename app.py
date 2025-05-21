import streamlit as st
from models.user import User
from models.passport import Passport
from datetime import datetime
from database import init_db
init_db()


# Background color change
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    </style>
""", unsafe_allow_html=True)


def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if User.authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in!")
        else:
            st.error("Invalid username or password")

def register():
    st.title("📝 Register")

    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            success, msg = User.register(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

def passport_analyzer():
    st.title("🛂 Passport Analyzer")

    passport_num = st.text_input("Enter Passport Number (e.g. P<GBR1234567)")

    if passport_num:
        passport = Passport(passport_num)

        if not Passport.exists_in_db(passport_num):
            st.error("❌ Passport number not found in database.")
        else:
            st.success("✅ Passport number exists in database.")
            st.success(f"Masked Passport Number: {passport.masked()}")
            st.write("Country Code:", passport.get_country_code())
            st.write("Country Name:", passport.get_country_name())

            expiry_date = st.date_input("Enter Passport Expiry Date")

            if st.button("Check Expiry"):
                if expiry_date < datetime.today().date():
                    st.error("❌ Passport has expired.")
                else:
                    st.success("✅ Passport is still valid.")

            if st.button("Generate Report"):
                report = f"""
Passport Number: {passport.masked()}
Country Code: {passport.get_country_code()}
Country Name: {passport.get_country_name()}
Expiry Date: {expiry_date}
"""
                with open("report.txt", "w") as file:
                    file.write(report)
                st.download_button("📥 Download Report", open("report.txt", "rb"), file_name="passport_report.txt")

def generate_passport():
    st.title("🆕 Generate Passport")

    number = st.text_input("Passport Number (e.g. P<PAK1234567)")
    name = st.text_input("Full Name")
    country = st.text_input("Country")
    expiry_date = st.date_input("Expiry Date")

    if st.button("Save to Database"):
        passport = Passport(
            number,
            name,
            expiry_date.strftime("%Y-%m-%d"),
            country
        )
        success, msg = passport.add_to_db()
        if success:
            st.success("✅ Passport generated and saved.")
        else:
            st.error(f"❌ {msg}")



def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    menu = ["Login", "Register", "Generate Passport"]
    if st.session_state.logged_in:
        menu.append("Logout")

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        if not st.session_state.logged_in:
            login()
        else:
            st.warning(f"Already logged in as {st.session_state.username}")
            passport_analyzer()

    elif choice == "Register":
        if not st.session_state.logged_in:
            register()
        else:
            st.warning(f"Already logged in as {st.session_state.username}")
            passport_analyzer()
    
    elif choice == "Generate Passport":
       if st.session_state.logged_in:
        generate_passport()
       else:
        st.warning("Please login to access passport generator.")



    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully")

if __name__ == "__main__":
    main()
