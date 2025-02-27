# Deploying Noan to Render

## Step 1: Prepare Your Project for Deployment

1. Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: noan
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

2. Add Gunicorn to your requirements.txt:

```
gunicorn==20.1.0
```

## Step 2: Create a Render Account

1. Go to [Render](https://render.com/) and sign up for an account
2. Verify your email address

## Step 3: Deploy Your Application

### Option A: Deploy via GitHub (Recommended)
1. Push your code to a GitHub repository
2. In Render, click "New +" and select "Web Service"
3. Connect your GitHub account and select your repository
4. Render will detect your `render.yaml` file and use those settings
5. Click "Create Web Service"

### Option B: Manual Deployment
1. In Render, click "New +" and select "Web Service"
2. Choose "Build and deploy from a Git repository"
3. Connect your GitHub account or provide a public repository URL
4. Configure your service:
   - Name: `noan`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Select the free plan

## Step 4: Environment Configuration
1. In your service dashboard, go to "Environment"
2. Click "Add Environment Variable" 
3. Add any environment variables your application needs (likely none for Noan)

## Step 5: Access Your App
1. Once the deployment is complete, Render will provide a URL
2. Your application will be accessible at `https://noan.onrender.com` (or similar)

## Step 6: Custom Domain (Optional)
1. Go to the "Settings" tab of your service
2. Scroll to "Custom Domain"
3. Follow the instructions to add your own domain

## Notes
- Render's free tier has some limitations but is sufficient for moderate usage
- Services on the free plan will spin down after 15 minutes of inactivity
- The first request after inactivity might be slow as the service spins up
- Render provides built-in HTTPS, which is a nice benefit 