class NaiveBayes:

    def __init__(self):
        self.prior = {}
        self.conditional = {}
        self.classes = []

    def fit(self, data):

        total_records = len(data)

        labels = [row[-1] for row in data]

        self.classes = list(set(labels))

        # Calculate Priors
        for c in self.classes:
            self.prior[c] = labels.count(c) / total_records
            self.conditional[c] = {}

        # Calculate Conditionals
        num_features = len(data[0]) - 1

        for c in self.classes:

            sub_data = [
                row[:-1]
                for row in data
                if row[-1] == c
            ]

            sub_total = len(sub_data)

            for f_idx in range(num_features):

                self.conditional[c][f_idx] = {}

                feature_vals = [
                    row[f_idx]
                    for row in data
                ]

                for val in set(feature_vals):

                    count = sum(
                        1
                        for row in sub_data
                        if row[f_idx] == val
                    )

                    # Laplace smoothing
                    self.conditional[c][f_idx][val] = (
                        (count + 1)
                        /
                        (sub_total + len(set(feature_vals)))
                    )

    def predict(self, sample):

        best_class = None
        best_prob = -1.0

        for c in self.classes:

            prob = self.prior[c]

            for f_idx, val in enumerate(sample):

                if val in self.conditional[c][f_idx]:
                    prob *= self.conditional[c][f_idx][val]

            if prob > best_prob:
                best_prob = prob
                best_class = c

        return best_class


# Example Usage
if __name__ == "__main__":

    dataset = [
        ['Sunny', 'High', 'No'],
        ['Sunny', 'High', 'No'],
        ['Overcast', 'High', 'Yes'],
        ['Rainy', 'Normal', 'Yes'],
        ['Rainy', 'Normal', 'Yes']
    ]

    nb = NaiveBayes()

    nb.fit(dataset)

    test_instance = ['Sunny', 'Normal']

    print(
        f"Predicted class for {test_instance}:",
        nb.predict(test_instance)
    )