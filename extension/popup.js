const formatNumber = (value) => value.toLocaleString();

const renderAnalysis = (analysis) => {
  document.getElementById('risk-level').textContent = analysis.riskLevel;
  document.getElementById('trust-score').textContent = `${analysis.trustScore}%`;
  document.getElementById('https-status').textContent = analysis.httpsStatus;
  document.getElementById('monthly-users').textContent = `Monthly users: ${formatNumber(analysis.monthlyUsers)}`;
  document.getElementById('daily-visitors').textContent = `Daily visitors: ${formatNumber(analysis.dailyVisitors)}`;
  document.getElementById('purpose').textContent = analysis.purpose;
  const reasonsList = document.getElementById('reasons');
  reasonsList.innerHTML = '';
  analysis.reasons.forEach((reason) => {
    const li = document.createElement('li');
    li.textContent = reason;
    reasonsList.appendChild(li);
  });
  document.getElementById('source-badge').textContent = 'Local analysis';
};

const getActiveTab = async () => {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs[0]);
    });
  });
};

const fetchAnalysis = async (tab) => {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ action: 'getAnalysis', tabId: tab.id, url: tab.url }, (response) => {
      resolve(response);
    });
  });
};

const initializePopup = async () => {
  const tab = await getActiveTab();
  if (!tab) return;
  document.getElementById('url').textContent = tab.url;

  const analysis = await fetchAnalysis(tab);
  renderAnalysis(analysis);

  document.getElementById('refresh-btn').addEventListener('click', async () => {
    const freshAnalysis = urlAnalyzer.analyzeUrl(tab.url);
    chrome.runtime.sendMessage({ action: 'updateAnalysis', tabId: tab.id, analysis: freshAnalysis }, () => {});
    renderAnalysis(freshAnalysis);
  });
};

initializePopup();
