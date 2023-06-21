
# Flask Reddit Dashboard

  

https://github.com/Batuhanaydnn/Reddit-Api-/assets/128238475/88402c8b-a392-4068-abcd-bb0cf74451bd

  

Flask Reddit Dashboard is a web application that provides a user-friendly interface to display and filter Reddit posts. It allows users to register, login, and view posts from the subreddit 'netsec'. The application utilizes the Flask framework, SQLAlchemy for database management, and the Python Reddit API Wrapper (praw) to interact with the Reddit API.

  
  
  

## Features

  

- User Registration: Users can create an account by providing their name, email, and password. The registration data is stored securely in a SQLite database.

  

- User Login: Registered users can log in to their accounts using their email and password. The application verifies the user's credentials against the stored data in the database.

  

- User Dashboard: After logging in, users are directed to their personalized dashboard. The dashboard displays both the filtered posts from the 'netsec' subreddit and all the posts available in the database. Users can filter the posts based on a provided text filter.

  

- Reddit API Integration: The application connects to the Reddit API using praw. It crawls the 'netsec' subreddit for new posts and adds them to the database. The application also retrieves post information such as title, content, upvotes, comment count, and media links.

  

- RESTful API Endpoints: The application provides several RESTful API endpoints to access post data. Users can retrieve all posts, filter posts based on selected parameters, and filter posts based on upvotes.

  

- Notes: You may not be able to access the site structure directly because some files are private. (see. .gitignore)

  

## Technologies Used

  

- Flask: A micro web framework for Python used to develop the web application.

  

- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library used for database management.

  

- praw: A Python wrapper for the Reddit API, allowing interaction with Reddit's features and data.

  

- SQLite: A lightweight database engine used to store user and post data.

  

## Installation

  

To run the Flask Reddit Dashboard locally, follow these steps:

  

1. Clone the repository: `git clone https://github.com/yourusername/flask-reddit-dashboard.git`

  

2. Install the required dependencies: `pip install -r requirements.txt`

  

3. Set up the database by running the following commands:

  

4. Run the application: `python app.py`

  

5. Open your web browser and access the application at `http://localhost:5000`

  

### or

  

## Docker Installation

1. Build the Docker image by running the following command in the terminal, while being in the same directory as the Dockerfile

```

docker build -t myflaskapp .

```

2. Run the Docker container with the following command

```

docker run -p 5000:5000 myflaskapp

  

# This will start the Flask application inside the Docker container and map port 5000 of the container to port 5000 of your local machine.

```

  
  

3. Access your Flask application by visiting http://localhost:5000 in your web browser.

  

## API Documentation

  

The Flask Reddit Dashboard provides the following API endpoints:

  

- `GET /api/allposts/`: Retrieves all posts in the database.

  

- `GET /api/selectedposts/?name=<parameter>&value=<value>`: Retrieves posts based on a selected parameter (e.g., title, content).

  

- `GET /api/upvotes/?value=<value>`: Retrieves posts with upvotes greater than the specified value.

  

For detailed information on using these API endpoints, please refer to the API documentation.

  

## Contributions

  

Contributions to the Flask Reddit Dashboard project are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the GitHub repository.

  

## License

  

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Batuhanaydnn/flask-reddit-dashboard/blob/main/LICENSE) file for more details.

  

## Acknowledgements

  

The Flask Reddit Dashboard project acknowledges the usage of the following third-party libraries and APIs:

  

- Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)

  

