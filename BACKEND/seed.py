from datetime import datetime
from app import app
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like, Save, Flag

# Define the seed data
def seed_data():
    with app.app_context():
        print("Start seeding...")

        # Clear existing records
        Like.query.delete()
        Comment.query.delete()
        Follow.query.delete()
        Save.query.delete()
        Flag.query.delete()
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
                media_url="https://example.com/sunset.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="New Smartphone Release",
                description="Check out the features of this new smartphone.",
                media_url="https://example.com/video.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Mountain Hike",
                description="Amazing view from the top of the mountain.",
                media_url="https://example.com/mountain.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Calm Forest",
                description="A walk in the peaceful forest.",
                media_url="https://example.com/forest.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Tech Conference 2024",
                description="Highlights from the tech conference.",
                media_url="https://example.com/conference.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="New AI Breakthrough",
                description="Exploring the latest in AI technology.",
                media_url="https://example.com/ai.mp4",
                media_type="video"
            ),
            # Add more cores to reach 20 in total
            Core(
                hashtag_id=hashtags[0].id,
                title="Ocean Waves",
                description="Relaxing sound of ocean waves.",
                media_url="https://example.com/ocean.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Night Sky",
                description="Starry night sky captured during my camping trip.",
                media_url="https://example.com/night_sky.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Robotics Revolution",
                description="The latest advancements in robotics.",
                media_url="https://example.com/robotics.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Quantum Computing Explained",
                description="An introduction to quantum computing.",
                media_url="https://example.com/quantum.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Wildlife Safari",
                description="A glimpse into the wildlife during my safari trip.",
                media_url="https://example.com/safari.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Spring Blossoms",
                description="Beautiful spring flowers in full bloom.",
                media_url="https://example.com/blossoms.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Space Exploration",
                description="The future of space travel.",
                media_url="https://example.com/space.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Cybersecurity Trends",
                description="Emerging trends in cybersecurity.",
                media_url="https://example.com/cybersecurity.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Autumn Leaves",
                description="The beauty of autumn leaves falling.",
                media_url="https://example.com/autumn.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[0].id,
                title="Desert Dunes",
                description="Mesmerizing sand dunes in the desert.",
                media_url="https://example.com/desert.jpg",
                media_type="image"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Blockchain Explained",
                description="Understanding the fundamentals of blockchain.",
                media_url="https://example.com/blockchain.mp4",
                media_type="video"
            ),
            Core(
                hashtag_id=hashtags[1].id,
                title="Virtual Reality Innovations",
                description="The latest innovations in virtual reality.",
                media_url="https://example.com/vr.mp4",
                media_type="video"
            )
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
