from datetime import datetime
from app import app
from models import db, User, Message, Hashtag, Core, Follow, Comment, Like, Save, Flag

# Define the seed data
def seed_data():
    with app.app_context():
        print("Start seeding...")

        try:
            # Clear existing records
            models = [Like, Comment, Follow, Save, Flag, Core, Hashtag, Message, User]
            for model in models:
                model.query.delete()
            
            print("Existing records deleted")

            # Seed Users
            print("Seeding users")
            users = [
                User(username="johndoe", email="johndoe@example.com", password="password123"),
                User(username="janedoe", email="janedoe@example.com", password="password456"),
                User(username="alice", email="alice@example.com", password="password789"),
                User(username="bob", email="bob@example.com", password="password321")
            ]
            db.session.add_all(users)
            db.session.commit()
            print("Users seeded")

            # Seed Hashtags
            print("Seeding hashtags")
            hashtags = [
                Hashtag(user_id=users[0].id, name="Nature", description="Photos and posts about nature."),
                Hashtag(user_id=users[1].id, name="Technology", description="Latest tech news and gadgets."),
                Hashtag(user_id=users[2].id, name="Travel", description="Adventures and travel experiences."),
                Hashtag(user_id=users[3].id, name="Food", description="Delicious recipes and food experiences."),
                Hashtag(user_id=users[0].id, name="Fitness", description="Health and fitness tips."),
                Hashtag(user_id=users[1].id, name="Music", description="Latest music trends and recommendations."),
                Hashtag(user_id=users[2].id, name="Books", description="Book reviews and literary discussions."),
                Hashtag(user_id=users[3].id, name="Movies", description="Movie reviews and recommendations."),
                Hashtag(user_id=users[0].id, name="Photography", description="Beautiful photos and photography tips."),
                Hashtag(user_id=users[1].id, name="Gaming", description="Gaming news and reviews."),
                Hashtag(user_id=users[2].id, name="DIY", description="Do-it-yourself projects and crafts."),
                Hashtag(user_id=users[3].id, name="Science", description="Latest developments in science.")
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
                # Add more cores to cover new hashtags...
                Core(
                    hashtag_id=hashtags[2].id,
                    title="Eiffel Tower in Paris",
                    description="A breathtaking view of the Eiffel Tower.",
                    media_url="https://example.com/eiffel_tower.jpg",
                    media_type="image"
                ),
                Core(
                    hashtag_id=hashtags[3].id,
                    title="Gourmet Pasta",
                    description="A delicious gourmet pasta recipe.",
                    media_url="https://example.com/pasta.jpg",
                    media_type="image"
                ),
                Core(
                    hashtag_id=hashtags[4].id,
                    title="Morning Workout",
                    description="A great start to the day with a morning workout.",
                    media_url="https://example.com/workout.mp4",
                    media_type="video"
                ),
                Core(
                    hashtag_id=hashtags[5].id,
                    title="New Album Release",
                    description="Check out the latest album from your favorite artist.",
                    media_url="https://example.com/album.mp3",
                    media_type="audio"
                ),
                Core(
                    hashtag_id=hashtags[6].id,
                    title="Book Review: 'The Great Gatsby'",
                    description="A detailed review of 'The Great Gatsby'.",
                    media_url="https://example.com/gatsby.jpg",
                    media_type="image"
                ),
                Core(
                    hashtag_id=hashtags[7].id,
                    title="Top 10 Movies of 2024",
                    description="A list of the top 10 movies released in 2024.",
                    media_url="https://example.com/movies.mp4",
                    media_type="video"
                ),
                Core(
                    hashtag_id=hashtags[8].id,
                    title="Nature Photography Tips",
                    description="Tips for capturing stunning nature photos.",
                    media_url="https://example.com/photography_tips.jpg",
                    media_type="image"
                ),
                Core(
                    hashtag_id=hashtags[9].id,
                    title="Best Gaming Gear of 2024",
                    description="A review of the best gaming gear released in 2024.",
                    media_url="https://example.com/gaming_gear.mp4",
                    media_type="video"
                ),
                Core(
                    hashtag_id=hashtags[10].id,
                    title="DIY Home Decor",
                    description="Creative DIY home decor ideas.",
                    media_url="https://example.com/diy_home_decor.jpg",
                    media_type="image"
                ),
                Core(
                    hashtag_id=hashtags[11].id,
                    title="Space Exploration Milestones",
                    description="Key milestones in space exploration history.",
                    media_url="https://example.com/space_exploration.mp4",
                    media_type="video"
                ),
                # Continue adding more cores as needed
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
        
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    seed_data()