#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-ook_blocks author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class ook_demod_ui(gr.basic_block):
    """
    docstring for block ook_demod_ui
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="ook_demod_ui",
            in_sig=[np.ubyte, ],
            out_sig=[np.int32,np.int32 ])

        self.onesamples = 0
        self.zerosamples = 0
        self.lastsample = np.array([])

    def forecast(self, noutput_items, ninputs):
        # ninputs is the number of input connections
        # setup size of input_items[i] for work call
        # the required number of input items is returned
        #   in a list where each element represents the
        #   number of required items for each input
        ninput_items_required = [noutput_items] * ninputs
        return ninput_items_required

    def general_work(self, input_items, output_items):
        # For this sample code, the general block is made to behave like a sync block

        dstr = ""

        samples = input_items[0].astype(np.int)
        self.consume(0, len(samples))
        #dstr += f"fls {samples[0:1]} {samples[-1]}\n"

        diff = None
        if len(self.lastsample)==0:
            self.lastsample = np.array([samples[0]])
            if self.lastsample==0:
                self.zerosamples = 1
            else:
                self.onesamples = 1
            samples = samples[1:]

        #print("len samples",len(samples))

        if len(samples)==0: # not tested
            #dstr += f"only one sample"
            #dstr = bytes(dstr, 'utf-8')
            #dstr = [x for x in dstr]
            output_items[0][:0] = []
            output_items[1][:len(dstr)] = np.array(dstr,'ubyte')
            self.produce(0, 0)
            self.produce(1, len(dstr))
            return gr.WORK_CALLED_PRODUCE

        b = np.concatenate((self.lastsample, samples[:-1])).astype(np.int)
        diff = samples-b

        raises = np.where(diff==1)[0]
        falls = np.where(diff==-1)[0]

        #vout = []
        zout = np.array([])
        oout = np.array([])

        if len(raises)+len(falls)==0:
            if samples[0]==0:
                self.zerosamples += len(samples)
            else:
                self.onesamples += len(samples)
        else:
            if self.zerosamples>0:
                if samples[0]==0:
                    if len(raises)==0:
                        self.onesamples += len(samples)
                    else:
                        self.zerosamples += raises[0]
                #vout.append(self.zerosamples)
                zout = np.concatenate((zout,np.array([self.zerosamples])))
                self.zerosamples = 0

                #print(f"e0, fs {samples[0]}")

                if len(raises)==len(falls)+1:
                    zs = raises[1:]-falls
                elif len(raises)==len(falls):
                    zs = raises[1:]-falls[:-1]

                if len(raises)==len(falls):
                    os = falls-raises
                elif len(raises)==len(falls)+1:
                    os = falls-raises[:-1]

                if len(raises)==len(falls):
                    self.zerosamples = len(samples)-falls[-1]
                elif len(raises)==len(falls)+1:
                    self.onesamples = len(samples)-raises[-1]

                #print(zs)
                #print(os)

                zout = np.concatenate((zout,zs))
                oout = np.concatenate((oout,os))
                #for i in range(len(os)):
                    #vout.append(os[i])
                    #if i<len(zs):
                        #vout.append(zs[i])

            elif self.onesamples>0:
                if samples[0]==1:
                    if len(falls)==0:
                        self.onesamples += len(samples)
                    else:
                        self.onesamples += falls[0]
                #vout.append(self.onesamples)
                oout = np.concatenate((oout,np.array([self.onesamples])))
                self.onesamples = 0

                # e1 fs same tested
                # e1 fs not same tested
                #print(f"e1, fs {samples[0]}")

                if len(falls)==len(raises)+1:
                    zs = raises-falls[:-1]
                elif len(falls)==len(raises):
                    zs = raises-falls

                if len(falls)==len(raises):
                    os = falls[1:]-raises[:-1]
                elif len(falls)==len(raises)+1:
                    os = falls[1:]-raises

                if len(falls)==len(raises):
                    self.onesamples = len(samples)-raises[-1]
                elif len(falls)==len(raises)+1:
                    self.zerosamples = len(samples)-falls[-1]

                #print(zs)
                #print(os)

                zout = np.concatenate((zout,zs))
                oout = np.concatenate((oout,os))
                #for i in range(len(zs)):
                    #vout.append(zs[i])
                    #if i<len(os):
                        #vout.append(os[i])


        #print(vout)
        #print(self.zerosamples, self.onesamples)

        self.lastsample = np.array([samples[-1]])

        """
        ninput_items = min([len(items) for items in input_items])
        noutput_items = min(len(output_items[0]), ninput_items)
        output_items[0][:noutput_items] = input_items[0][:noutput_items]
        self.consume_each(noutput_items)
        return noutput_items
        """
        output_items[0][:len(zout)] = zout
        self.produce(0, len(zout))

        output_items[1][:len(oout)] = oout
        self.produce(1, len(oout))

        return gr.WORK_CALLED_PRODUCE

