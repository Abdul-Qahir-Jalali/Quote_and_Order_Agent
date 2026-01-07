# How to Deploy to Vercel

Here are the simple steps to deploy your **Agentic Quote & Order System** to Vercel.

## Prerequisites
1.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com/).
2.  **GitHub Repo**: You already have this!

## Step 1: Connect to Vercel
1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Find your repository: `Quote_and_Order_Agent`.
4.  Click **"Import"**.

## Step 2: Configure Project
1.  **Framework Preset**: Select **"FastAPI"** (or leave as "Other").
2.  **Root Directory**: Leave it as `./` (default).
3.  **Environment Variables** (Critical!):
    *   Expand the **"Environment Variables"** section.
    *   Open your local `.env` file on your computer.
    *   Copy every key and value from your `.env` file into Vercel.
    *   *Example*:
        *   Key: `GROQ_API_KEY`
        *   Value: `gsk_...` (your actual key)

## Step 3: Deploy
1.  Click **"Deploy"**.
2.  Wait for Vercel to build your project (about 1 minute).
3.  **Success!** You will get a live URL (e.g., `https://quote-and-order-agent.vercel.app`).

## Troubleshooting
*   **"Internal Server Error"**: Usually means you forgot an Environment Variable. Go to **Settings > Environment Variables** on Vercel and check.
