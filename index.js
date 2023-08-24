const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const url = "https://storage.googleapis.com/jus-challenges/challenge-crawler.html";

function extractTextFromTd($element, searchText) {
    const text = $element.find(`strong:contains("${searchText}:")`).parent().contents()
        .filter((i, el) => el.nodeType === 3)
        .text()
        .trim();
    return text.replace(/\s+/g, ' ');
}

async function scrapeData() {
    try {
        const response = await axios.get(url);
        const htmlContent = response.data;
        const $ = cheerio.load(htmlContent);

        const extractedData = [];
        const trList = $('#divDadosResultado-A > table > tbody > tr');

        trList.each((index, element) => {
            const item = {};
            const $tr = $(element);

            item['numero_processo'] = $tr.find('a').text().trim();
            item['ementa'] = extractTextFromTd($tr, "Ementa");
            item['relator'] = extractTextFromTd($tr, "Relator(a)");
            item['comarca'] = extractTextFromTd($tr, "Comarca");
            item['orgao_julgador'] = extractTextFromTd($tr, "Órgão julgador");
            item['data_julgamento'] = extractTextFromTd($tr, "Data do julgamento");
            item['classe_assunto'] = extractTextFromTd($tr, "Classe/Assunto");
            item['data_publicacao'] = extractTextFromTd($tr, "Data de publicação");

            extractedData.push(item);
        });

        fs.writeFileSync('extracted_data.json', JSON.stringify(extractedData, null, 4), 'utf-8');
        console.log("Data extraction and structuring completed.");
    } catch (error) {
        console.error("Error:", error);
    }
}

scrapeData();
