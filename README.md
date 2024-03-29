# Job Listing Portal using Django and MongoDB

This is a web application that allows companies to post job listings and students to apply for these job opportunities. The application is built using the Django framework and MongoDB as the database.

## Features

- Companies can post job listings and manage applications from students
- Students can create an account, search for job opportunities, and apply for them
- Admins can approve or decline job applications
- The application uses MongoDB as the database to store job listings, student accounts, and job applications
- The application is secured using Django's built-in authentication system

## Getting Started

To run this application locally, you need to have Python and MongoDB installed on your machine. Follow these steps:

Make sure to install django, pymongo and before starting the following steps , run models.py to get access to the admin portal

1. Clone the repository to your local machine.
2. Install the requirements using `pip install -r requirements.txt`.
3. Use pymongo to connect with database in models.py (use your own connection string from MongoDB Atlas)
4. Run the server using `python manage.py runserver`.
5. Access the application in your browser at `http://localhost:8000`.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for new features, please create an issue or submit a pull request.

## License

This application is licensed under the MIT license. See the `LICENSE` file for more details.

## Credits

This project was created by Tejas Solanke, as a personal project.
