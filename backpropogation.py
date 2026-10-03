import numpy as np

np.random.seed(42)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def train_backpropagation(X, y, epochs=10000, lr=0.5):

    input_layer_size = X.shape[1]
    hidden_layer_size = 3
    output_layer_size = 1

    # Weights
    wh = np.random.uniform(
        -1, 1,
        (input_layer_size, hidden_layer_size)
    )

    wout = np.random.uniform(
        -1, 1,
        (hidden_layer_size, output_layer_size)
    )

    # Biases
    bh = np.zeros((1, hidden_layer_size))
    bout = np.zeros((1, output_layer_size))

    for _ in range(epochs):

        # Forward propagation
        hidden_layer_input = np.dot(X, wh) + bh
        hidden_layer_activations = sigmoid(hidden_layer_input)

        output_layer_input = (
            np.dot(hidden_layer_activations, wout) + bout
        )

        predicted_output = sigmoid(output_layer_input)

        # Backpropagation
        error = y - predicted_output

        d_predicted_output = (
            error * sigmoid_derivative(predicted_output)
        )

        hidden_layer_error = (
            d_predicted_output.dot(wout.T)
        )

        d_hidden_layer = (
            hidden_layer_error
            * sigmoid_derivative(hidden_layer_activations)
        )

        # Update weights
        wout += (
            hidden_layer_activations.T.dot(d_predicted_output)
            * lr
        )

        wh += (
            X.T.dot(d_hidden_layer)
            * lr
        )

        # Update biases
        bout += np.sum(
            d_predicted_output,
            axis=0,
            keepdims=True
        ) * lr

        bh += np.sum(
            d_hidden_layer,
            axis=0,
            keepdims=True
        ) * lr

    return predicted_output


# XOR dataset
X_xor = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_xor = np.array([
    [0],
    [1],
    [1],
    [0]
])


# Train the neural network
outputs = train_backpropagation(
    X_xor,
    y_xor
)


print("Final outputs:")
print(outputs)

print("\nPredicted classes:")
print((outputs >= 0.5).astype(int))