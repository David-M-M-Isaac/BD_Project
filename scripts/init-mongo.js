const fs = require('fs');

// Define the database-to-file mapping
const databaseMapping = {
    Company_Database: ['dell_data.json', 'ibm_data.json', 'intel_data.json', 'microsoft_data.json', 'nvidia_data.json', 'sony_data.json'],
    Youtube_Database: ['youtube_data_us.json', 'youtube_data_br.json','youtube_data_ca.json','youtube_data_de.json',
                        'youtube_data_fr.json','youtube_data_gb.json','youtube_data_in.json','youtube_data_jp.json',
                        'youtube_data_kr.json','youtube_data_mx.json','youtube_data_ru.json'],
    Final_Database: ['company','youtube'],
    Final_Database: ['dell','ibm','intel','microsoft','nvidia','sony'],

};

// Function to load JSON files
function loadJsonFile(filename) {
    return JSON.parse(fs.readFileSync(filename, 'utf8')); // Use MongoDB shell's `cat` to read files
}

// Helper function to convert $oid to native ObjectId
function convertIds(document) {
    if (document._id && document._id.$oid) {
        document._id = ObjectId(document._id.$oid); // MongoDB shell's built-in ObjectId
    }
    return document;
}

// Iterate over the databaseMapping
for (const [dbName, files] of Object.entries(databaseMapping)) {
    try {
        const targetDb = db.getSiblingDB(dbName); // Switch to target database

        files.forEach((file) => {
            try {
                let data = loadJsonFile(`database/data/${file}`);

                // Ensure all documents have valid ObjectId for _id
                data = data.map(convertIds);

                // Derive collection name from the file name by removing the extension
                const collectionName = file.split('.').slice(0, -1).join('.');

                // Drop the collection if it exists and insert data
                targetDb[collectionName].drop();
                targetDb[collectionName].insertMany(data);

                console.log(`Data from ${file} imported successfully into the ${collectionName} collection of ${dbName}.`);
            } catch (fileError) {
                console.log(`An error occurred while importing ${file} into ${dbName}:`);
                console.log(fileError);
            }
        });
    } catch (dbError) {
        console.log(`An error occurred while accessing the database ${dbName}:`);
        console.log(dbError);
    }
}

