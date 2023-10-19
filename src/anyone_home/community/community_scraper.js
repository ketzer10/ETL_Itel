// Require Puppeteer
const puppeteer = require('puppeteer');

async function navigate(){
    // The URLs to access the data and the credentials are passed as an argument to the program
    var args = process.argv.slice(2);
    login_url = args[0]
    username = args[1]
    password = args[2]
    scraping_url = args[3]
    id_to_wait = args[4]

    // Create a browser and page instance in pupeteer. Disable navigation timeouts.
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(0);

    // Wait for the fields to be visible
    await page.goto(login_url);
    await page.waitForSelector('#BTN_LOGIN', {visible: true})
    await page.waitForSelector('#ctl00_ContentPlaceHolder1_UserName_InnerTextBox', {visible: true})
    await page.waitForSelector('#ctl00_ContentPlaceHolder1_Password_InnerTextBox', {visible: true})
    
    // Login into community using the credentials passed as arguments
    await page.type('#ctl00_ContentPlaceHolder1_UserName_InnerTextBox', username);
    await page.type('#ctl00_ContentPlaceHolder1_Password_InnerTextBox', password);
    await page.click('#BTN_LOGIN');

    // Go to the time off events URL. The URL contains the appropiate date range passed as an argument. The URL is built in Python
    // with the appropriate parameters.
    await page.goto(scraping_url);

    // Wait for element to be visible. The element is passed as an argument since it varies from page to page
    await page.waitForSelector(id_to_wait, {visible: true, timeout: 0})

    // Wait 10 seconds anyway because I have noticed sometimes the content doesn't load immediately
    await page.waitForTimeout(5000)

    // Get page content
    const html = await page.content();
    await browser.close()

    // I know doing a console.log instead of returning the result is crap. However, I have no idea how to get the return 
    // value of a node js function in Python and I have spent like 30 minutes trying to figure it out.
    console.log(html)
}

navigate()
