#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import os, sys
import subprocess
import collections
import time
import textwrap
import getpass
import re
import logging

import alphatwirl

from .exec_util import try_executing_until_succeed, compose_shortened_command_for_logging

##__________________________________________________________________||
# https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=MagicNumbers
HTCONDOR_JOBSTATUS = {
    0: "Unexpanded",
    1: "Idle",
    2: "Running",
    3: "Removed",
    4: "Completed",
    5: "Held",
    6: "Transferring_Output",
    7: "Suspended"
}

##__________________________________________________________________||
class HTCondorJobSubmitter(object):
    def __init__(self, job_desc_extra=[ ]):

        self.job_desc_template = """
        Executable = {job_script}
        output = {out}
        error = {error}
        log = {log}
        {args}
        should_transfer_files = YES
        when_to_transfer_output = ON_EXIT
        transfer_input_files = {input_files}
        transfer_output_files = {output_files}
        Universe = vanilla
        notification = Error
        # Initialdir = {initialdir}
        getenv = True
        queue 1
        """
        self.job_desc_template = textwrap.dedent(self.job_desc_template).strip()

        if job_desc_extra:
            job_desc_list = self.job_desc_template.split('\n')
            job_desc_list[-1:-1] = job_desc_extra
            self.job_desc_template = '\n'.join(job_desc_list)

        self.clusterids_outstanding = [ ]
        self.clusterids_finished = [ ]

    def run(self, workingArea, package_index):

        cwd = os.getcwd()
        os.chdir(workingArea.path)

        package_path = workingArea.package_path(package_index)

        resultdir_basename = os.path.splitext(package_path)[0]
        resultdir_basename = os.path.splitext(resultdir_basename)[0]
        resultdir = os.path.join('results', resultdir_basename)
        alphatwirl.mkdir_p(resultdir)

        input_files = [package_path, 'python_modules.tar.gz']
        input_files = [f for f in input_files if os.path.exists(f)]

        job_desc = self.job_desc_template.format(
            job_script='run.py',
            out=os.path.join(resultdir, 'stdout.txt'),
            error=os.path.join(resultdir, 'stderr.txt'),
            log=os.path.join(resultdir, 'log.txt'),
            args='Arguments = {}'.format(package_path),
            input_files=', '.join(input_files),
            output_files='results',
            initialdir='to be determined',
        )

        procargs = [
            '/usr/bin/condor_submit',
            '-append', 'accounting_group=group_physics.hep',
            '-append', 'accounting_group_user={}'.format(getpass.getuser()),
        ]

        logger = logging.getLogger(__name__)
        command_display = compose_shortened_command_for_logging(procargs)
        logger.debug('execute: {!r}'.format(command_display))

        proc = subprocess.Popen(
            procargs,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = proc.communicate(job_desc)

        for l in stdout.rstrip().split(b'\n'):
            logger.debug(l)

        regex = re.compile(b"(\d+) job\(s\) submitted to cluster (\d+)", re.MULTILINE)
        njobs = int(regex.search(stdout).groups()[0])
        clusterid = regex.search(stdout).groups()[1]

        self.clusterids_outstanding.append(clusterid)

        change_job_priority([clusterid], 10) ## need to make configurable

        os.chdir(cwd)

        return clusterid

    def poll(self):
        """check if the jobs are running and return a list of cluster IDs for
        finished jobs

        """

        clusterid_status_list = query_status_for(self.clusterids_outstanding)
        # e.g., [['1730126', 2], ['1730127', 2], ['1730129', 1], ['1730130', 1]]


        if clusterid_status_list:
            clusterids, statuses = zip(*clusterid_status_list)
        else:
            clusterids, statuses = (), ()

        clusterids_finished = [i for i in self.clusterids_outstanding if i not in clusterids]
        self.clusterids_finished.extend(clusterids_finished)
        self.clusterids_outstanding[:] = clusterids

        # logging
        counter = collections.Counter(statuses)
        messages = [ ]
        if counter:
            messages.append(', '.join(['{}: {}'.format(HTCONDOR_JOBSTATUS[k], counter[k]) for k in counter.keys()]))
        if self.clusterids_finished:
            messages.append('Finished {}'.format(len(self.clusterids_finished)))
        logger = logging.getLogger(__name__)
        logger.info(', '.join(messages))

        return clusterids_finished

    def wait(self):
        """wait until all jobs finish and return a list of cluster IDs
        """
        sleep = 5
        while self.clusterids_outstanding:
            self.poll()
            time.sleep(sleep)
        return self.clusterids_finished

    def failed_runids(self, runids):
        # remove failed clusterids from self.clusterids_finished
        # so that len(self.clusterids_finished)) becomes the number
        # of the successfully finished jobs
        for i in runids:
            try:
                self.clusterids_finished.remove(i)
            except ValueError:
                pass

    def terminate(self):
        n_at_a_time = 500
        ids_split = [self.clusterids_outstanding[i:(i + n_at_a_time)] for i in range(0, len(self.clusterids_outstanding), n_at_a_time)]
        statuses = [ ]
        for ids_sub in ids_split:
            procargs = ['condor_rm'] + ids_sub
            command_display = compose_shortened_command_for_logging(procargs)
            logger = logging.getLogger(__name__)
            logger.debug('execute: {}'.format(command_display))
            proc = subprocess.Popen(
                procargs,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()

##__________________________________________________________________||
def query_status_for(ids, n_at_a_time=500):

    ids_split = split_ids(ids, n=n_at_a_time)
    stdout = [ ]
    for ids_sub in ids_split:
        procargs = ['condor_q'] + ids_sub + ['-format', '%-2s ', 'ClusterId', '-format', '%-2s\n', 'JobStatus']
        stdout.extend(try_executing_until_succeed(procargs))

    # e.g., stdout = ['688244 1 ', '688245 1 ', '688246 2 ']

    ret = [l.strip().split() for l in stdout]
    # e.g., [['688244', '1'], ['688245', '1'], ['688246', '2']]

    ret = [[e[0], int(e[1])] for e in ret]
    # a list of [clusterid, status]
    # e.g., [['688244', 1], ['688245', 1], ['688246', 2]]

    return ret

##__________________________________________________________________||
def change_job_priority(ids, priority=10, n_at_a_time=500):

    # http://research.cs.wisc.edu/htcondor/manual/v7.8/2_6Managing_Job.html#sec:job-prio

    ids_split = split_ids(ids, n=n_at_a_time)
    for ids_sub in ids_split:
        procargs = ['condor_prio', '-p', str(priority)] + ids_sub
        try_executing_until_succeed(procargs)

##__________________________________________________________________||
def split_ids(ids, n=500):
    # e.g.,
    # ids = [3158174', '3158175', '3158176', '3158177', '3158178']
    # n = 2
    # return [[3158174', '3158175'], ['3158176', '3158177'], ['3158178']]
    return [ids[i:(i + n)] for i in range(0, len(ids), n)]

##__________________________________________________________________||
