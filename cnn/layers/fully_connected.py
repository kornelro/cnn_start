import numpy as np

from .layer import Layer


class FullyConnected(Layer):

    def __init__(
        self,
        layer_id: str,
        n_inputs: int,
        n_neurons: int,
        batch_size: int
    ):
        super(FullyConnected, self).__init__(
            layer_id=layer_id,
            n_inputs=n_inputs,
            n_outputs=n_neurons,
            batch_size=batch_size
        )
        self.n_neurons = n_neurons
        self.weights = np.random.uniform(size=(self.n_outputs, self.n_inputs))

    def _run_forward(
        self,
        inputs: np.array
    ) -> np.array:

        self.inputs = inputs

        return np.tensordot(self.weights, inputs, axes=1)

    def _run_backward(
        self,
        error_wrt_output: np.array,
        lr: float
    ) -> np.array:

        output_wrt_weights = np.transpose(self.inputs, axes=(1, 0, 2))
        error_wrt_weights = np.zeros(
            shape=(self.n_outputs, self.n_inputs, self.batch_size)
        )
        for k in range(self.batch_size):
            error_wrt_weights[:, :, k] = np.dot(
                error_wrt_output[:, :, k], output_wrt_weights[:, :, k]
            )

        output_wrt_inputs = self.weights
        error_wrt_inputs = np.tensordot(
            output_wrt_inputs.T, error_wrt_output, axes=1
        )

        self.weights = self.weights + lr * np.mean(error_wrt_weights, axis=2)

        return error_wrt_inputs
