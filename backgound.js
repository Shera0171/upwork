var tabUrls = {};

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'startScraping') {
    // Query all tabs in the current browser window
    chrome.tabs.query({ currentWindow: true }, function (tabs) {
      const urlPattern = /^https:\/\/www.upwork.com\/ab\/proposals\/\d+$/;

      tabs.forEach(function (tab) {
        if (urlPattern.test(tab.url)) {
          if (!tabUrls[tab.url]) {
            tabUrls[tab.url] = true; // Mark this tab as having a request sent

            // Trigger the API by sending a GET request to your Flask server
            fetch(`http://localhost:5000/run_selenium_script?url=${tab.url}`)
              .then(response => response.text())
              .then(result => {
                console.log(result);
              });
          }
        }
      });
    });
  }
});


