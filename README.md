# Internship Project: Bookstore Management System

## Project Description
Welcome to the Internship Project for creating a comprehensive Bookstore Management System. This project aims to develop an efficient platform for managing books, user memberships, and book reservations.

## Key Features
1. **Book Management:**
   - Perform CRUD operations on books with detailed attributes such as title, authors, genre, publication date, ISBN, and price.
   - Utilize a NoSQL database for storing books, enhancing performance.
   - Create a powerful API with advanced filtering, pagination, sorting, and text search capabilities.

2. **User Management:**
   - Establish user profiles including names, last names, membership types, and expiration dates.
   - Enable OTP-based login for enhanced security, with circuit breaker mechanism for SMS services.
   - Allow users to purchase special memberships, obtaining JWT tokens for authenticated access.
   - Implement token revocation and OTP throttling to maintain security standards.

3. **Book Reservation:**
   - Empower users to reserve books for a maximum of 1 week.
   - Grant special members extended 2-week free book reservations; regular members pay per day.
   - Offer discounts and free reservations for regular members based on usage patterns.
   - Utilize optimistic locking to avoid race conditions during book reservations.
   - Display a personalized list of reserved books for each user.

## Getting Started
Follow these steps to get started with the Bookstore Management System:

1. **Clone the Repository:**
   Clone this repository to your local machine using the following command:


```bash


git clone https://github.com/your-username/bookstore-management.git


```

2. **Install Dependencies:**
Navigate to the project directory and set up the required dependencies. Run the following commands:

```bash

cd bookstore-management
pip install -r requirements.txt

```

3. **Database Setup:**
Configure your database settings in the `settings.py` file. Migrate the database using:

```bash

python manage.py makemigrations
python manage.py migrate

```


4. **Run the Project:**
Launch the development server with the following command:

```bash

python manage.py runserver


```

Access the project through your web browser at `http://localhost:8000/`.

5. **Access APIs:**
Explore the powerful APIs by navigating to `http://localhost:8000/api/`.

## Dependencies
- Django, Django REST framework
- Kafka or RabbitMQ (for transitioning to NoSQL)
- Kavenegar and Signal libraries (for SMS services)
