#include <iostream>
#include <iomanip>
#include <string>
#include <openssl/sha.h> // Libreria OpenSSL per SHA-256

using namespace std;

// Funzione per calcolare SHA-256 della chiave
string sha256(const string& key) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char*)key.c_str(), key.length(), hash);
    string result;

    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        result += hash[i]; // Usiamo direttamente i byte binari
    }

    return result;
}

// Funzione per criptare/decriptare usando XOR
string xorEncrypt(const string& data, const string& key){
    string hashedKey = sha256(key); // Otteniamo chiave da 32 byte
    string result;

    for(size_t i = 0; i < data.size(); ++i){
        result += data[i] ^ hashedKey[i % hashedKey.size()];
    }

    return result;
}

// Funzione per convertire binario in esadecimale (per stampa leggibile)
string toHex(const string& input){
    stringstream ss;
    for (unsigned char c : input){
        ss << hex << setw(2) << setfill('0') << (int)c;
    }
    return ss.str();
}

int main() {
    string testo, chiave;
    const string defkey = "Lf4$8Jk@3#tGw!ZpO2^qYxBn%1&CeMLd"; // Chiave valida

    cout << "Inserisci la chiave segreta: ";
    getline(cin, chiave);

    // Controllo: se la chiave è errata, termina il programma
    if(chiave != defkey){
        cerr << "Chiave non autorizzata" << endl;
        return 1; // Termina il programma con codice errore
    }

    cout << "Inserisci il testo da criptare: ";
    getline(cin, testo);

    string criptato = xorEncrypt(testo, chiave);
    string decriptato = xorEncrypt(criptato, chiave); // XOR è simmetrico

    cout << "Testo criptato: " << toHex(criptato) << endl;
    cout << "Testo decriptato: " << decriptato << endl;

    return 0;
}
