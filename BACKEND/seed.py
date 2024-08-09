from datetime import datetime
from app import app
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like

# Define the seed data
def seed_data():
    with app.app_context():
        print("Start seeding...")

        # Clear existing records
        Like.query.delete()
        Comment.query.delete()
        Follow.query.delete()
        Core.query.delete()
        Hashtag.query.delete()
        Message.query.delete()
        User.query.delete()

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

        # Seed Core
        print("Seeding core")
        cores = [
            Core(
                hashtag_id=hashtags[0].id,
                title="Beautiful Sunset",
                description="Captured this stunning sunset yesterday.",
                image_url="https://example.com/sunset.jpg",
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="New Smartphone Release",
                description="Check out the features of this new smartphone.",
                link_url="https://example.com/video.mp4",
            ),
        ]
        db.session.add_all(cores)
        db.session.commit()
        print("Core seeded")

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
