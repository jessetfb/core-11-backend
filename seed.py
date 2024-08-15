from datetime import datetime
from app import app
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like, Save, Flag
import requests

# Define the API URL for fetching core data
API_URL = "https://api.unsplash.com/photos/random"  # Adjust to fetch random photos or other endpoints as needed

# Your Unsplash access key
UNSPLASH_ACCESS_KEY = "oScHgmeQXdftW1nga3W3LYqUKhMa-qXYEx2CToooPe8"  # Replace with your actual Unsplash API access key

def seed_data():
    with app.app_context():
        print("Start seeding...")

        # Clear existing records
        db.session.query(Like).delete()
        db.session.query(Comment).delete()
        db.session.query(Follow).delete()
        db.session.query(Save).delete()
        db.session.query(Flag).delete()
        db.session.query(Core).delete()
        db.session.query(Hashtag).delete()
        db.session.query(Message).delete()
        db.session.query(User).delete()

        db.session.commit()  # Commit deletion
        print("Existing records deleted")

        # Seed Users
        print("Seeding users")
        users = [
            User(username="johndoe", email="johndoe@example.com", password="password123"),
            User(username="janedoe", email="janedoe@example.com", password="password456")
        ]
        db.session.add_all(users)
        db.session.commit()
        print("Users seeded")

        # Seed Hashtags
        print("Seeding hashtags")
        hashtags = [
            Hashtag(user_id=users[0].id, name="Nature", description="Photos and posts about nature."),
            Hashtag(user_id=users[1].id, name="Technology", description="Latest tech news and gadgets.")
        ]
        db.session.add_all(hashtags)
        db.session.commit()
        print("Hashtags seeded")

        # Fetch and Seed Core Data from Unsplash API
        print("Fetching core data from Unsplash API")
        cores = []  # Initialize cores list
        for hashtag in hashtags:
            response = requests.get(API_URL, headers={
                "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
                "Content-Type": "application/json"
            }, params={
                "query": hashtag.name,  # Fetch photos related to the hashtag
                "count": 100              # Number of photos to fetch
            })

            if response.status_code == 200:
                core_data = response.json()
                print(f"Seeding core data for hashtag '{hashtag.name}'")
                for item in core_data:
                    core = Core(
                        hashtag_id=hashtag.id,
                        title=item['alt_description'] or "Untitled",
                        description=item['description'] or item['alt_description'] or "No description",
                        media_url=item['urls']['regular'],  # Adjust as needed
                        media_type="image"  # Assuming images only for now
                    )
                    cores.append(core)
                db.session.add_all(cores)
                db.session.commit()
                print(f"Core data for '{hashtag.name}' seeded")
            else:
                print(f"Failed to fetch core data for '{hashtag.name}'. Status code: {response.status_code}")

        # Seed Messages
        print("Seeding messages")
        messages = [
            Message(sender_id=users[0].id, recipient_id=users[1].id, content="Hello, how are you?", created_at=datetime.now()),
            Message(sender_id=users[1].id, recipient_id=users[0].id, content="I'm good, thanks!", created_at=datetime.now())
        ]
        db.session.add_all(messages)
        db.session.commit()
        print("Messages seeded")

        # Seed Follows
        print("Seeding follows")
        follows = [
            Follow(follower_id=users[0].id, followee_id=users[1].id, created_at=datetime.now()),
            Follow(follower_id=users[1].id, followee_id=users[0].id, created_at=datetime.now())
        ]
        db.session.add_all(follows)
        db.session.commit()
        print("Follows seeded")

        # Check if cores have been populated before seeding comments and likes
        if not cores:
            print("No core data available for seeding comments and likes.")
            return

        # Seed Comments
        print("Seeding comments")
        comments = [
            Comment(user_id=users[0].id, core_id=cores[0].id, content="Amazing photo!", created_at=datetime.now()),
            Comment(user_id=users[1].id, core_id=cores[1].id, content="Can't wait to try this phone.", created_at=datetime.now())
        ]
        db.session.add_all(comments)
        db.session.commit()
        print("Comments seeded")

        # Seed Likes
        print("Seeding likes")
        likes = [
            Like(user_id=users[0].id, core_id=cores[0].id, created_at=datetime.now()),
            Like(user_id=users[1].id, core_id=cores[1].id, created_at=datetime.now())
        ]
        db.session.add_all(likes)
        db.session.commit()
        print("Likes seeded")

        print("Database seeded successfully")

if __name__ == "__main__":
    seed_data()
