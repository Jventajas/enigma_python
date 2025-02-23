import os
from fastapi.testclient import TestClient
from enigma.machine import Enigma

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from main import app
client = TestClient(app)


def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    # Check a typical title from the template
    assert "Enigma Machine" in response.text

def get_valid_form_data():
    return {
        "plaintext": "HELLO WORLD",
        "left_rotor": "I",
        "center_rotor": "II",
        "right_rotor": "III",
        "left_initial_position": "A",
        "center_initial_position": "A",
        "right_initial_position": "A",
        "left_ring_setting": "A",
        "center_ring_setting": "A",
        "right_ring_setting": "A",
        "reflector": "B",
        "plugboard_connections": "AB CD"
    }

def test_post_valid_input():
    data = get_valid_form_data()
    response = client.post("/", data=data)
    assert response.status_code == 200
    # Make sure the response contains ciphertext output
    # (Depending on how your Enigma.process() works the encrypted text might be different)
    assert "ciphertext" in response.text or "Ciphertext" in response.text
    # Check that the provided plaintext is reflected back in the form (if no exception occurred)
    assert "HELLO WORLD" in response.text


def test_post_missing_plaintext():
    data = get_valid_form_data()
    del data["plaintext"]
    response = client.post("/", data=data)
    # FastAPI should reject the request due to missing required field with a 422 status
    assert response.status_code == 422

def test_post_long_plaintext():
    data = get_valid_form_data()
    # Create a very long plaintext (e.g., 1000 characters)
    long_text = "HELLO " * 200  # 1200 characters approximately
    data["plaintext"] = long_text
    response = client.post("/", data=data)
    assert response.status_code == 200
    # Check that the response has ciphertext output; we cannot anticipate what it will be,
    # but we assume encryption occurs without error.
    assert "Error:" not in response.text


def test_post_with_monkeypatched_exception(monkeypatch):
    # Simulate an exception in the encryption process to test error handling in the endpoint.
    def fake_process(self, plaintext):
        raise Exception("Test exception")

    monkeypatch.setattr(Enigma, "process", fake_process)

    data = get_valid_form_data()
    response = client.post("/", data=data)
    assert response.status_code == 200
    # Check that the returned page contains the error message provided by our fake exception.
    assert "Test exception" in response.text


def test_post_unexpected_rotor_value(monkeypatch):
    # Test with a rotor value that is not normally expected. This may result in an exception
    # if the Enigma implementation checks rotor validity.
    data = get_valid_form_data()
    data["left_rotor"] = "VI"  # An unexpected rotor choice

    # Optionally monkeypatch __init__ to simulate a failure when invalid rotor is provided.
    original_init = Enigma.__init__

    def fake_init(self, rotors, initial_positions, ring_settings, reflector, plugboard_connections):
        # Simulate a validation failure for rotor values.
        if "VI" in rotors:
            raise Exception("Invalid rotor configuration")
        original_init(self, rotors, initial_positions, ring_settings, reflector, plugboard_connections)

    monkeypatch.setattr(Enigma, "__init__", fake_init)

    response = client.post("/", data=data)
    assert response.status_code == 200
    # The error should be handled and rendered in the response template.
    assert "Invalid rotor configuration" in response.text