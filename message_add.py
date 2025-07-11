from app import db,app
from app import ChatMessage

with app.app_context():
    message = ChatMessage(sender_id=1, receiver_id=2, content="Hello, how are you?")
    db.session.add(message)
    db.session.commit()
    print("Added message  successfully!")