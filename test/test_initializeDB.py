import unittest
from unittest.mock import MagicMock, patch
import pymongo
from src import initializeDB

class TestInitializeDB(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def test_create_database(self, mock_client):
        # Crear una instancia simulada de MongoClient
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        # Simular que la colección no existe en la base de datos
        mock_db.list_collection_names.return_value = []

        # Llamar a la función con la instancia simulada de MongoClient
        initializeDB.create_database(mock_client, 'test_db', 'test_collection')

        # Verificar que se llamó a los métodos correctos en la instancia simulada de MongoClient
        mock_client.__getitem__.assert_called_once_with('test_db')
        mock_db.list_collection_names.assert_called_once()
        mock_db.create_collection.assert_called_once_with('test_collection')

    @patch('pymongo.MongoClient')
    def test_create_database_collection_exists(self, mock_client):
        # Crear una instancia simulada de MongoClient
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        # Simular que la colección ya existe en la base de datos
        mock_db.list_collection_names.return_value = ['test_collection']

        # Llamar a la función con la instancia simulada de MongoClient
        initializeDB.create_database(mock_client, 'test_db', 'test_collection')

        # Verificar que se llamó a los métodos correctos en la instancia simulada de MongoClient
        mock_client.__getitem__.assert_called_once_with('test_db')
        mock_db.list_collection_names.assert_called_once()
        mock_db.create_collection.assert_not_called()

if __name__ == '__main__':
    unittest.main()

