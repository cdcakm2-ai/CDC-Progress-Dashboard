const https = require('https');

function fetchHtml(url) {
  return new Promise((resolve) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchHtml(res.headers.location).then(resolve);
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
  });
}

async function check() {
  const html2 = await fetchHtml('https://docs.google.com/spreadsheets/d/1H_bwTOUUGj_cpIZKfBxs74Omt0xIgtTVeWhaRA3G7WI/htmlview');
  console.log('HTML2 length:', html2.length);
  const sheetMatches = html2.match(/<li id="sheet-button-[^"]+"[^>]*>.*?<\/li>/g);
  console.log('Sheet 2 tabs:', sheetMatches);

  const html1 = await fetchHtml('https://docs.google.com/spreadsheets/d/1JGjlJxPri48nzVyRgZS1hd8_VMF2t7rU0_KU-xEnYkk/htmlview');
  console.log('HTML1 length:', html1.length);
  const sheetMatches1 = html1.match(/<li id="sheet-button-[^"]+"[^>]*>.*?<\/li>/g);
  console.log('Sheet 1 tabs:', sheetMatches1);
}
check();
