#!/bin/bash

PERL_HOME=/usr/bin
#Configure PATH to Assemblathon1 perl script
ASSEMBLATHON1_HOME=/usr/local/assemblathon1/current
PATH="$PERL_HOME:$ASSEMBLATHON1_HOME:$PATH"
export PERL_HOME ASSEMBLATHON1_HOME PATH
