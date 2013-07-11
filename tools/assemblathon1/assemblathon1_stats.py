"""
A Galaxy wrapper script for the perl script assemblathon_stats.pl
Peter Li - GigaScience and BGI-HK
"""

import optparse
import os
import shutil
import subprocess
import sys
import tempfile

def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()

def cleanup_before_exit(tmp_dir):
    if tmp_dir and os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

def main():
    #Parse command line
    parser = optparse.OptionParser()
    parser.add_option("", "--assembly", dest="assembly")
    parser.add_option("", "--limit", dest="limit")
    parser.add_option("", "--n", dest="n")
    #Outputs for reads
    parser.add_option("", "--results", dest="results")

    opts, args = parser.parse_args()

    #Temp directory for data processing
    tmp_dir = tempfile.mkdtemp(prefix="tmp-assemblathon1-")

    tmp_err_file = tempfile.NamedTemporaryFile(dir=tmp_dir).name
    tmp_stderr = open(tmp_err_file, 'w')

    #Set up command line call
    cmd = "perl /usr/local/assemblathon1/current/assemblathon_stats.pl %s --limit %s --n %s" % (opts.assembly, opts.limit, opts.n)
    cmd += " >%s 2>%s" % (opts.results, tmp_err_file)

    print "Command executed: ", cmd

    #Execute Assemblathon1_stats
    try:
        #Perform Corrector_HA call
        proc = subprocess.Popen(args=cmd, shell=True, cwd=tmp_dir, stderr=tmp_stderr)
        returncode = proc.wait()

        # get stderr, allowing for case where it's very large
        tmp_stderr = open(tmp_err_file, 'r')
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += tmp_stderr.read(buffsize)
                if not stderr or len(stderr) % buffsize != 0:
                    break
        except OverflowError:
            pass
        tmp_stderr.close()
        if returncode != 0:
            raise Exception, stderr

    except Exception, e:
        raise Exception, 'Problem performing Assemblathon1_stats process: ' + str(e)

    #Clean up temp files
    cleanup_before_exit(tmp_dir)
    #Check results in output file
    if os.path.getsize(opts.results) > 0:
        sys.stdout.write('Status complete')
    else:
        stop_err("The output is empty")

if __name__ == "__main__":
    main()
