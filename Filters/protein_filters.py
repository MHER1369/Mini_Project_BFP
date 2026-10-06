from Error_and_Logging.errors import DataFileError
import logging

logger = logging.getLogger("bioforge")


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
                #xxx#
                try:
                    weight += self.weights[amino_asid]
                except KeyError as error:
                    #loggerconnect
                    logger.error("Missing amino acid weight: %s", amino_asid)
                    raise DataFileError(
                        f"Missing amino acid weight: {amino_asid}"
                    ) from error

            if weight >= 400:
                result.append(protein)

        return result
