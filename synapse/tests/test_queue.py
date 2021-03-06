import io
import time
import unittest

import synapse.lib.queue as s_queue
import synapse.lib.threads as s_threads

class QueueTest(unittest.TestCase):

    def test_queue_base(self):
        q = s_queue.Queue()
        q.put('woot')

        self.assertEqual( q.get(), 'woot' )
        self.assertIsNone( q.get(timeout=0.1) )

        q.fini()

    def test_queue_bulk(self):

        q = s_queue.BulkQueue()
        q.put( 1 )
        q.extend( (2,3) )

        res = tuple(q.get(timeout=3))
        self.assertEqual( res, (1,2,3) )

        q.fini()

    def test_queue_bulk_abandon(self):
        q = s_queue.BulkQueue()
        self.assertFalse( q.abandoned(2) )

        time.sleep(0.02)
        self.assertTrue( q.abandoned(0.01) )

        q.fini()

    def test_queue_hybernate(self):
        f = io.BytesIO()
        q = s_queue.BulkQueue()

        q.extend([ 'foo', 'bar' ])
        q.hyber(f)

        q.put('baz')
        q.extend(['faz'])

        rows = tuple(q.get())
        self.assertEqual( rows, ('foo','bar','baz','faz') )

        q.put('baz')
        self.assertEqual( len(q.get()), 1 )