- SQLAlchemy: [https://www.sqlalchemy.org](https://www.sqlalchemy.org)

  

- praw: [https://praw.readthedocs.io](https://praw.readthedocs.io)

  

- Reddit API: [https://www.reddit.com/dev/api/](https://www.reddit.com/dev/api/)

  
  

## Class Diagram

  

### User Model Class Diagram

```

+----------------+

| User |

+----------------+

| - id: Integer |

| - name: String |

| - email: String |

| - password: String |

| - created_at: DateTime |

+----------------+

| __repr__() |

+----------------+

```

### Post Model Class Diagram

```

+----------------+

| Post |

+----------------+

| - id: Integer |

| - title: String |

| - content: Text |

| - created_at: DateTime |

| - user_id: Integer |

| - upvotes: Integer |

| - comment_count: Integer |

| - video_link: String |

| - image_link: String |

+----------------+

| __repr__() |

+----------------+

```

## Explanation of the Code

```

1. The code imports necessary modules and libraries, including Flask, SQLAlchemy, datetime, and praw (Python Reddit API Wrapper).

2. The Flask application is created, and the secret key and database configuration are set up.

3. Two models are defined using SQLAlchemy: User and Post. These models represent the tables in the database.

4. Several routes are defined using the `@app.route` decorator to handle different HTTP requests.

- The '/' route represents the home page.

- The '/register' route handles registration of new users.

- The '/login' route handles user login.

- The '/dashboard' route represents the user dashboard, where posts are displayed.

- The '/api/allposts/' route returns all posts as JSON.

- The '/api/selectedposts/' route returns posts based on a selected parameter.

- The '/api/upvotes' route returns posts with upvotes greater than a specified value.

- The '/logout' route logs out the user by removing the user_id from the session.

5. The `home()` function renders the home.html template.

6. The `register()` function handles user registration by adding a new user to the database.

7. The `login()` function handles user login by checking the email and password against the database.

8. The `dashboard()` function displays the user dashboard, which includes posts. It retrieves posts from the database and filters them based on the provided filter text. It also interacts with the Reddit API to crawl new posts and add them to the database.

9. The `api_all_posts()` function retrieves all posts from the database and returns them as JSON.

10. The `api_selected_posts()` function retrieves posts based on a selected parameter (name and value) and returns them as JSON.

11. The `api_upvotes()` function retrieves posts with upvotes greater than a specified value and returns them as JSON.

12. The `logout()` function removes the user_id from the session to log out the user.

13. The `if __name__ == '__main__':` block creates the database tables using `db.create_all()` and starts the Flask application.

```

  

## 🌟 Welcome to Batuhan's Coding Wonderland! 🚀

  

If you've stumbled upon this enchanting corner of the coding universe, get ready for an extraordinary adventure! 🎩✨

  

👋 Greetings, fellow travelers! I'm Muhammed Batuhan Aydın, your guide through this whimsical world of code. As a passionate developer and explorer of digital realms, I invite you to join me on an exhilarating journey through the realms of technology and innovation. 🌌💻

  

Within these virtual landscapes, we'll traverse the valleys of Python, scale the mountains of Flask, and dive deep into the mysterious depths of databases. Together, we'll unravel the secrets of web development and create amazing applications that bring dreams to life. 🌐🔧

  

But this is not just another mundane coding experience. Along the way, we'll sprinkle our journey with a touch of magic and fun! Expect surprises, hidden easter eggs, and interactive challenges that will test your coding prowess and spark joy in your heart. 🎉✨

  

Oh, and did I mention that we have a secret language? ✨✨ The language of creativity, innovation, and problem-solving. Together, we'll speak this language fluently and conjure remarkable solutions to any challenge that crosses our path.

  

So, fasten your seatbelts and prepare to be enchanted! 🌟🔮 Let's embark on this extraordinary adventure, where learning becomes an exhilarating quest and every line of code reveals a new chapter in our story.

  

Remember, in Batuhan's Coding Wonderland, there are no limits to what we can achieve. Let's dream big, code boldly, and create wonders that leave a lasting mark on this digital realm. 🚀💡

  

🌈 Are you ready to embrace the magic of coding? Then join me, and let's set forth into this incredible journey together! Follow me on Twitter [@Telumak](https://twitter.com/Telumak) and connect with me on LinkedIn [Batuhan Aydın](https://www.linkedin.com/in/batuhan-aydinn/) to stay updated with the latest adventures.

  

May the code be with you! 🌟💻✨

  

Kind Regards

  

Muhammed Batuhan Aydın

  

Note: I guess you'll get me on internship now and I'm too lazy to use the blueprint structure, so I'm sorry about that, I'll update it after a 3-day project.
<<<<<<< HEAD
Last Note: Bak bu türkçe abi canlıya almaya çok üşendim gerekliyse yaparım. Ben kaçtım bye
=======
>>>>>>> 2094c9a82df18b2a3f1aba96d21613095b10e403
