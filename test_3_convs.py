from presidio_utils import *
from utils import *


# Create an anonymiser and an analyser
anonymizer = AnonymizerEngine()
anonymizer.add_anonymizer(InstanceCounterAnonymizer)

users = load_users()
users.append({"first_name": "Ag"})
ceda_name_recognizer = PatternRecognizer(supported_entity="CEDA_PERSON", deny_list=[user["first_name"] for user in users])

ceda_paths_pattern = Pattern(name="ceda_paths_pattern", regex=r"/(home/users|gws|group_workspaces)/([a-zA-Z0-9_\-\.]+/?)*", score=1)
ceda_paths_recognizer = PatternRecognizer(supported_entity="CEDA_PATH", patterns=[ceda_paths_pattern])

# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
analyzer = AnalyzerEngine()

# Add my specific recognisers to the analyserss
for recognizer in (ceda_name_recognizer, ceda_paths_recognizer):
    analyzer.registry.add_recognizer(recognizer)


entities = "CREDIT_CARD CRYPTO DATE_TIME EMAIL_ADDRESS IBAN_CODE IP_ADDRESS NRP LOCATION PERSON PHONE_NUMBER MEDICAL_LICENSE URL".split()
entities.extend(["CEDA_PATH", "CEDA_PERSON"])


def get_anonymized_text(text):
    results = analyzer.analyze(text=text, entities=entities, language="en")
    anonymized_text = anonymizer.anonymize(text, results,
                      {"DEFAULT": OperatorConfig("entity_counter", {"entity_mapping": {}})})
    return anonymized_text


def show_one_thread_anonymised():
    text = get_thread(replace={"Matt": "Ag"})
    anon = get_anonymized_text(text)
    print("Anonymised thread as text:", anon.text)
    print("Anonymised item details[:3]:", anon.items[:3])


show_one_thread_anonymised()
print("---------------")
print("Now trying the first 100 JASMIN user names we have...")


def test_thread_with_user(user):
    first_name = user["first_name"]
    text = get_thread(replace={"Matt": first_name})
    anon = get_anonymized_text(text)
    assert first_name not in anon.text, f"Failed with name: {first_name}:\n\n{anon.text}"


def test_thread_with_100_users():
    users = load_users()
    print("Testing...", end="")
    for user in users:
        test_thread_with_user(user)
        print(user["first_name"], end=", ")


test_thread_with_100_users()

print("""\n\nNOTE: You can also include reversible anonymisation.
See: https://python.langchain.com/v0.1/docs/guides/productionization/safety/presidio_data_anonymization/reversible/#quickstart""")
