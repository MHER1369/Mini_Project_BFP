WATER_MASS = 18.015


class Filter:

    def filtering(self, proteins):
        raise NotImplementedError(
            "Subclasses must implement filtering()."
        )


class LengthFilter(Filter):

    def __init__(self, min_length):
        self.min_length = min_length

    def filtering(self, proteins):
        result = []

        for protein in proteins:

            if len(protein) >= self.min_length:
                result.append(protein)

        return result


class WeightFilter(Filter):

    def __init__(self, weights, min_weight):
        self.weights = weights
        self.min_weight = min_weight

    def filtering(self, proteins):
        result = []

        for protein in proteins:

            weight = WATER_MASS

            for amino_acid in protein:

                if amino_acid not in self.weights:
                    raise ValueError(
                        f"Unknown amino acid: {amino_acid}"
                    )

                weight += self.weights[amino_acid]

            if weight >= self.min_weight:
                result.append(protein)

        return result