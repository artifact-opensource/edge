#!/bin/bash
# Deploy Stakeholder Portal to Vercel (Preview Mode)
# Run this script from your Codespace with internet access

set -e  # Exit on error

echo "🚀 Stakeholder Portal - Preview Deployment Script"
echo "=================================================="
echo ""

# Check if we have internet
echo "📡 Checking internet connectivity..."
if ! ping -c 1 google.com &> /dev/null; then
    echo "❌ ERROR: No internet connection detected"
    echo "   Make sure you're running this in Codespace or local machine"
    exit 1
fi
echo "✅ Internet connection verified"
echo ""

# Check if Vercel CLI is installed
echo "🔧 Checking Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "⚙️  Installing Vercel CLI..."
    npm install -g vercel
else
    echo "✅ Vercel CLI already installed ($(vercel --version))"
fi
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBSITE_DIR="$SCRIPT_DIR"

echo "📂 Working directory: $WEBSITE_DIR"
echo ""

# Deploy Frontend
echo "🎨 Deploying Frontend (Preview)..."
echo "-----------------------------------"
cd "$WEBSITE_DIR/frontend"

if [ ! -d "dist" ]; then
    echo "⚠️  Frontend not built yet. Building..."
    npm ci --ignore-scripts
    npm run build
fi

echo "📤 Deploying to Vercel..."
echo "   (This will open browser for authentication if first time)"
vercel --yes

FRONTEND_URL=$(vercel inspect --json | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)
echo ""
echo "✅ Frontend deployed!"
echo "   Preview URL will be shown above"
echo ""

# Deploy Backend
echo "🔧 Deploying Backend (Preview)..."
echo "-----------------------------------"
cd "$WEBSITE_DIR/backend"

if [ ! -d "dist" ]; then
    echo "⚠️  Backend not built yet. Building..."
    npm ci --ignore-scripts
    npx prisma generate
    npx tsc
fi

echo "📤 Deploying to Vercel..."
vercel --yes

BACKEND_URL=$(vercel inspect --json | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)
echo ""
echo "✅ Backend deployed!"
echo "   Preview URL will be shown above"
echo ""

# Summary
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "Your preview deployments are ready!"
echo ""
echo "📱 Frontend: Check output above for URL"
echo "🔧 Backend:  Check output above for URL"
echo ""
echo "⚙️  Next Steps:"
echo "   1. Open the frontend URL to test the UI"
echo "   2. Configure environment variables in Vercel Dashboard if needed:"
echo "      - Backend: DATABASE_URL, REDIS_URL, JWT_SECRET, ALLOWED_EMAILS"
echo "      - Frontend: VITE_API_URL (set to backend URL)"
echo "   3. Test all functionality"
echo "   4. If everything works, promote to production with: vercel --prod"
echo ""
echo "📖 See PREVIEW-DEPLOY.md for more details"
echo ""
