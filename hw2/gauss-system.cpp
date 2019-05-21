#include <iostream>
#include <vector>

using namespace std;

int n;

vector<vector<double>> findmaxandswap(int ch, vector<vector<double>> system) {
    double max = -99999.0;
    int pos = -1;
    for (int i = 0; i < n; i++) {
        if (system[i][ch] > max) {
            max = system[i][ch];
            pos = i;
        }
    }
    for (int i = 0; i < n + 1; i++) {
        swap(system[pos][i], system[ch][i]);
    }
    return system;
}

vector<vector<double>> makenull(int ch, vector<vector<double>> system) {
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
        system = findmaxandswap(ch, system);
        for (int i = n; i >= 0; i--) {
            system[ch][i] /= system[ch][ch];
        }
        system = makenull(ch, system);
        ch++;
    }
    return system;
}

int main() {
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);
    cin >> n;
    vector<vector<double>> system;
    system.resize(n);
    for (int i = 0; i < n; i++) {
        system[i].resize(n + 1);
        for (int j = 0; j < n + 1; j++) {
            double tmp;
            cin >> tmp;
            system[i][j] = tmp;
        }
    }
    system = solve(system);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n + 1; j++) {
            cout << system[i][j] << ' ';
        }
        cout << endl;
    }
    return 0;
}