# VectorDB test program
# Date: 2024/10/03
# Author: araobp@github.com

import sys
sys.path.append("../rag")

import embeddings
import vector_db
import unittest

EMBEDDINGS_DB_PATH = "./test.db"

TEXTS = ["hello!", "how are you?", "I'm fine, thank you!"]

COLLECTION = "hello"

class TestVectorDB(unittest.TestCase):
    """Test vector_db package
    """

    def _collection(self):
        return vector_db.VectorDB(EMBEDDINGS_DB_PATH, COLLECTION, embeddings.DIMENSION)

    def _embeddings(self):
        items = []

        for idx, text in enumerate(TEXTS):
            vector = embeddings.get_embedding(text)
            items.append((idx, vector))

        return items
         
    def  test_instantiate(self):
        """Instantiate a collection
        """
        collection = self._collection() 
        self.assertEqual(type(collection), vector_db.VectorDB)

    def test_delete_all(self):
        """Remove all items in the collection
        """
        collection = self._collection() 
        collection.delete_all()
        items = self._embeddings()
        collection.save(items)
        self.assertEqual(len(collection), len(TEXTS))
        collection.delete_all()
        self.assertEqual(len(collection), 0)

    def test_save_embedding(self):
        """Calculate and save embeddings in the vector database
        """
        collection = self._collection() 
        collection.delete_all()
        items = self._embeddings() 
        collection.save(items)
        self.assertEqual(len(collection), len(TEXTS))

    def test_similarity_search(self):
        """Perform similarity search
        """
        collection = self._collection() 
        text = TEXTS[1]
        print(f"Text to be searched: {text}")
        vector = embeddings.get_embedding(text)
        
        result = collection.search(vector)
        print(f"Search result(k=3): {result}")
        self.assertEqual(result[0][0], 1)
        self.assertEqual(len(result), 3)

        result = collection.search(vector, k=2)
        print(f"Search result(k=2): {result}")
        self.assertEqual(result[0][0], 1)
        self.assertEqual(len(result), 2)
    
if __name__ == "__main__":
    unittest.main()
