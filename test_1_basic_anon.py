from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

# Initialize the engine:
engine = AnonymizerEngine()

# Invoke the anonymize function with the text, 
# analyzer results (potentially coming from presidio-analyzer) and
# Operators to get the anonymization output:
result = engine.anonymize(text="My name is Bond, James Bond", analyzer_results=[
                            RecognizerResult(entity_type="PERSON", start=11, end=15, score=0.8),
                            RecognizerResult(entity_type="PERSON", start=17, end=27, score=0.8)],
                            operators={"PERSON": OperatorConfig("replace", {"new_value": "BIP"})})

print(result)
