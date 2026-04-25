import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Sample dataset: 100 URLs (50 safe, 50 phishing)
safe_urls = [
    'https://google.com',
    'https://yahoo.com',
    'https://github.com',
    'https://stackoverflow.com',
    'https://microsoft.com',
    'https://apple.com',
    'https://amazon.com',
    'https://facebook.com',
    'https://twitter.com',
    'https://linkedin.com',
    'https://wikipedia.org',
    'https://reddit.com',
    'https://youtube.com',
    'https://instagram.com',
    'https://netflix.com',
    'https://spotify.com',
    'https://dropbox.com',
    'https://slack.com',
    'https://zoom.us',
    'https://discord.com',
    'https://notion.so',
    'https://figma.com',
    'https://canva.com',
    'https://trello.com',
    'https://asana.com',
    'https://mailchimp.com',
    'https://shopify.com',
    'https://stripe.com',
    'https://paypal.com',
    'https://ebay.com',
    'https://craigslist.org',
    'https://indeed.com',
    'https://glassdoor.com',
    'https://linkedin.com/jobs',
    'https://github.io',
    'https://medium.com',
    'https://quora.com',
    'https://pinterest.com',
    'https://tumblr.com',
    'https://flickr.com',
    'https://vimeo.com',
    'https://dailymotion.com',
    'https://soundcloud.com',
    'https://bandcamp.com',
    'https://lastfm.com',
    'https://goodreads.com',
    'https://imdb.com',
    'https://rottentomatoes.com',
    'https://metacritic.com',
    'https://allmusic.com'
]

phishing_urls = [
    'https://fakebank-login.com',
    'https://secure-paypal.com',
    'https://verify-account.net',
    'https://login-bank.org',
    'https://password-reset.biz',
    'https://account-verify.info',
    'https://bank-login-secure.com',
    'https://paypal-verify.net',
    'https://amazon-login.org',
    'https://facebook-secure.biz',
    'https://google-verify.com',
    'https://microsoft-login.net',
    'https://apple-account.org',
    'https://netflix-password.biz',
    'https://spotify-secure.info',
    'https://dropbox-login.com',
    'https://slack-verify.net',
    'https://zoom-account.org',
    'https://discord-password.biz',
    'https://notion-secure.info',
    'https://figma-login.com',
    'https://canva-verify.net',
    'https://trello-account.org',
    'https://asana-password.biz',
    'https://mailchimp-secure.info',
    'https://shopify-login.com',
    'https://stripe-verify.net',
    'https://paypal-account.org',
    'https://ebay-password.biz',
    'https://craigslist-secure.info',
    'https://indeed-login.com',
    'https://glassdoor-verify.net',
    'https://linkedin-account.org',
    'https://github-password.biz',
    'https://medium-secure.info',
    'https://quora-login.com',
    'https://pinterest-verify.net',
    'https://tumblr-account.org',
    'https://flickr-password.biz',
    'https://vimeo.com',
    'https://dailymotion.com',
    'https://soundcloud.com',
    'https://bandcamp.com',
    'https://lastfm.com',
    'https://goodreads.com',
    'https://imdb.com',
    'https://rottentomatoes.com',
    'https://metacritic.com',
    'https://allmusic.com'
]

urls = safe_urls + phishing_urls
labels = [0] * len(safe_urls) + [1] * len(phishing_urls)  # 0: safe, 1: phishing

df = pd.DataFrame({'url': urls, 'label': labels})

# Feature extraction function
def extract_features(url):
    url_length = len(url)
    has_https = 1 if url.startswith('https') else 0
    num_dots = url.count('.')
    suspicious_keywords = ['login', 'secure', 'bank', 'verify', 'account', 'password', 'paypal']
    has_suspicious = 1 if any(kw in url.lower() for kw in suspicious_keywords) else 0
    return [url_length, has_https, num_dots, has_suspicious]

# Apply feature extraction
df['features'] = df['url'].apply(extract_features)

# Prepare data for training
X = df['features'].tolist()
y = df['label'].tolist()

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save model
with open(BASE_DIR / 'model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Model trained and saved as model.pkl')