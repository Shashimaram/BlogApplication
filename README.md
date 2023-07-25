## BlogApplication

## Introduction

"My Blog" is a simple blog application developed as part of my learning journey with Django. It allows users to publish and read blog posts, add comments, and view similar posts filtered by tags. The application is built using Python, Django, HTML, CSS, and jQuery."

## Features

- List all published blog posts
- View individual blog post with comments
- Add comments to blog posts
- Display similar posts based on tags
- Create new blog posts asynchronously with status messages
- Show the five latest blog posts
- Generate fake data using Faker for testing and development purposes

## Setup and Installation

To clone and run the "My Blog" app locally, follow these steps:

1. Clone the repository:

git clone https://github.com/Shashimaram/BlogApplication.git

2.  Install dependencies:

pip install -r requirements.txt

3. Run Application:

python3 manage.py runserver

4.Add fake data 

python3 manage.py shell
from faker import create_fake_data
create_fake_data()

## Usage:

- Visit the homepage to see a list of all published blog posts.
- Click on a blog post title to view the complete blog post along with comments.
- Add comments to a blog post by filling out the comment form at the bottom of the post detail page.
- Use the sidebar to view similar posts filtered by tags.
- To create a new blog post, click the "New Post" button located at the bottom right corner of the page. Save the post asynchronously, and status messages will be displayed within the page.
-if needed add fake data to Database by running faker.py 
