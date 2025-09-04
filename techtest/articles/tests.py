"""
Unit 10 Walk through 
Testing

Here we will learn how to perform testing in Django and learn the power of 
automated testing. We will build tests in both the Blog and Users apps.

- RUNNING TESTS FROM CLI

**To run all tests in both apps we use**
    python manage.py test

**To run all tests in a specific app we use**
python manage.py test (name_of_app)

    python manage.py test blog
    python manage.py test users

**To run all tests in a specific class in a test file we use**
python manage.py test blog.tests.classname

    python manage.py test blog.tests.PostModelTests
    python manage.py test blog.tests.PostViewsTests

**To run a single test in a specific class in a test file we use**
python manage.py test blog.tests.classname.test_method

    python manage.py test blog.tests.PostModelTests.test_post_content
    python manage.py test blog.tests.PostViewsTests.test_post_list_view
# 
# 

**************************BLOG APP TESTS***************************************

"""
# blog/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

"""

These lines import necessary classes and functions.

TestCase - is a class provided by Django's test framework which we'll use to create our test cases.
Client - is a class that acts as a dummy web browser for simulating GET and POST requests on a URL.
User - is Django’s default user model.
reverse - is a helper function to reverse resolve Django URLs.
Post - is a model class which we are going to test.

**PostModelTests class**

"""
class PostModelTests(TestCase):
"""
- Defines a new class PostModelTests which is a subclass of TestCase.

# 
# 

1.  setUpTestData class method
"""
@classmethod
def setUpTestData(cls):
    cls.user = User.objects.create_user(username='testuser', password='12345')
    cls.post = Post.objects.create(
        author=cls.user, 
        title='Test Post', 
        content='This is a test post'
    )
"""

- This class method is decorated with @classmethod indicating that it's a class method.

- setUpTestData is called once at the beginning of the test run for class-level setup.

- cls.user creates a user in the test database.

- cls.post creates a post in the test database associated with the user we just created.

# 
# 

2.  test_post_content method
"""
def test_post_content(self):
    post = Post.objects.get(id=1)
    expected_author = f'{post.author}'
    expected_title = f'{post.title}'
    expected_content = f'{post.content}'
    self.assertEqual(expected_author, 'testuser')
    self.assertEqual(expected_title, 'Test Post')
    self.assertEqual(expected_content, 'This is a test post')
"""

- This method tests the content of the Post created in setUpTestData.

- It retrieves a Post instance by its id.

- It then verifies that the author, title, and content match what was set up.

# 
# 

3.  test_post_str_method method
"""
def test_post_str_method(self):
    post = Post.objects.get(id=1)
    self.assertEqual(str(post), post.title)
"""

- This method tests the __str__ method of the Post model.

- It ensures that the string representation of a Post instance (str(post)) is the same as the post's title.

# 
# 

4.  test_get_absolute_url method
"""
def test_get_absolute_url(self):
    post = Post.objects.get(id=1)
    self.assertEqual(post.get_absolute_url(), reverse('post-detail', args=[post.id]))
"""

- This method tests the get_absolute_url method of the Post model.

- It ensures that the URL returned is what is expected by using reverse to generate the URL for the 'post-detail' view using the post's id.

# 
# 

**PostViewsTests class**

"""
class PostViewsTests(TestCase):
"""
This class contains tests for the views associated with the Post model.

5.  setUp method
"""
 def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.post = Post.objects.create(
        author=self.user, 
        title='Test Post', 
        content='This is a test post'
    )
"""

- This method sets up the data needed for the individual tests.

- A Client instance is created to simulate a browser.

- A User and Post instance are created for use in the upcoming tests.

# 
# 

6.  test_post_list_view method
"""
def test_post_list_view(self):
    url = reverse('blog-home')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This is a test post')
    self.assertTemplateUsed(response, 'blog/home.html')
