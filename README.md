# StudyBud

StudyBud is a study assistant application designed to help students form groups and learn with their peers and chat with each other

## Installation and Setup

--> Clone the repository:

```bash
git clone https://github.com/h-lakshman/StudyBud.git
```

--> Move into the directory where we have the project files :
 ```bash
 cd StudyBud
```
--> Create a virtual environment :
```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv envname
```

--> Activate the virtual environment :
```bash
envname\scripts\activate
```
--> Install the requirements :
```bash
pip install -r requirements.txt
```
##Running the App
--> To run the App, we use :
```bash
python manage.py runserver
```
###Then, the development server will be started at http://127.0.0.1:8000/

##App Preview
## Image Grid Example

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
  <div>
    <img src="image1.jpg" alt="Image 1" width="300" height="200">
    <h3>Home Feed</h3>
  </div>
  <div>
    <img src="image2.jpg" alt="Image 2" width="300" height="200">
    <h3>Room Conversations</h3>
  </div>
</div>





