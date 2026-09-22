#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
    string input;
    string line;

    // Read entire POST body from stdin
    while (getline(cin, line)) {
        input += line + "\n";
    }

    double a = 0;
    double b = 0;

    // Expect either:
    // 1) "a=5&b=3"   (default form encoding)
    // 2) "5 3"       (if using enctype="text/plain")

    if (input.find("a=") != string::npos) {
        // Handle application/x-www-form-urlencoded
        size_t pos_a = input.find("a=");
        size_t pos_b = input.find("b=");

        if (pos_a != string::npos)
            a = stod(input.substr(pos_a + 2));

        if (pos_b != string::npos)
            b = stod(input.substr(pos_b + 2));
    }
    else {
        // Handle plain text input like "5 3"
        istringstream iss(input);
        iss >> a >> b;
    }

    double result = a - b;

    // Print HTML (no Content-Type header if server already adds it)
    cout << "<html><body>";
    cout << "<h1>Result: " << a << " - " << b << " = " << result << "</h1>";
    cout << "</body></html>";

    return 0;
}