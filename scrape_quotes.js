import fs from 'fs';
import puppeteer from 'puppeteer';

const scrape = async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const allQuotes = [];
  let currentPage = 1;
  const maxPages = 10;

  while (currentPage <= maxPages) {
    const url = `https://quotes.toscrape.com/page/${currentPage}/`;
    await page.goto(url);
    const quotes = await page.evaluate((currentPage) => {
      const quoteElements = document.querySelectorAll('.quote');
      return Array.from(quoteElements).map((element) => {
        const quote = element.querySelector('.text').textContent;
        const author = element.querySelector('.author').textContent;
        const authorLink = `https://quotes.toscrape.com/${element.querySelector('a').getAttribute('href')}`;
        const keywords = element.querySelector('.keywords').getAttribute('content').split(',');
        const tagLinks = keywords.map(tag => `https://quotes.toscrape.com/tag/${tag}/page/${currentPage}/`);

        return {
          quote,
          author,
          authorLink,
          keywords,
          tagLinks,
        };
      });
    }, currentPage);

    allQuotes.push(...quotes);
    console.log(`Quotes on page ${currentPage}: `, quotes);
    currentPage++;
  }

  console.log(`Data saved to quotes.json`)
  fs.writeFileSync('quotes.json', JSON.stringify(allQuotes, null, 2));
  await browser.close();
}

scrape();
