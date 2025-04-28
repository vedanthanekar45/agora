# LibLend

Liblend will be an open-source, scalable and flexible digital lending system that'll work on top of already available digtial asset accessing platforms. The project is specifically designed to enabl libraries around the world to a "Controlled Digital Lending" of the books they already own.

# Project Overview

Libraries often face significant barriers when trying to make the transition from print to digital media. The issues include restrictive licensing models imposed by publishers and the lack of technical infrastructure. This system provides a solution to these challenges by enabling libraries to lend digital versions of books while ensuring compliance with the **Controlled Digital Lending (CDL)** model.

**The main goal of this project is to create an open-source lending system** that can be integrated into any library's environment, allowing them to lend digital copies in compliance with legal restrictions.

## Features

- **Book Management**: Add, update, and manage books in the library's collection.
- **Lending Management**: Borrow and return books while ensuring the number of available digital copies never exceeds the physical copies owned by the library.
- **Digital Lending**: Use Readium Web SDK and LCP (Licensed Content Protection) DRM to deliver secure digital books to users.
- **User Management**: Support for library patrons who can borrow books, track their loans, and renew books within the allowed period.
- **RESTful API**: A complete REST API for managing books, users, and lending operations, making it easy to integrate with other systems like Koha, FOLIO, or existing library infrastructure.

## System Design

The system is designed as a **RESTful API**, with a clear separation of concerns between the core backend and any frontend applications that might be built on top of it. Libraries can implement their own user authentication and integrate the lending system into their existing workflows.

## Installation

### Requirements

- Python 3.x
- Django 4.x
- PostgreSQL 12+
- Readium Web SDK (for DRM)

### Steps to Install

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vedanthanekar45/liblend.git
   cd liblend

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Set up the database:**

   - Create a PostgreSQL database and configure the database settings in settings.py.
   - Run migrations to set up the database tables:
     ```bash
     python manage.py migrate

5. **Create a superuser to access the admin panel:**

   ```bash
   pyhton manage.py createsuperuser

6. **Run the development server:**

   ```bash
   python manage.py runserver
