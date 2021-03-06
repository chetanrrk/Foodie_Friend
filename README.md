# Welcome to the Foodie's Friend Application.

This application uses Django and zomato API to locate the restaurants serving your desired cusines near you. 
The application automatically detects the current location and displays desired choices.


## How to run locally

`git clone` https://github.com/chetanrrk/Foodie_Friend.

`cd foodie_friend`.

Create a virtual environment by running `py -3 -m venv venv`.

### Activate the virtual environment by running:

  * on Linux/Mac: `source venv/bin/activate`

  * on Windows: `venv\Scripts\activate`

Install the necessary python packages by running `pip install -r requirements.txt`.

Run the migrations by running `./manage.py makemigrations` or `python manage.py makemigrations`.

Run the migrations by running `./manage.py migrate` or `python manage.py migrate`.

Run the migrations by running `./manage.py collectstatic` or `python manage.py collectstatic`.

Start the web server by running `./manage.py runserver` or `python manage.py runserver`.

To see the website, go to `http://localhost:8000`.

## To change the Layout and Theme:

* `foodie_friend_app\templates\foodie_friend_app`    
    * `index.html` is used as the home page inheriting the `base.html`.
    
 - Change the Template pages as required to customize.
