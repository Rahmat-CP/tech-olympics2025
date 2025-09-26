import unittest

from packet import Packet
from receiver import Receiver
from transmitter import Transmitter


def test_hash(data: str, key: str) -> str:
    return f"HT::{key}::{data}"

class ReceiverSampleTest(unittest.TestCase):
    def test_packet(self):
        p = Packet(sequence_number=5, data="chunk", hashed_data=test_hash("chunk", "k"))
        self.assertEqual(p.sequence_number, 5)
        self.assertEqual(p.data, "chunk")
        self.assertEqual(p.hashed_data, test_hash("chunk", "k"))
        self.assertTrue(p.is_valid(test_hash, "k"))

    def test_receiver(self):
        key = "key"
        r = Receiver(key)
        r._hash_function = test_hash
        packets = [
            Packet(1, "d", test_hash("d", key)),
            Packet(2, "junk", "bad-key"),
            Packet(0, "a", test_hash("a", key)),
        ]
        r.receive(packets)
        self.assertEqual(r.get_message(), "ad")


    def test_transmitter(self):
        class ExampleReceiver(Receiver):
            def __init__(self, key):
                super().__init__(key)
                self._hash_function = test_hash
                self.received = None
            def receive(self, packets):
                self.received = list(packets)
                super().receive(packets)

        tx = Transmitter(key="k", bait_count=3, chunk_size=3)
        tx._hash_function = test_hash
        r = ExampleReceiver("k")
        packets = tx.transmit("abcdefghij", r)
        self.assertIsNotNone(r.received)
        self.assertEqual(len(r.received), 7)
        self.assertEqual(sum(p.is_valid(test_hash, "k") for p in packets), 4)


    def test_integration(self):
        key = 'a-secret-key-for-hashing-%^#@'
        transmitter = Transmitter(key, bait_count=10)
        receiver = Receiver(key)
        message = 'hello from under water! this is spongebob sending message to patrik! do you copy?'
        transmitter.transmit(message, receiver)
        self.assertEqual(receiver.get_message(), message)