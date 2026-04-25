from flask import Flask, request, jsonify, render_template
import pickle
import whois
from datetime import datetime
import random
import json
from functools import lru_cache
import time
from pathlib import Path
import requests
import os

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Load the trained model
with open(BASE_DIR / 'model.pkl', 'rb') as f:
    model = pickle.load(f)

# API Keys (set these environment variables or replace with your actual keys)
SIMILARWEB_API_KEY = os.getenv('SIMILARWEB_API_KEY', '')
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')

# Simple in-memory cache
cache = {}

# Feature extraction function
def extract_features(url):
    url_length = len(url)
    has_https = 1 if url.startswith('https') else 0
    num_dots = url.count('.')
    suspicious_keywords = ['login', 'secure', 'bank', 'verify', 'account', 'password', 'paypal']
    has_suspicious = 1 if any(kw in url.lower() for kw in suspicious_keywords) else 0
    return [url_length, has_https, num_dots, has_suspicious]

# Function to get domain age with caching
@lru_cache(maxsize=100)
def get_domain_age(url):
    try:
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
        else:
            domain = url.split('/')[0]
        domain = domain.split(':')[0]
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            age_years = age_days / 365.25
            return age_years
        else:
            return 0
    except Exception as e:
        print(f"Error getting domain age: {e}")
        return 0

