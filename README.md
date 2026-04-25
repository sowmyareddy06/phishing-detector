
<img width="1872" height="895" alt="advance 2" src="https://github.com/user-attachments/assets/e7239a9d-5e59-42b0-b905-d2e5c7196be8" />
<img width="1876" height="892" alt="advance 1" src="https://github.com/user-attachments/assets/74b60911-59e3-4b4d-af88-3815d8f09d3d" />
<img width="1872" height="895" alt="advance 2" src="https://github.com/user-attachments/assets/a2719a3b-25b0-427b-8971-1d3e91bcb843" />
<img width="1876" height="892" alt="advance 1" src="https://github.com/user-attachments/assets/2d0dad76-fa3b-448f-88a7-c04cbaba8ebc" />
# Advanced AI Website Intelligence & Phishing Detection Dashboard

A comprehensive full-stack web application that provides complete A-Z analysis of any website, including safety assessment, traffic analytics, user demographics, reviews, AI insights, and interactive visualizations.

## 🚀 Features

### 🔒 Safety Analysis
- **Trust Score** (0-100): AI-calculated safety rating with confidence bar
- **Risk Level**: Safe / Suspicious / Phishing classification with color-coded badges
- **Detailed Reasons**: Explanations with icons based on risk level

### 🌐 Website Overview
- Domain age verification via WHOIS
- HTTPS status check
- Hosting country detection
- Registrar information

### 📊 Traffic & Usage Analytics
- Estimated monthly users and daily visitors
- Bounce rate and session duration analysis
- Traffic source breakdown (Direct, Search, Social, Referral)
- Interactive pie chart visualization

### 👥 User Demographics
- Age group distribution (bar chart)
- Device usage statistics (mobile vs desktop - doughnut chart)
- Top countries by user count (horizontal bar chart)

### ⭐ Reviews & Reputation
- Overall rating (stars out of 5)
- Total review count with positive/negative breakdown
- Sample user reviews display
- Genuine vs suspicious review indicators

### 🤖 AI Insights
- Website purpose classification
- AI-generated summary based on domain analysis
- Intelligent content categorization

### 📈 Growth Trends
- Yearly user growth visualization
- Interactive line chart with trend analysis

## 🛠️ Technology Stack

- **Frontend**: React 18 with modern hooks, Chart.js for visualizations
- **Backend**: Python Flask with REST API
- **ML**: scikit-learn (Logistic Regression)
- **Domain Info**: python-whois
- **Caching**: LRU cache for performance
- **Styling**: CSS3 with glassmorphism, gradients, animations

## 📁 Project Structure

```
advanced-website-intelligence/
├── app.py                    # Flask backend with API endpoints
├── phishing_model.py         # ML model training script
├── requirements.txt         # Python dependencies
├── model.pkl               # Trained ML model
├── client/                 # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   ├── InputSection.js
│   │   │   ├── Results.js
│   │   │   └── sections/
│   │   │       ├── SafetyAnalysis.js
│   │   │       ├── WebsiteOverview.js
│   │   │       ├── TrafficAnalytics.js
│   │   │       ├── UserDemographics.js
│   │   │       ├── ReviewsReputation.js
│   │   │       ├── AIInsights.js
│   │   │       └── GrowthVisualization.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm (for React frontend)

### 1. Backend Setup
```bash
cd advanced-website-intelligence
pip install -r requirements.txt
python phishing_model.py  # Train the ML model
python app.py            # Start Flask server on port 5000
```

### 2. Frontend Setup (in new terminal)
```bash
cd advanced-website-intelligence/client
npm install
npm start                # Start React dev server on port 3000
```

### 3. Optional: Real API Integration
To get real traffic and security data, set up API keys:

#### SimilarWeb API (Traffic Data)
1. Sign up at [SimilarWeb](https://www.similarweb.com/developer/)
2. Get your API key
3. Set environment variable: `SIMILARWEB_API_KEY=your_key_here`

#### VirusTotal API (Security Data)
1. Sign up at [VirusTotal](https://www.virustotal.com/)
2. Get your API key
3. Set environment variable: `VIRUSTOTAL_API_KEY=your_key_here`

#### Setting Environment Variables
**Windows:**
```cmd
set SIMILARWEB_API_KEY=your_similarweb_key
set VIRUSTOTAL_API_KEY=your_virustotal_key
```

**Linux/Mac:**
```bash
export SIMILARWEB_API_KEY=your_similarweb_key
export VIRUSTOTAL_API_KEY=your_virustotal_key
```

**Without API keys, the app will use realistic mock data as fallback.**

### 4. Access the Dashboard
- Backend API: `http://localhost:5000`
- Frontend: `http://localhost:3000` (proxies to backend)

