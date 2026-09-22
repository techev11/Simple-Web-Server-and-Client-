#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>

using namespace std;

struct Counts {
    long long lines = 0;
    long long words = 0;
    long long bytes = 0;
};

Counts count_stream(istream &stream) {
    Counts c;
    string line;

    while (true) {
        char buffer[4096];
        stream.read(buffer, sizeof(buffer));
        streamsize n = stream.gcount();
        if (n <= 0) break;

        c.bytes += n;

        for (streamsize i = 0; i < n; i++) {
            if (buffer[i] == '\n')
                c.lines++;
        }

        istringstream iss(string(buffer, n));
        string word;
        while (iss >> word)
            c.words++;
    }

    return c;
}

Counts count_file(const string &filename) {
    ifstream file(filename, ios::binary);
    if (!file) {
        throw runtime_error("File not found");
    }
    return count_stream(file);
}

int main(int argc, char *argv[]) {

    // No arguments → read from stdin and print HTML
    if (argc == 1) {
        Counts c = count_stream(cin);

        cout << "<html><body><center><h1>"
             << setw(7) << c.lines << " "
             << setw(7) << c.words << " "
             << setw(7) << c.bytes
             << "</h1></center></body></html>"
             << endl;
    }
    else {
        long long total_lines = 0;
        long long total_words = 0;
        long long total_bytes = 0;

        for (int i = 1; i < argc; i++) {
            try {
                Counts c = count_file(argv[i]);

                total_lines += c.lines;
                total_words += c.words;
                total_bytes += c.bytes;

                cout << setw(7) << c.lines << " "
                     << setw(7) << c.words << " "
                     << setw(7) << c.bytes << " "
                     << argv[i] << endl;
            }
            catch (...) {
                cerr << "mywc: " << argv[i]
                     << ": No such file or directory" << endl;
            }
        }

        if (argc > 2) {
            cout << setw(7) << total_lines << " "
                 << setw(7) << total_words << " "
                 << setw(7) << total_bytes << " total"
                 << endl;
        }
    }

    return 0;
}