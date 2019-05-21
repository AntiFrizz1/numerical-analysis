#include <iostream>
#include <vector>

using namespace std;

int n;

vector<vector<double>> findMaxAndSwap(int ch, vector<vector<double>> &system) {
    double max = system[0][ch];
    int pos = -1;
    for (int i = 1; i < n; i++) {
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

vector<vector<double>> makeNull(int ch, vector<vector<double>> &system) {
    for (int i = 0; i < n; i++) {
        if (ch == i) continue;
        double tmp = system[i][ch];
        for (int j = 0; j < n + 1; j++) {
            system[i][j] += -tmp * system[ch][j];
        }
    }
    return system;
}

vector<vector<double>> solve(vector<vector<double>> &system) {
    int ch = 0;
    while (ch < n) {
        system = findMaxAndSwap(ch, system);
        for (int i = n; i >= 0; i--) {
            system[ch][i] /= system[ch][ch];
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
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n + 1; j++) {
            cout << system[i][j] << ' ';
        }
        cout << endl;
    }
    return 0;
}