## 🎯 Usage

1. Enter any website URL in the input field
2. Click "Analyze Website" to start analysis
3. Watch the animated progress bar with status updates
4. Explore comprehensive results across all sections:
   - Safety assessment with trust score and confidence
   - Website technical details
   - Traffic and user analytics with interactive charts
   - Demographic breakdowns and visualizations
   - Review summaries and ratings
   - AI-generated insights and summaries
   - Growth trends and projections

## 🔍 How It Works

### ML Model
- Trained on 100 sample URLs (50 safe, 50 phishing)
- Features: URL length, HTTPS presence, suspicious keywords, dot count
- Logistic Regression classifier with explainable output
- Confidence scoring for trust assessment

### Real API Integration
- **SimilarWeb API**: Real traffic data (monthly users, daily visitors)
- **VirusTotal API**: Real security analysis (malware detections, trust scores)
- **WHOIS API**: Real domain age and registration information
- **Fallback System**: Automatically uses mock data if APIs are unavailable or rate-limited

### Mock Data Generation (Fallback)
- Realistic traffic statistics based on URL patterns
- Simulated user demographics and reviews
- AI insights tailored to known websites
- Growth trends with plausible yearly progression

### API Integration
- `/analyze` endpoint processes URLs with error handling
- Combines ML predictions with comprehensive analytics
- LRU caching for improved performance
- Returns structured JSON with all analysis data

## 🧩 Chrome Extension
- `extension/manifest.json` defines a Chrome extension that analyzes visited URLs in real time
- `extension/background.js` monitors tabs and updates badge risk indicators
- `extension/popup.html` shows live trust score, risk level, traffic estimation, and risk reasons
- Uses local heuristic analysis in `extension/analyzer.js` for browser-friendly URL scoring
- Load in Chrome via `chrome://extensions` → "Load unpacked" → select `advanced-website-intelligence/extension`

## 🎨 UI Features

- **Dark Cyber Theme**: Neon glows, animated grid background, floating elements
- **Glassmorphism**: Translucent cards with blur effects and gradients
- **Interactive Charts**: Multiple visualization types using Chart.js
- **Loading Animations**: Progress bar with real-time status updates
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Hover Effects**: Enhanced user interaction and feedback
- **Color-Coded Elements**: Risk levels, confidence bars, status indicators

## 🔧 Customization

### Adding Real APIs
Replace mock data in `app.py` with real API calls:
- SimilarWeb API for authentic traffic data
- VirusTotal API for comprehensive security scanning
- WHOIS APIs for enhanced domain information
- Review aggregation services for genuine user feedback

### Enhancing ML Model
- Add more features (URL entropy, lexical analysis, SSL certificate checks)
- Use advanced models (Random Forest, Neural Networks, Deep Learning)
- Train on larger, real-world datasets
- Implement ensemble methods for better accuracy

### UI Modifications
- Edit React components for layout changes
- Modify CSS files for theme adjustments
- Add new chart types or visualization libraries
- Implement dark/light mode toggle

## 📊 Sample Results

For `https://google.com`:
- Trust Score: 98 (95% confidence)
- Risk Level: Safe ✅
- Monthly Users: ~2.5B
- Main Purpose: Search engine
- Top Countries: US, India, Brazil, etc.

For suspicious URLs:
- Trust Score: 25 (78% confidence)
- Risk Level: Phishing 🚫
- Low traffic indicators
- Warning explanations with color coding

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open-source. Feel free to use and modify.

## ⚠️ Disclaimer

This is a demonstration system showcasing AI-powered web analysis. For production use:
- Implement proper authentication and rate limiting
- Add comprehensive input validation and sanitization
- Use real API services with proper licensing
- Ensure data privacy and GDPR compliance
- Add monitoring and logging for security
- Consider using cloud infrastructure for scalability

---

**Built with ❤️ using React, Flask, and scikit-learn for advanced web intelligence analysis.**
