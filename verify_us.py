from app import db, User,app

def verify_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_verified = True
        db.session.commit()
        print(f"User '{username}' is now verified.")
    else:
        print(f"No user found with username '{username}'.")

if __name__ == "__main__":
    with app.app_context():
        username_input = input("Enter username to verify: ")
        verify_user_by_username(username_input)