# Deploying Noan to PythonAnywhere

## Step 1: Create an Account
1. Sign up for a free account at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Log in to your dashboard

## Step 2: Set Up a Web App
1. Click on the "Web" tab in your dashboard
2. Click "Add a new web app"
3. Click "Next" on the domain name page
4. Select "Flask" and the latest Python version (3.10+)
5. When asked for the path to your Flask app, enter: `/home/yourusername/Noan/app.py`

## Step 3: Upload Your Code
1. Go to the "Files" tab
2. Create a new directory called "Noan"
3. Navigate into the directory
4. Upload all your project files (you can zip them and use the "Upload" button)
5. If you upload a zip, unzip it using the Bash console (Files > Bash console):
   ```
   cd Noan
   unzip your_uploaded_file.zip
   ```

## Step 4: Install Dependencies
1. Go to the "Consoles" tab
2. Start a new Bash console
3. Navigate to your project directory:
   ```
   cd Noan
   ```
4. Install the required packages:
   ```
   pip install --user -r requirements.txt
   ```

## Step 5: Configure WSGI File
1. Go to the "Web" tab
2. Click on the WSGI configuration file link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Replace the Flask section with:
   ```python
   # Import app object from your app.py
   import sys
   path = '/home/yourusername/Noan'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
4. Save the file

## Step 6: Set Up Static Files
1. Go to the "Web" tab
2. In the "Static Files" section, add:
   - URL: `/static/`
   - Directory: `/home/yourusername/Noan/static/`

## Step 7: Reload Your Web App
1. Go back to the "Web" tab
2. Click the "Reload" button for your web app

Your application should now be accessible at `yourusername.pythonanywhere.com`

## Troubleshooting
- Check the error logs in the "Web" tab if anything isn't working
- Make sure all paths in your code are relative, not absolute
- PythonAnywhere doesn't support SQLite in the web directory, so if you add a database later, store it in /tmp 