import json
import os
import pytest
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from clients.storage.storage import StorageClient
from clients.models.client import Client, FireDepartmentService


# clients/storage/test_storage.py

@pytest.fixture
def temp_file_path(tmp_path):
	"""Fixture to create a temporary file for testing."""
	return tmp_path / "test_clients.jsonl"


@pytest.fixture
def sample_client():
	"""Fixture to create a sample client."""
	return Client(
		name='Vitor Barbon 1',
        address='Rua 1, 123 - Bairro - Cidade - SP',
        email='email@email.com',
        phone='(11) 99999-9999',
        occupation='C-2',
        fire_department_service=FireDepartmentService(
            area=100.0,
            fire_load=200.0
		),
	)


def test_add_client_jsonl_creates_file(temp_file_path, sample_client):
	"""Test if add_client_jsonl creates a file and writes the client data."""
	storage_client = StorageClient(file_path=temp_file_path)

	storage_client.add_client_jsonl(sample_client)

	assert os.path.exists(temp_file_path), "File was not created"
	with open(temp_file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()
		assert len(lines) == 1, "File should contain one line"
		data = json.loads(lines[0])
		assert data["id"] == 1, "Client ID should be 1"
		assert data["name"] == sample_client.name, "Client name mismatch"
		assert data["email"] == sample_client.email, "Client email mismatch"


def test_add_client_jsonl_appends_to_existing_file(temp_file_path, sample_client):
	"""Test if add_client_jsonl appends data to an existing file."""
	storage_client = StorageClient(file_path=temp_file_path)

	# Add the first client
	storage_client.add_client_jsonl(sample_client)

	# Add a second client
	second_client = Client(		
		name='Vitor Barbon 2',
        address='Rua 1, 123 - Bairro - Cidade - SP',
        email='email@email.com',
        phone='(11) 99999-9999',
        occupation='C-2',
        fire_department_service=FireDepartmentService(
            area=100.0,
            fire_load=200.0
		),
	)
	storage_client.add_client_jsonl(second_client)

	with open(temp_file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()
		assert len(lines) == 2, "File should contain two lines"
		first_data = json.loads(lines[0])
		second_data = json.loads(lines[1])
		assert first_data["id"] == 1, "First client ID should be 1"
		assert second_data["id"] == 2, "Second client ID should be 2"
		assert second_data["name"] == second_client.name, "Second client name mismatch"
		assert second_data["email"] == second_client.email, "Second client email mismatch"


def test_add_client_jsonl_handles_empty_file(temp_file_path, sample_client):
	"""Test if add_client_jsonl handles an empty file gracefully."""
	storage_client = StorageClient(file_path=temp_file_path)

	# Create an empty file
	temp_file_path.touch()

	storage_client.add_client_jsonl(sample_client)

	with open(temp_file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()
		assert len(lines) == 1, "File should contain one line after adding a client"
		data = json.loads(lines[0])
		assert data["id"] == 1, "Client ID should be 1"
		assert data["name"] == sample_client.name, "Client name mismatch"
		assert data["email"] == sample_client.email, "Client email mismatch"
