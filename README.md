# Welcome to the Foodie's Friend Application.

This application Django and zomato API to locate the restaurants near you based on distance and price.
The code automatically detects the current location (by default) or takes a adress to display desired choices.


## How to run locally

`git clone` this repository.

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