# Function to get real traffic data from SimilarWeb API
@lru_cache(maxsize=50)
def get_similarweb_data(domain):
    if not SIMILARWEB_API_KEY:
        return None

    try:
        # SimilarWeb API endpoint for traffic data
        url = f"https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/visits"
        headers = {
            'api-key': SIMILARWEB_API_KEY
        }
        params = {
            'start_date': '2024-01',
            'end_date': '2024-12',
            'country': 'world',
            'granularity': 'monthly'
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant metrics
            visits_data = data.get('visits', [])
            if visits_data:
                # Get the latest month's data
                latest_data = visits_data[-1]
                monthly_visits = latest_data.get('visits', 0)

                # Estimate daily visitors (rough approximation)
                daily_visitors = monthly_visits // 30

                return {
                    'monthly_users': monthly_visits,
                    'daily_visitors': daily_visitors,
                    'source': 'SimilarWeb API'
                }
    except Exception as e:
        print(f"Error fetching SimilarWeb data: {e}")

    return None

# Function to get security data from VirusTotal API
@lru_cache(maxsize=50)
def get_virustotal_data(url):
    if not VIRUSTOTAL_API_KEY:
        return None

    try:
        # Extract domain from URL
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
        else:
            domain = url.split('/')[0]
        domain = domain.split(':')[0]

        # VirusTotal API endpoint for domain report
        vt_url = f"https://www.virustotal.com/api/v3/domains/{domain}"
        headers = {
            'x-apikey': VIRUSTOTAL_API_KEY
        }

        response = requests.get(vt_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            attributes = data.get('data', {}).get('attributes', {})

            # Extract security metrics
            last_analysis_stats = attributes.get('last_analysis_stats', {})
            malicious = last_analysis_stats.get('malicious', 0)
            suspicious = last_analysis_stats.get('suspicious', 0)
            harmless = last_analysis_stats.get('harmless', 0)
            total_scans = malicious + suspicious + harmless

            # Calculate trust score based on analysis
            if total_scans > 0:
                trust_score = int((harmless / total_scans) * 100)
            else:
                trust_score = 50  # Default if no analysis

            # Determine risk level
            if malicious > 0:
                risk_level = 'Phishing'
            elif suspicious > 0:
                risk_level = 'Suspicious'
            else:
                risk_level = 'Safe'

            return {
                'trust_score': trust_score,
                'risk_level': risk_level,
                'malicious_detections': malicious,
                'suspicious_detections': suspicious,
                'total_scans': total_scans,
                'source': 'VirusTotal API'
            }
    except Exception as e:
        print(f"Error fetching VirusTotal data: {e}")

    return None

# Mock data generators with caching and real API integration
@lru_cache(maxsize=50)
def generate_mock_data(url):
    domain = url.split('://')[1].split('/')[0] if '://' in url else url.split('/')[0]
    is_phishing = any(kw in url.lower() for kw in ['fake', 'secure-paypal', 'verify-account', 'login-bank', 'password-reset'])

    # Try to get real data from APIs first
    real_traffic_data = get_similarweb_data(domain)
    real_security_data = get_virustotal_data(url)

    # Use real security data if available
    if real_security_data:
        trust_score = real_security_data['trust_score']
        risk_level = real_security_data['risk_level']
        reasons = ['Based on VirusTotal analysis.']
        if real_security_data['malicious_detections'] > 0:
            reasons.append(f'{real_security_data["malicious_detections"]} malicious detections found.')
        if real_security_data['suspicious_detections'] > 0:
            reasons.append(f'{real_security_data["suspicious_detections"]} suspicious detections found.')
    else:
        # Fallback to mock security data
        if is_phishing:
            trust_score = random.randint(10, 40)
            risk_level = 'Phishing'
            reasons = ['Contains suspicious keywords.', 'Low traffic volume.', 'Short domain age.']
        else:
            trust_score = random.randint(70, 100)
            risk_level = 'Safe' if trust_score > 85 else 'Suspicious'
            reasons = ['Based on URL analysis and traffic patterns.']

    # Use real traffic data if available
    if real_traffic_data:
        monthly_users = real_traffic_data['monthly_users']
        daily_visitors = real_traffic_data['daily_visitors']
        bounce_rate = random.uniform(0.2, 0.6)  # Still mock bounce rate
        session_duration = random.uniform(120, 600)  # Still mock session duration
    else:
        # Fallback to mock traffic data
        if is_phishing:
            monthly_users = random.randint(100, 10000)
            daily_visitors = monthly_users // 30
            bounce_rate = random.uniform(0.7, 0.95)
            session_duration = random.uniform(10, 60)
        else:
            monthly_users = random.randint(1000000, 100000000)
            daily_visitors = monthly_users // 30
            bounce_rate = random.uniform(0.2, 0.6)
            session_duration = random.uniform(120, 600)

    # Generate AI insights based on domain
    if 'google' in domain:
        purpose = 'Search engine'
        summary = 'Google is a multinational technology company that specializes in Internet-related services and products.'
    elif 'amazon' in domain:
        purpose = 'E-commerce'
        summary = 'Amazon is an American multinational technology company which focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence.'
    elif 'facebook' in domain:
        purpose = 'Social networking'
        summary = 'Facebook is a social networking service owned by Meta Platforms.'
    else:
        purpose = 'General website'
        summary = f'{domain} is a website providing various online services.'

    # Traffic sources (still mock for now, could be enhanced with real API)
    traffic_sources = {
        'Direct': random.uniform(0.3, 0.6),
        'Search': random.uniform(0.2, 0.5),
        'Social': random.uniform(0.05, 0.2),
        'Referral': random.uniform(0.05, 0.15)
    }
    total = sum(traffic_sources.values())
    traffic_sources = {k: v/total for k, v in traffic_sources.items()}

    # Demographics (still mock)
    age_groups = {
        '18-24': random.uniform(0.1, 0.3),
        '25-34': random.uniform(0.2, 0.4),
        '35-44': random.uniform(0.15, 0.35),
        '45-54': random.uniform(0.1, 0.25),
        '55+': random.uniform(0.05, 0.2)
    }
    total_age = sum(age_groups.values())
    age_groups = {k: v/total_age for k, v in age_groups.items()}

    devices = {
        'Mobile': random.uniform(0.4, 0.7),
        'Desktop': random.uniform(0.3, 0.6)
    }
    total_dev = sum(devices.values())
    devices = {k: v/total_dev for k, v in devices.items()}

    # Top countries (still mock)
    countries = ['United States', 'India', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 'Japan', 'Brazil', 'Mexico']
    top_countries = random.sample(countries, 5)
    country_data = {country: random.randint(10000, 1000000) for country in top_countries}

    # Growth data (yearly)
    growth_years = [2020, 2021, 2022, 2023, 2024, 2025]
    growth_data = [monthly_users * (0.8 + i * 0.1) for i in range(len(growth_years))]

    # Reviews (still mock)
    num_reviews = random.randint(10, 100)
    positive_reviews = random.randint(int(num_reviews * 0.6), num_reviews)
    negative_reviews = num_reviews - positive_reviews

    reviews = []
    for _ in range(min(5, num_reviews)):
        if random.random() < 0.7:
            reviews.append("Great website! Very useful and reliable.")
        else:
            reviews.append("Suspicious content. Be careful.")

    # Domain info
    domain_age = get_domain_age(url)
    https_status = 'Yes' if url.startswith('https') else 'No'
    hosting_country = random.choice(['United States', 'Germany', 'Netherlands', 'Canada', 'Japan'])
    registrar = random.choice(['GoDaddy', 'Namecheap', 'Hostinger', 'Bluehost', 'SiteGround'])

    # Calculate rating based on trust score
    rating = round((trust_score / 100) * 5, 1)

    return {
        'trust_score': trust_score,
        'risk_level': risk_level,
        'reasons': reasons,
        'domain_age': round(domain_age, 1),
        'https_status': https_status,
        'hosting_country': hosting_country,
        'registrar': registrar,
        'monthly_users': monthly_users,
        'daily_visitors': daily_visitors,
        'bounce_rate': round(bounce_rate * 100, 1),
        'session_duration': round(session_duration, 1),
        'traffic_sources': traffic_sources,
        'age_groups': age_groups,
        'devices': devices,
        'top_countries': country_data,
        'growth_data': dict(zip(growth_years, growth_data)),
        'rating': rating,
        'num_reviews': num_reviews,
        'positive_reviews': positive_reviews,
        'negative_reviews': negative_reviews,
        'reviews': reviews,
        'purpose': purpose,
        'summary': summary,
        'data_sources': {
            'traffic': 'real' if real_traffic_data else 'mock',
            'security': 'real' if real_security_data else 'mock',
            'domain': 'real',  # WHOIS is always real if available
            'reviews': 'mock'  # Reviews are always mock for now
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@app.route('/predict', methods=['POST'])
def analyze():
    try:
        start_time = time.time()

        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        url = data['url'].strip()
        if not url:
            return jsonify({'error': 'URL cannot be empty'}), 400

        # Check cache
        cache_key = url
        if cache_key in cache:
            cached_result = cache[cache_key]
            if time.time() - cached_result['timestamp'] < 3600:  # 1 hour cache
                return jsonify(cached_result['data'])

        # Extract features and predict
        features = extract_features(url)
        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]
        ml_confidence = probabilities[prediction]

        # Get mock data
        mock_data = generate_mock_data(url)

        # Adjust trust score based on ML
        if prediction == 1:  # phishing
            mock_data['trust_score'] = min(mock_data['trust_score'], int(ml_confidence * 50))
            mock_data['risk_level'] = 'Phishing'
        else:
            mock_data['trust_score'] = max(mock_data['trust_score'], int(ml_confidence * 100))

        # Add confidence score
        mock_data['confidence_score'] = round(ml_confidence * 100, 1)

        # Cache result
        cache[cache_key] = {
            'data': mock_data,
            'timestamp': time.time()
        }

        processing_time = time.time() - start_time
        mock_data['processing_time'] = round(processing_time, 2)

        return jsonify(mock_data)

    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)