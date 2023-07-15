
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
import random

from .models import Post, Comments

fake = Faker()

def create_fake_data():
    # Create fake users
    users = []
    for _ in range(5):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, email=email, password=password)
        users.append(user)

        # Create fake posts
    for _ in range(10):
        title = ' '.join(fake.words(nb=random.randint(1, 5)))  # Limit title to 1-5 words
        author = random.choice(users)
        body = ' '.join(fake.words(nb=random.randint(10, 50)))  # Limit body to 10-50 words
        publish = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
        status = random.choice(['draft', 'published'])
        post = Post.objects.create(title=title, author=author, body=body, publish=publish, status=status)

        # Create fake comments for each post
        for _ in range(3):
            name = fake.name()
            email = fake.email()
            comment_body = fake.paragraph()
            comment = Comments.objects.create(post=post, name=name, email=email, body=comment_body)


# Call the function to create fake data
create_fake_data()
