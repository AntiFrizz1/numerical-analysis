#include <iostream>
#include <vector>
#include <ctime>
#include <cmath>
#include <iomanip>

using namespace std;

int matrix_size = 10;
int iteration_count = 0;
double eps = 0.001;

vector<double> generate_right(int size) {
    vector<double> tmp;
    for (int i = 0; i < size; i++) {
        tmp.push_back(1 + (rand() % 8));
    }
    return tmp;
}

double max_diff(vector<double> v1, vector<double> v2) {
    double dif = fabs(v2[0] - v1[0]);
    for (int i = 1; i < v1.size(); i++) {
        if (fabs(v2[i] - v1[i]) > dif) {
            dif = fabs(v2[i] - v1[i]);
        }
    }
    return dif;
}

vector<double> solution(vector<vector<double>> matrix, vector<double> right) {
    vector<double> ans;
    vector<double> tmp = generate_right(matrix_size);
    do {
        ans = tmp;
        iteration_count++;
        for (int i = 0; i < matrix_size; i++) {
            tmp[i] = right[i];
            for (int j = 0; j < matrix_size; j++) {
                if (i != j) {
                    tmp[i] -= matrix[i][j] * ans[j];
                }
            }
            tmp[i] /= matrix[i][i];
        }
    } while (max_diff(tmp, ans) > eps);
    return tmp;
}


double check_norm (vector<vector<double>> matrix) {
    double sum = 0.0;
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix.size(); j++) {
            sum += matrix[i][j] * matrix[i][j];
        }
    }
    return sqrt(sum);
}

vector<vector<double>> create_d_matrix(vector<vector<double>> matrix) {
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            if (i != j) {
                matrix[i][j] = 0;
            }
        }
    }
    return matrix;
}

vector<vector<double>> create_dm_matrix(vector<vector<double>> matrix) {
    for (int i = 0; i < matrix_size; i++) {
        matrix[i][i] = 1.0 / matrix[i][i];
    }
    return matrix;
}

vector<vector<double>> minus_matrix(vector<vector<double>> matrix1, vector<vector<double>> matrix2) {
    for (int i = 0; i < matrix_size; i++) {
        for (int j = 0; j < matrix_size; j++) {
            matrix1[i][j] -= matrix2[i][j];
        }
    }
    return matrix1;
}

vector<vector<double>> mul_matrix(vector<vector<double>> matrix1, vector<vector<double>> matrix2) {
    vector<vector<double>> ans;
    ans.resize(matrix_size);
    for (int i = 0; i < matrix_size; i++) {
        ans[i].resize(matrix_size);
        for (int j = 0; j < matrix_size; j++) {
            ans[i][j] = 0;
            for (int k = 0; k < matrix_size; k++) {
                ans[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
    return ans;
}

int main() {
    cin >> matrix_size;
    cin >> eps;
    vector<vector<double>> matrix;
    matrix.resize(matrix_size);
    for (int i = 0; i < matrix_size; i++) {
        matrix[i].resize(matrix_size);
        for (int j = 0; j < matrix_size; j++) {
            cin >> matrix[i][j];
        }
    }
    vector<double> right;
    right.resize(matrix_size);
    for (int i = 0; i < matrix_size; i++) {
        cin >> right[i];
    }
    vector<vector<double>> d = create_d_matrix(matrix);
    if (check_norm(mul_matrix(create_dm_matrix(d), minus_matrix(d, matrix))) < 1) {
        iteration_count = 0;
        vector<double> ans = solution(matrix, right);
        cout << std::fixed;
        for (double an : ans) {
            cout << setprecision(16) << an << " ";
        }
        cout << endl;
        cout << iteration_count << endl;
    } else {
        return -1;
    }
    return 0;
}