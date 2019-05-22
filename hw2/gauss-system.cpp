#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

int n;

vector<vector<double>> findMaxAndSwap(int ch, vector<vector<double>> system) {
    double max = system[ch][ch];
    int pos = ch;
    for (int i = ch; i < n; i++) {
        if (system[i][ch] > max) {
            max = system[i][ch];
            pos = i;
        }
    }
    swap(system[pos], system[ch]);
    return system;
}

vector<vector<double>> makeNull(int ch, vector<vector<double>> system) {
    for (int i = 0; i < n; i++) {
        if (ch == i) continue;
        double tmp = system[i][ch];
        for (int j = 0; j < n + 1; j++) {
            system[i][j] += -tmp * system[ch][j];
        }
    }
    return system;
}

vector<vector<double>> solve(vector<vector<double>> system) {
    int ch = 0;
    while (ch < n) {
        system = findMaxAndSwap(ch, system);
        double tmp = system[ch][ch];
        for (int i = n; i >= 0; i--) {
            system[ch][i] /= tmp;
        }
        system = makeNull(ch, system);
        ch++;
    }
    return system;
}

int main() {
    cin >> n;
    vector<vector<double>> system;
    system.resize(n);
    for (int i = 0; i < n; i++) {
        system[i].resize(n + 1);
        for (int j = 0; j < n; j++) {
            double tmp;
            cin >> tmp;
            system[i][j] = tmp;
        }
    }
    for (int i = 0; i < n; i++){
        double tmp;
        cin >> tmp;
        system[i][n] = tmp;
    }
    system = solve(system);
    cout << fixed;
    for (int i = 0; i < n; i++) {
        cout << setprecision(16) << system[i][n] << ' ';
    }
    return 0;
}
