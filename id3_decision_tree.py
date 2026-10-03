import math


def entropy(data):
    labels = [row[-1] for row in data]
    total = len(labels)

    counts = {}

    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def split_data(data, attribute_index, value):
    return [
        row[:attribute_index] + row[attribute_index + 1:]
        for row in data
        if row[attribute_index] == value
    ]


def info_gain(data, attribute_index):
    total_entropy = entropy(data)

    values = set(row[attribute_index] for row in data)
    total = len(data)

    sub_entropy = 0.0

    for val in values:
        subset = [
            row for row in data
            if row[attribute_index] == val
        ]

        sub_entropy += (len(subset) / total) * entropy(subset)

    return total_entropy - sub_entropy


def id3(data, features):

    labels = [row[-1] for row in data]

    # If all labels are the same
    if len(set(labels)) == 1:
        return labels[0]

    # If no features are left
    if len(features) == 0:
        return max(set(labels), key=labels.count)

    # Find the feature with maximum information gain
    best_feat_idx = max(
        range(len(features)),
        key=lambda i: info_gain(data, i)
    )

    best_feature = features[best_feat_idx]

    tree = {best_feature: {}}

    # Remove selected feature
    remaining_features = [
        f for i, f in enumerate(features)
        if i != best_feat_idx
    ]

    # Get possible values
    feature_values = set(
        row[best_feat_idx]
        for row in data
    )

    # Build branches
    for val in feature_values:

        subset = split_data(
            data,
            best_feat_idx,
            val
        )

        tree[best_feature][val] = id3(
            subset,
            remaining_features
        )

    return tree


# Example Usage
if __name__ == "__main__":

    dataset = [
        ['Sunny', 'Hot', 'High', 'Weak', 'No'],
        ['Sunny', 'Hot', 'High', 'Strong', 'No'],
        ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
        ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
        ['Rain', 'Cool', 'Normal', 'Weak', 'Yes']
    ]

    features = [
        'Outlook',
        'Temperature',
        'Humidity',
        'Wind'
    ]

    tree = id3(dataset, features)

    print("Generated ID3 Decision Tree:")
    print(tree)