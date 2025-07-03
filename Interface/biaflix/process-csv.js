// process-csv.js (usando sintaxe de Módulo ES e filtro de status)
import fs from 'fs';
import csv from 'csv-parser';

const results = [];
const csvFilePath = './TMDB_movie_dataset_v11.csv'; // Coloque o CSV na raiz do projeto
const outputFilePath = './public/movie_ids.json';   // O arquivo de saída irá para a pasta 'public'

console.log('Iniciando a leitura do arquivo CSV...');

fs.createReadStream(csvFilePath)
  .pipe(csv())
  .on('data', (data) => {
    // Adiciona o ID ao array de resultados apenas se o status for "Released"
    if (data.id && data.status === 'Released') {
      results.push(data.id);
    }
  })
  .on('end', () => {
    console.log(`Leitura do CSV finalizada. Total de ${results.length} IDs encontrados com status "Released".`);
    
    // Salva o array de IDs como um arquivo JSON na pasta 'public'
    fs.writeFileSync(outputFilePath, JSON.stringify(results, null, 2));
    
    console.log(`Arquivo 'movie_ids.json' salvo com sucesso em ${outputFilePath}`);
  });
