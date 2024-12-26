db = db.getSiblingDB('metro_lisboa');

function loadJsonFile(filename) {
    return JSON.parse(fs.readFileSync(filename, 'utf8'));
}

try {
    var data = loadJsonFile('/data/estacoes_metro.json');
    db.estacoes.drop();
    db.estacoes.insertMany(data.features);
    print("Data import completed successfully.");
} catch (error) {
    print("An error occurred during data import:");
    print(error);
}