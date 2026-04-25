const urlAnalyzer = (() => {
  const suspiciousKeywords = ['login', 'secure', 'bank', 'verify', 'account', 'password', 'paypal', 'update', 'confirm', 'support', 'security', 'invoice'];

  const safePurpose = {
    google: 'Search engine',
    amazon: 'E-commerce',
    facebook: 'Social networking',
    twitter: 'Social media',
    linkedin: 'Professional network',
    github: 'Developer platform'
  };

  const stableValue = (seed, min, max) => {
    let hash = 0;
    for (let i = 0; i < seed.length; i += 1) {
      hash = (hash << 5) - hash + seed.charCodeAt(i);
      hash |= 0;
    }
    const positive = Math.abs(hash);
    return min + (positive % (max - min + 1));
  };

  const normalizeUrl = (url) => {
    try {
      const parsed = new URL(url);
      return {
        hostname: parsed.hostname.replace(/^www\./, ''),
        protocol: parsed.protocol,
        pathname: parsed.pathname
      };
    } catch {
      return { hostname: url, protocol: '', pathname: '' };
    }
  };

  const getRiskScore = (url) => {
    const { hostname, protocol } = normalizeUrl(url);
    const hasHttps = protocol === 'https:';
    const urlLength = url.length;
    const dotCount = (hostname.match(/\./g) || []).length;
    const keywordMatch = suspiciousKeywords.filter((kw) => url.toLowerCase().includes(kw)).length;
    const score = Math.max(
      10,
      Math.min(
        100,
        100 - dotCount * 6 - keywordMatch * 18 - (urlLength > 65 ? 15 : urlLength > 45 ? 8 : 0) + (hasHttps ? 12 : -8)
      )
    );
    return { score, hasHttps, keywordMatch, dotCount, urlLength };
  };

  const getRiskLevel = (score) => {
    if (score >= 70) return 'Safe';
    if (score >= 40) return 'Suspicious';
    return 'Phishing';
  };

  const getReasons = (info) => {
    const reasons = [];
    if (!info.hasHttps) reasons.push('Site does not use HTTPS.');
    if (info.keywordMatch > 0) reasons.push('URL contains suspicious keywords.');
    if (info.urlLength > 65) reasons.push('URL is unusually long.');
    if (info.dotCount > 4) reasons.push('Multiple subdomains or redirect-style URL structure.');
    if (reasons.length === 0) reasons.push('URL structure appears normal.');
    return reasons;
  };

  const estimateTraffic = (host, level) => {
    const base = stableValue(host, 10000, 8000000);
    if (level === 'Phishing') {
      return { monthly: Math.max(200, Math.floor(base * 0.03)), daily: Math.max(10, Math.floor(base * 0.0018)) };
    }
    if (level === 'Suspicious') {
      return { monthly: Math.max(1500, Math.floor(base * 0.12)), daily: Math.max(80, Math.floor(base * 0.004)) };
    }
    return { monthly: Math.max(50000, Math.floor(base * 0.35)), daily: Math.max(1200, Math.floor(base * 0.012)) };
  };

  const getPurpose = (hostname) => {
    for (const key of Object.keys(safePurpose)) {
      if (hostname.includes(key)) return safePurpose[key];
    }
    return 'General website';
  };

  const getDeviceSplit = (host) => {
    const mobile = stableValue(`${host}-mobile`, 45, 75);
    return { mobile, desktop: 100 - mobile };
  };

  const getAgeGroups = (host) => {
    const values = [
      stableValue(`${host}-18`, 8, 18),
      stableValue(`${host}-25`, 20, 35),
      stableValue(`${host}-35`, 15, 30),
      stableValue(`${host}-45`, 10, 18),
      stableValue(`${host}-55`, 5, 12)
    ];
    const total = values.reduce((sum, value) => sum + value, 0);
    return values.map((value) => Math.round((value / total) * 100));
  };

  const getTopCountries = (host) => {
    const all = ['United States', 'India', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'Brazil', 'France', 'Japan', 'Mexico'];
    const start = stableValue(host, 0, all.length - 5);
    return all.slice(start, start + 5);
  };

  const analyzeUrl = (url) => {
    const { hostname, protocol } = normalizeUrl(url);
    const info = getRiskScore(url);
    const trustScore = info.score;
    const riskLevel = getRiskLevel(trustScore);
    const traffic = estimateTraffic(hostname, riskLevel);
    const purpose = getPurpose(hostname);
    const ageGroups = getAgeGroups(hostname);
    const topCountries = getTopCountries(hostname);

    return {
      url,
      hostname,
      trustScore,
      riskLevel,
      reasons: getReasons(info),
      purpose,
      httpsStatus: protocol === 'https:' ? 'Yes' : 'No',
      monthlyUsers: traffic.monthly,
      dailyVisitors: traffic.daily,
      trafficSources: {
        Direct: 0.38,
        Search: 0.34,
        Social: 0.16,
        Referral: 0.12
      },
      ageGroups: {
        '18-24': ageGroups[0],
        '25-34': ageGroups[1],
        '35-44': ageGroups[2],
        '45-54': ageGroups[3],
        '55+': ageGroups[4]
      },
      devices: getDeviceSplit(hostname),
      topCountries,
      summary: `${hostname} appears to be a ${purpose.toLowerCase()} website.`,
      dataSource: 'local'
    };
  };

  return { analyzeUrl };
})();
