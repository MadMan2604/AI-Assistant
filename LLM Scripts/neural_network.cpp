#include <iostream>
#include <vector>
#include <cmath>
#include <Eigen/Dense>

using namespace std;
using namespace Eigen;

// Activation function (sigmoid)
double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// Derivative of the sigmoid function
double sigmoidDerivative(double x) {
    return sigmoid(x) * (1 - sigmoid(x));
}

// Neural network class
class NeuralNetwork {
private:
    int inputSize;
    int hiddenSize;
    int outputSize;
    MatrixXd weightsInputHidden;
    VectorXd biasHidden;
    MatrixXd weightsHiddenOutput;
    VectorXd biasOutput;
public:
    // Constructor
    NeuralNetwork(int inputSize, int hiddenSize, int outputSize) :
            inputSize(inputSize), hiddenSize(hiddenSize), outputSize(outputSize) {
        // Initialize weights and biases with random values
        weightsInputHidden = MatrixXd::Random(hiddenSize, inputSize);
        biasHidden = VectorXd::Random(hiddenSize);
        weightsHiddenOutput = MatrixXd::Random(outputSize, hiddenSize);
        biasOutput = VectorXd::Random(outputSize);
    }

    // Forward pass
    VectorXd forward(const VectorXd& input) {
        // Compute hidden layer output
        VectorXd hiddenOutput = (weightsInputHidden * input + biasHidden).unaryExpr(&sigmoid);

        // Compute output layer output
        VectorXd output = (weightsHiddenOutput * hiddenOutput + biasOutput).unaryExpr(&sigmoid);

        return output;
    }

    // Backward pass (gradient descent)
    void backward(const VectorXd& input, const VectorXd& target, double learningRate) {
        // Forward pass
        VectorXd hiddenOutput = (weightsInputHidden * input + biasHidden).unaryExpr(&sigmoid);
        VectorXd output = (weightsHiddenOutput * hiddenOutput + biasOutput).unaryExpr(&sigmoid);

        // Compute output layer error
        VectorXd outputError = output - target;
        
        // Compute gradients for weights and biases
        MatrixXd deltaWeightsHiddenOutput = (outputError * hiddenOutput.transpose()) * learningRate;
        VectorXd deltaBiasOutput = outputError * learningRate;

        // Update weights and biases for hidden to output layer
        weightsHiddenOutput -= deltaWeightsHiddenOutput;
        biasOutput -= deltaBiasOutput;

        // Compute hidden layer error
        VectorXd hiddenError = (weightsHiddenOutput.transpose() * outputError).cwiseProduct(hiddenOutput.cwiseProduct(VectorXd::Ones(hiddenSize) - hiddenOutput));

        // Compute gradients for weights and biases
        MatrixXd deltaWeightsInputHidden = (hiddenError * input.transpose()) * learningRate;
        VectorXd deltaBiasHidden = hiddenError * learningRate;

        // Update weights and biases for input to hidden layer
        weightsInputHidden -= deltaWeightsInputHidden;
        biasHidden -= deltaBiasHidden;
    }
};

int main() {
    // Define neural network parameters
    int inputSize = 2;
    int hiddenSize = 3;
    int outputSize = 1;

    // Create neural network
    NeuralNetwork nn(inputSize, hiddenSize, outputSize);

    // Define training data (OR gate)
    vector<VectorXd> inputs = {VectorXd::Zero(inputSize), VectorXd::Zero(inputSize), VectorXd::Zero(inputSize), VectorXd::Zero(inputSize)};
    int inputs  = 1;
    int inputs  = 1;
    int inputs  = 1;
    int inputs  = 1;

    vector<VectorXd> targets = {VectorXd::Zero(outputSize), VectorXd::Zero(outputSize), VectorXd::Zero(outputSize), VectorXd::Ones(outputSize)};

    // Train the neural network
    double learningRate = 0.1;
    int epochs = 1000;
    for (int i = 0; i < epochs; ++i) {
        for (int j = 0; j < inputs.size(); ++j) {
            // Forward pass
            VectorXd output = nn.forward(inputs[j]);

            // Backward pass
            nn.backward(inputs[j], targets[j], learningRate);
        }
    }

    // Test the neural network
    for (int i = 0; i < inputs.size(); ++i) {
        VectorXd output = nn.forward(inputs[i]);
        cout << "Input: " << inputs[i].transpose() << ", Output: " << output.transpose() << endl;
    }

    return 0;
}
