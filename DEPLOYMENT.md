# PDF Receipt Processing API - Deployment Guide

## 🚀 Deploy to Render.com (Free)

### Step 1: Prepare Your GitHub Repository

1. **Create a GitHub account** (if you don't have one)
   - Go to: https://github.com/signup

2. **Create a new repository**
   - Go to: https://github.com/new
   - Repository name: `pdf-receipt-api`
   - Description: "API to extract transaction data from PDF receipts"
   - Visibility: Public or Private (both work with Render)
   - **Don't** initialize with README (we already have files)
   - Click "Create repository"

3. **Push your code to GitHub**

   Open terminal in your project folder and run:

   ```bash
   cd c:\Users\Meet\.gemini\pdf-receipt-api
   
   # Initialize git
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: PDF receipt processing API"
   
   # Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/pdf-receipt-api.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

   **Note:** If git asks for credentials, use your GitHub username and a Personal Access Token (not password).
   - Generate token at: https://github.com/settings/tokens

---

### Step 2: Deploy on Render.com

1. **Create Render account**
   - Go to: https://render.com/
   - Click "Get Started" or "Sign Up"
   - Sign up with GitHub (easiest option)

2. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `pdf-receipt-api`
   - Click "Connect"

3. **Configure the service**
   
   Render will auto-detect the settings from `render.yaml`, but verify:
   
   - **Name:** `pdf-receipt-api` (or your choice)
   - **Environment:** `Python`
   - **Region:** Choose closest to you (e.g., Singapore)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** `Free`

4. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Watch the build logs

5. **Get your URL**
   - Once deployed, you'll see: `https://pdf-receipt-api-XXXX.onrender.com`
   - Copy this URL - this is your production API endpoint!

---

### Step 3: Test Your Deployed API

1. **Health check**
   ```bash
   curl https://your-app.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "PDF Receipt Processing API",
     "version": "1.0.0"
   }
   ```

2. **Test with a PDF**
   ```bash
   curl -X POST https://your-app.onrender.com/process-receipt \
     -F "file=@trial.pdf"
   ```

---

### Step 4: Integrate with Your Chatbot

Now that your API is live, update your chatbot flow:

#### In your chatbot External API Request:

```
Method: POST
URL: https://your-app.onrender.com/process-receipt

Headers:
  Content-Type: multipart/form-data

Body:
  file: {{last_user_attachment}}

Save response as: receipt_data
```

#### Then add conditions:

```
Condition 1: Check Success
  {{receipt_data.success}} equals "true"
  
  Success Path:
    → Check amount: {{receipt_data.data.amount}} equals "100"
    → If yes: Add tag payment_verified
    → Send: "✅ Payment confirmed! RM {{receipt_data.data.amount}}"
  
  Failed Path:
    → Send: "⚠️ Could not read receipt. Please send again."
```

---

## 📊 Your Deployed API Endpoints

Once deployed, your API will have:

### `GET /`
API documentation

### `GET /health`  
Health check for monitoring

### `POST /process-receipt`
Process PDF receipt

**Example response:**
```json
{
  "success": true,
  "data": {
    "bank": "Maybank",
    "transaction_id": "290121492M",
    "amount": 100.00,
    "date": "03 Dec 2025",
    "time": "09:37 AM",
    "receiver_account": "564191775091",
    "status": "successful"
  }
}
```

---

## ⚙️ Render.com Free Tier Limits

- ✅ **750 hours/month** (enough for 24/7 uptime)
- ✅ **Free SSL** (automatic HTTPS)
- ✅ **Auto-deploy** from GitHub (push updates automatically)
- ⚠️ **Sleeps after 15 min inactivity** (first request after sleep takes ~30 sec)
- ⚠️ **512 MB RAM** (sufficient for this API)

---

## 🔄 Updating Your Deployed API

When you make code changes:

```bash
cd c:\Users\Meet\.gemini\pdf-receipt-api

# Make your changes, then:
git add .
git commit -m "Description of changes"
git push

# Render will automatically redeploy!
```

---

## 🐛 Troubleshooting

### Build fails on Render
- Check the build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Make sure Python version matches (`runtime.txt`)

### API returns 500 error
- Check Render logs: Dashboard → Your service → Logs
- Test locally first to debug

### Slow first response
- Normal! Free tier sleeps after inactivity
- First request wakes it up (~30 seconds)
- Subsequent requests are fast

---

## 🎯 Alternative: Deploy to Railway.app

If you prefer Railway instead of Render:

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `pdf-receipt-api`
5. Railway auto-detects and deploys
6. Get your URL from the deployment page

Railway gives $5 free credit per month.

---

## ✅ Deployment Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub  
- [ ] Created Render.com account
- [ ] Connected GitHub repo to Render
- [ ] Deployed web service
- [ ] Tested `/health` endpoint
- [ ] Tested `/process-receipt` with PDF
- [ ] Got production URL
- [ ] Updated chatbot External API Request
- [ ] Tested end-to-end chatbot flow

---

## 📝 Production URL

Once deployed, save your URL here:

```
Production API: https://your-app.onrender.com
```

Use this URL in your chatbot's External API Request configuration!
