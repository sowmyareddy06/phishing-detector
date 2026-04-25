importScripts('analyzer.js');

const setBadge = (tabId, result) => {
  const text = result.riskLevel === 'Safe' ? 'OK' : result.riskLevel === 'Suspicious' ? '!' : 'PH';
  const color = result.riskLevel === 'Safe' ? '#00ff88' : result.riskLevel === 'Suspicious' ? '#ffae33' : '#ff4444';
  chrome.action.setBadgeText({ tabId, text });
  chrome.action.setBadgeBackgroundColor({ tabId, color });
};

const storeAnalysis = (tabId, result) => {
  const payload = {};
  payload[`analysis_${tabId}`] = result;
  chrome.storage.local.set(payload);
};

const handleTabUpdate = (tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'complete') return;
  if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) return;
  const result = urlAnalyzer.analyzeUrl(tab.url);
  storeAnalysis(tabId, result);
  setBadge(tabId, result);
};

chrome.tabs.onUpdated.addListener(handleTabUpdate);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getAnalysis') {
    const tabId = message.tabId;
    const storageKey = `analysis_${tabId}`;
    chrome.storage.local.get(storageKey, (data) => {
      const result = data[storageKey] || urlAnalyzer.analyzeUrl(message.url || '');
      sendResponse(result);
    });
    return true;
  }

  if (message.action === 'updateAnalysis') {
    const tabId = message.tabId;
    const result = message.analysis;
    if (tabId && result) {
      storeAnalysis(tabId, result);
      setBadge(tabId, result);
    }
    sendResponse({ success: true });
    return true;
  }
});
