#include <iostream>
#include <vector>
#include <Eigen/Dense> // Include Eigen library for matrix operations

using namespace std;
using namespace Eigen;

// Define the RNN language model class
class RNNLanguageModel {
private:
    int vocab_size;
    int hidden_size;
    MatrixXd Wxh; // Weight matrix for input to hidden
    MatrixXd Whh; // Weight matrix for hidden to hidden
    MatrixXd Why; // Weight matrix for hidden to output
    VectorXd bh;  // Bias vector for hidden layer
    VectorXd by;  // Bias vector for output layer
public:
    RNNLanguageModel(int vocab_size, int hidden_size) : vocab_size(vocab_size), hidden_size(hidden_size) {
        // Initialize weight matrices and bias vectors with random values
        Wxh = MatrixXd::Random(hidden_size, vocab_size);
        Whh = MatrixXd::Random(hidden_size, hidden_size);
        Why = MatrixXd::Random(vocab_size, hidden_size);
        bh = VectorXd::Random(hidden_size);
        by = VectorXd::Random(vocab_size);
    }

    // Forward pass through the RNN language model
    VectorXd forward(const vector<int>& inputs, VectorXd hprev) {
        VectorXd x(vocab_size);
        VectorXd h(hidden_size);
        VectorXd y(vocab_size);

        for (int t = 0; t < inputs.size(); ++t) {
            // One-hot encode input vector
            x.setZero();
            x(inputs[t]) = 1.0;

            // Hidden state update
            h = (Wxh * x + Whh * hprev + bh).array().tanh();

            // Output calculation
            y = Why * h + by;
        }

        return y;
    }
};

int main() {
    const int vocab_size = 10000;
    const int hidden_size = 128;
    RNNLanguageModel rnn(vocab_size, hidden_size);

    // Example usage: Forward pass through the model
    vector<int> inputs = {10, 20, 30, 40}; // Example input sequence
    VectorXd hprev = VectorXd::Zero(hidden_size); // Initial hidden state
    VectorXd output = rnn.forward(inputs, hprev);
    
    cout << "Output vector size: " << output.size() << endl;
    cout << "Example output: " << output.transpose() << endl;

    return 0;
}

int thought() {
    const int word_count = 10000;
    const int thought_size = 1380;
    RNNLanguageModel rnn(word_count, thought_size);


}