"""

- This method tests the view for listing blog posts (home page).

- It uses reverse to find the URL named 'blog-home'.

- It simulates a GET request to that URL and checks that the response status is 200 (HTTP OK).

- It checks if the response contains certain text (to ensure the post is listed).

- It checks that the correct template is used to render the response.

# 
# 

7.  test_post_detail_view method
"""
def test_post_detail_view(self):
    url = reverse('post-detail', args=[self.post.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.post.title)
"""

- This method tests the view for displaying a single blog post detail.

- It reverses the 'post-detail' URL using the test post's id.

- It checks the response status and whether the response contains the post's title.

# 
# 

8.  test_create_post_view method
"""
def test_create_post_view(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('post-create'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

    response = self.client.post(reverse('post-create'), {
        'title': 'New title',
        'content': 'New text',
    })
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertTrue(Post.objects.filter(title='New title').exists())
"""

- This test checks the post creation view.

- It logs in the test user using the login method of the client.

- It retrieves the URL for the 'post-create' view and makes a GET request to check if the response 
  is successful and the correct template is used.

- It then makes a POST request to the same URL, simulating the creation of a new post with a title and content.

- It checks that the response status code is 302, which is expected on a successful post creation as the view should redirect.

- It verifies that a post with the title 'New title' now exists in the database.

# 
# 

9.  test_update_post_view method
"""
def test_update_post_view(self):
    self.client.login(username='testuser', password='12345')
    url = reverse('post-update', kwargs={'pk': self.post.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_form.html')

    response = self.client.post(url, {
        'title': 'Updated title',
        'content': 'Updated text',
    })
    self.post.refresh_from_db()
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertEqual(self.post.title, 'Updated title')
"""

- This test checks the post update view.

- After logging in the test user, it retrieves the URL for the 'post-update' 
 view using the test post's primary key.

- It makes a GET request to the update view and verifies the response and template.

- It then sends a POST request with updated title and content for the post.

- It refreshes the test post instance from the database and checks if the title has 
been updated as expected.

- It also checks that the response status code is 302 following the update.

# 
# 

10. test_delete_post_view method
"""
def test_delete_post_view(self):
    self.client.login(username='testuser', password='12345')
    url = reverse('post-delete', kwargs={'pk': self.post.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    response = self.client.post(url)
    self.assertEqual(response.status_code, 302)  # Redirect after POST
    self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
"""
- This test verifies the post deletion view.

- After logging in the test user, it retrieves the URL for the 'post-delete' 
  view using the test post's primary key.

- It makes a GET request to the delete view and checks the response status code and template.

- It then sends a POST request to actually perform the deletion

# 
# 

**************************USER APP TESTS***************************************

"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
"""

Heere we import the necessary imports to write test cases for Django forms and models 
related to user and profile functionality. 

- `from django.test import TestCase`:
   - This imports `TestCase` from Django's test framework. 
   `TestCase` is a subclass of `unittest.TestCase` that runs each test inside a transaction to provide isolation among tests.

- `from django.contrib.auth.models import User`:
   - This imports the User model from Django's built-in authentication system. 
   The User model is the default user account model that Django provides, which can be used to create, modify, and authenticate users.

- `from django.core.files.uploadedfile import SimpleUploadedFile`:
   - This imports `SimpleUploadedFile`, which is a class for creating in-memory uploaded file objects. 
   It is used in tests to simulate file uploads, such as profile images in this context.

- `from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm`:
   - This line imports specific form classes from the local `forms` module within the same Django app. 
   These forms are likely custom forms that inherit from Django's form classes and add specific 
   validation, fields, and functionality for user registration, user data updates, and profile updates.

- `from .models import Profile`:
   - This imports the `Profile` model from the local `models` module. 
   The `Profile` model is typically used to extend the default `User` model with additional information 
   (like a profile picture or bio) that isn't included in the default user model.

When writing tests, we use these imports to access the form and model classes you need to test. 
You can create instances of `User` and `Profile` for use in your tests, manipulate them through forms 
(like `UserRegisterForm`, `UserUpdateForm`, and `ProfileUpdateForm`), and create `SimpleUploadedFile` 
instances to simulate file uploads in your tests.

**UserFormsTests Class**

"""
class UserFormsTests(TestCase):
"""

- Defines a new class UserFormsTests which is a subclass of TestCase.

#
#

11. setUpTestData class method
"""
def setUp(self):
     # Set up a user and profile for the tests
    self.user = User.objects.create_user(username='testuser', password='12345')
    Profile.objects.get_or_create(user=self.user, defaults={'image': 'default.png'})
"""

- setUp is an instance method of the TestCase class that is called before every test function is executed.

- This method is used for setting up the test environment, which may include creating test records in the database.

- self.user creates a new user with the username 'testuser' and password '12345' in the test database for each test method.

- Profile.objects.get_or_create ensures a profile is associated with self.user. If the profile does not exist, 
  it creates one with the default image 'default.png'. If it exists, it will get the existing profile. 
  This happens before each test method runs.

#
#

12. test_user_register_form method
"""
def test_user_register_form(self):
    # Test user registration form with valid data
    form_data = {
        'username': 'newuser', 
        'email': 'newuser@example.com', 
        'password1': 'django1234', 
        'password2': 'django1234'
    }
    form = UserRegisterForm(data=form_data)
    self.assertTrue(form.is_valid())

"""

- This test function, `test_user_register_form`, is intended to validate the user registration form functionality.

- It begins by setting up a dictionary named `form_data` with keys for 'username', 'email', 'password1', and 'password2', 
  assigning them respective values that mimic what a user might enter in a registration form.

- A `UserRegisterForm` instance is created with `form_data` passed into it. 
  This simulates the form being filled out with the provided data.

- The test then calls `form.is_valid()`, which runs all the form's validation checks for the fields provided.

- The assertion `self.assertTrue(form.is_valid())` checks that the form is valid, meaning that all 
  the data provided meets the expected format and constraints defined in the `UserRegisterForm`. 
  If the form is not valid, the test will fail, indicating there is an issue with the form's validation logic or the test data provided.

#
#

13. test_user_update_form method
"""
def test_user_update_form(self):
    # Test user update form with valid data
    form_data = {
        'username': 'updateduser', 
        'email': 'updateduser@example.com'
    }
    form = UserUpdateForm(data=form_data, instance=self.user)
    self.assertTrue(form.is_valid())
    form.save()
    self.user.refresh_from_db()
    self.assertEqual(self.user.username, 'updateduser')
"""

- This test function, `test_user_update_form`, is meant to verify the functionality of the user update form.

- It starts by preparing a dictionary called `form_data` that contains key-value pairs for 'username' and 'email'. 

- The values 'updateduser' and 'updateduser@example.com' represent the new data that a user might enter to update their profile.

- The `UserUpdateForm` is then instantiated with the `form_data` and the current instance of `self.user`, 
  which was previously set up in the test environment. 

- This action simulates filling out the update form with new user data.

- The method `form.is_valid()` is invoked to run the form's validation routines for the provided fields.

- The test asserts that the form is valid by using `self.assertTrue(form.is_valid())`. 
  If the form's data doesn't conform to the validation rules, the test will fail, indicating a problem 
  with the form's validation logic or the test data itself.

- Upon validation, the form's `save()` method is called to commit the changes to the database.

- To ensure that the changes have indeed been made, `self.user.refresh_from_db()` 
  is called to update the `self.user` instance with the latest data from the database.

- Lastly, the test asserts that the user's username has been successfully updated to 'updateduser' with 
  `self.assertEqual(self.user.username, 'updateduser')`. 
  If the username has not been updated as expected, the test will fail, indicating an issue with 
  the form's save functionality or the test setup.

#
#

14. test_profile_update_with_invalid_image_format method
"""
def test_profile_update_with_invalid_image_format(self):
    # Test profile update with an invalid image format
    invalid_image_data = b'this is not real image data'
    invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
    form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
    self.assertFalse(form.is_valid())

"""

- The test function `test_profile_update_with_invalid_image_format` is designed to test the profile update functionality specifically in the scenario where an invalid image file is provided.
  
- `invalid_image_data` is a byte string that does not represent a valid image file; it's simply plain text that says 'this is not real image data'. 
   In a real image file, this data would be binary data representing image pixels.

- `invalid_image_file` is created using `SimpleUploadedFile`, a Django utility that mimics an uploaded file. 
   It is given a name 'new_image.txt', which implies a text file rather than an image, and the content type is set to 'text/plain', 
   further signifying that this is not an image file.

- The `ProfileUpdateForm` is then instantiated with the invalid file passed in the `files` dictionary, 
  which simulates the process of a user trying to upload a text file where an image is expected. 
  The `instance` argument is provided with `self.user.profile`, which ties the form to the specific profile instance associated with the test user.

- The form's validity is checked using `form.is_valid()`, which should return `False` because the uploaded file does not meet the requirements 
  for an image field (wrong format, wrong content type).

- `self.assertFalse(form.is_valid())` asserts that the form is indeed invalid. 
  If the form mistakenly considers this invalid file as valid, the test will fail, indicating a problem with the form's validation logic or the file handling in the application. 
  This test ensures that only proper image files can be uploaded to a user's profile.

#
#

15. test_profile_update_with_oversized_image()
"""
def test_profile_update_with_oversized_image(self):
    # Test profile update with an oversized image
    oversized_image_data = b'\x00' * 5242880  # 5MB of zeros
    oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
    form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
    self.assertFalse(form.is_valid())
"""

- The test function `test_profile_update_with_oversized_image` is intended to assess the profile update functionality for the case where an image file 
  exceeds the acceptable file size limit.

- `oversized_image_data` is a byte string that's created by repeating the null byte (`\x00`) 5,242,880 times, 
   effectively simulating a 5MB file. This size is generally considered too large for an image to be uploaded 
   in the context of web applications due to concerns over storage and bandwidth.

- `oversized_image_file` is a simulated file created with Django's `SimpleUploadedFile` helper. 
   It mimics an uploaded image file named 'new_image.jpg' with the 5MB of null byte data, and the content type set to 'image/jpeg', 
   indicating that the file should be recognized as a JPEG image.

- The `ProfileUpdateForm` is instantiated with the oversized image file included in the `files` dictionary to emulate an 
  attempt by a user to upload this file to their profile. The form is tied to the test user's profile instance via the `instance` parameter.

- The validity of the form is tested using the `form.is_valid()` method, which, if the form validation is correctly set up, 
  should return `False` because the file size exceeds the allowed limit for an image upload.

- The assertion `self.assertFalse(form.is_valid())` checks that the form is indeed invalid with the oversized image. 
   If the form validation is not correctly implemented to check for file size constraints, the test would fail. 
   This test is important to prevent users from uploading excessively large files, which could lead to increased server load, higher storage costs, and a degraded user experience due to slow load times.

#
#

16. Another important aspect of testing is to see if your tests provide good coverage on your codebase.
coverage.py is a tool for measuring code coverage, which means it checks which parts of your code are being executed by your tests. 
It's often used to ensure that your tests are exercising a sufficient portion of your codebase.

- Installation
First, you need to install the coverage package if you haven't already. You can install it using pip:
"""
pip install coverage

"""

- Basic Usage
To use coverage.py, you typically follow these steps:

Run Your Tests with Coverage

Instead of just running your tests with unittest, you prefix your test command with coverage run. 
For example, using Django's test runner:
"""
coverage run manage.py test

"""

- Generate a Report
After running your tests with coverage, you can generate a report to see the results.
This will print a simple coverage report to the console, showing you the percentage of coverage for each file.
"""
coverage report

"""

-Generate an HTML Report
For a more detailed view, you can generate an HTML report
"""
coverage html

"""
This will create a directory called htmlcov containing an interactive HTML report. 
You can open htmlcov/index.html in your web browser to view it.

** Remember to add htmlcov/ and .coverage to your .gitignore file, 
as you usually don't want to include coverage data and HTML reports in your version control system. **

SUMMARY

Importance of Automated Testing

1. Quality Assurance 
   Automated tests help ensure that the code works as expected and that new changes don't break existing functionality. 
   This is crucial for maintaining the integrity of a web application over time.

2. Efficiency 
   Writing tests for Django applications automates the process of checking for errors, saving developers time and effort compared to manual testing. 
   This allows for more frequent testing and faster development cycles.

3. Refactoring Confidence 
   Automated tests provide a safety net that gives developers the confidence to refactor and improve the code without fear of introducing regressions.

4. Documentation 
   Tests can serve as a form of documentation for your code. 
   They provide insights into what the code is supposed to do, which can be helpful for new developers joining a project.

5. Debugging 
   When tests fail, they can pinpoint the exact location of problems, making debugging much easier and faster.

6. Continuous Integration (CI) 
   Automated tests are integral to CI/CD pipelines. 
   When tests are automated, they can be run every time code is pushed to a repository, ensuring that only code that passes all tests is deployed.

7. Scalability 
   As a Django application grows, manual testing becomes less practical. 
   Automated testing scales much more effectively with the size of the project.

8. Risk Mitigation 
   By catching issues early in the development process, automated tests reduce the risk of bugs making it to production, 
   which can be costly to fix and damaging to user trust.

9. Test Coverage 
   Tools can measure test coverage, the proportion of your codebase tested by automated tests, 
   which is a key metric for understanding the effectiveness of your testing strategy.

10. Development Culture 
    Automated testing promotes a culture of quality and accountability. 
    It encourages writing testable code and considering edge cases and potential errors during the development process.




