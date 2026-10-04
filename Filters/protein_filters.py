class Filter:
    def filtering(self, proteins):
        pass


class LengthFilter(Filter):
    def filtering(self, proteins):
        result = []
        for protein in proteins:
            if len(protein) >= 4:
                result.append(protein)

        return result


class WeightFilter(Filter):
    def __init__(self, weights):
        self.weights = weights

    def filtering(self, proteins):
        result = []

        for protein in proteins:
            weight = 0

            for amino_asid in protein:
                weight += self.weights[amino_asid]

            if weight >= 400:
                result.append(protein)

        return result

