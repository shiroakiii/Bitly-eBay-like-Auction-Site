# Bidly: eBay-like Auction Site

This project is an e-commerce auction web application built with **Django**, designed to replicate key features of platforms like **eBay**. Users can register, create listings, place bids, comment, manage a watchlist, and explore auctions by categories.

## 📌 Features

- **User Authentication**  
  Register, login, logout functionality using Django's built-in auth system.

- **Create Listings**  
  Users can create auction listings with title, description, starting bid, optional image URL, and category.

- **View Listings**  
  Homepage shows all listings with details: title, price, image, and description.

- **Listing Detail Page**  
  - Bid on items (with validation)
  - Add/remove from watchlist
  - View and add comments
  - Close auction (listing owner only)
  - Auction winner display when closed

- **Watchlist**  
  Logged-in users can view and manage their personal watchlist.

- **Categories**  
  Browse auctions by category. 

- **Django Admin**  
  Admins can manage users, listings, bids, and comments.

## 🧠 Project Structure
```
commerce/
├── auctions/
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── templates/
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── commerce/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── db.sqlite3
└── manage.py
```

## 🛠️ Technologies Used

- Python 3
- Django
- SQLite3
- HTML/CSS (Bootstrap optional)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/commerce.git
cd commerce
````

### 2. Install dependencies (in a virtual environment recommended)

```bash
pip install django
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the app.

## 💡 Future Improvements

* Add search and filtering functionality
* Enhance bidding with real-time updates (e.g., using WebSockets)
* Improve UI/UX with responsive design
* Email notifications for winning bids

## 📄 License

This project is part of **CS50’s Web Programming with Python and JavaScript** by Harvard University. Educational use only.

## 🙋‍♀️ Author

**Erika Falculan Velasquez**
📧 [erika.velasquez.cs@gmail.com](mailto:erika.velasquez.cs@gmail.com)
📍 Caloocan City, Philippines
