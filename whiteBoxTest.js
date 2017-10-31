const puppeteer = require('puppeteer');


puppeteer.launch({headless:false}).then(async browser => {
    const page = await browser.newPage();

    await page.goto('http://192.168.7.163/?url=http://192.168.7.233:8080/mano-nfvo/rest/&topic=/TestService/run');

    setTimeout(() =>
    {
        console.log('CLOSING BROSWER NOW');
        browser.close();
        console.log('EXITING WHITE BOX TEST');
    },120000);
});