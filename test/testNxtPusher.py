# coding=UTF-8

import unittest
from mock import MagicMock, call
import sys
sys.path.insert(0, '../picam_server')
from  nxtPusher import *
import nxt

class TestNxt(unittest.TestCase):
    def test_nxt_push_2(self):
        mock = MagicMock()
        nxt_push(mock, 2)
        assert mock.cmd.mock_calls == [call(nxt.PORT_B, 100, MOTOR_ROTATION)]

    def test_nxt_push_1(self):
        mock = MagicMock()
        nxt_push(mock, 1)
        assert mock.cmd.mock_calls == [call(nxt.PORT_B, -100, MOTOR_ROTATION)]

    def test_nxt_push_invalid_classification2(self):
        mock = MagicMock()
        with self.assertRaises(ValueError):
            nxt_push(mock, 7)

if __name__ == '__main__':
    unittest.main()
