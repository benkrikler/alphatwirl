import os
import sys
import logging
import textwrap

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import SGEJobSubmitter

##__________________________________________________________________||
@pytest.fixture()
def subprocess():
    proc_submit = mock.MagicMock(name='qsub')
    proc_submit.communicate.return_value = (b'Your job-array 2476030.1-1:1 ("job_script.sh") has been submitted', b'')

    proc_submit_2 = mock.MagicMock(name='qsub')
    proc_submit_2.communicate.return_value = (b'Your job-array 2476030.1-3:1 ("job_script.sh") has been submitted', b'')

    #proc_query = mock.MagicMock(name='qstat')
    #proc_query.communicate.return_value = (
    #    b'job-ID  prior   name          user         state submit/start at     queue                          slots ja-task-ID'+\
    #    b'-----------------------------------------------------------------------------------------------------------------'+\
    #    b'2476030 0.12500 job_script.sh sdb15        qw    02/14/2018 04:15:59                                    1 2'+\
    #    b'2476030 0.12500 job_script.sh sdb15        qw    02/14/2018 04:15:59                                    1 3',
    #    b'',
    #)

    ret = mock.MagicMock(name='subprocess')
    ret.Popen.side_effect = [proc_submit, proc_submit_2]
    return ret

@pytest.fixture()
def obj(monkeypatch, subprocess):
    module = sys.modules['alphatwirl.concurrently.SGEJobSubmitter']
    monkeypatch.setattr(module, 'subprocess', subprocess)
    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module, 'subprocess', subprocess)
    return SGEJobSubmitter()

def test_repr(obj):
    repr(obj)

def test_init_queue_walltime(obj):
    queue = "hep.q"
    walltime = 10800
    obj = SGEJobSubmitter(queue=queue, walltime=walltime)
    assert queue == obj.queue
    assert walltime == obj.walltime

def test_run(obj, tmpdir_factory, caplog):
    workingarea = mock.MagicMock()
    workingarea.path = str(tmpdir_factory.mktemp(''))
    workingarea.package_path.return_value = 'aaa'
    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        assert '2476030.1' == obj.run(workingArea=workingarea, package_index=0)

def test_run_multiple(obj, tmpdir_factory, caplog):
    workingarea = mock.MagicMock()
    workingarea.path = str(tmpdir_factory.mktemp(''))
    workingarea.package_path.return_value = 'aaa'
    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        obj.run(workingArea=workingarea, package_index=0)
        assert ['2476030.1','2476030.2','2476030.3'] == obj.run_multiple(workingArea=workingarea, package_indices=[0,1,2])

##__________________________________________________________________||
