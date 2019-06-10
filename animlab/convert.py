#! /usr/bin/env python
#
# Python toolset for the mechanistic study of animal behaviour
# Copyright (c) 2018 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import animlab.utils as alu
import animlab.imutils as alimu

import os
import cv2
import sys
import glob
import argparse
import subprocess

from datetime import datetime
from multiprocess import Pool


class KeyboardInterruptError(Exception): pass

class Converter:

    """
    Converter class to convert a directory of videos to mp4 with
    potential to write frame number on each frames

    Parameters
    -----------
    dir : str, default = ""
        Directory containing the videos
    vidtype : str, default = ".h264"
        The filetype of the video to convert
    withframe : bool, default = False
        Type of conversion, either very fast conversion using ffmpeg or
        using opencv to add frame number to each frame
    remove : bool, default = False
        If the original videos should be removed or not
    pools : int, default = 6
        Number of computer cores to use for conversion script
    resizeval : float, default = 1
        Float value to which video should be resized
    """

    def __init__(self, dir = "", vidtype = ".h264", withframe = False,
                 remove = False, pools = 6, resizeval = 1):

        alu.lineprint("Convert function started!", label = "AnimRec")

        self.dir = os.getcwd() if dir == "" else dir
        assert os.path.exists(self.dir), "directory does not exist, try again.."

        self.vidtype = vidtype
        self.withframe = withframe
        self.remove = remove
        self.pools = int(pools)
        self.resizeval = float(resizeval)

        self.conv_files = alu.listfiles(self.dir, self.vidtype, keepdir = True)
        self.flen = len(self.conv_files)
        self.done = False

        self.convertpool()


    def conv_single(self, filein):

        try:
            fileprint = os.path.basename(filein)
            alu.lineprint("Start converting "+fileprint, label = "AnimRec")


            if self.withframe:
                vid = cv2.VideoCapture(filein)
                fps,width,height,_ = alimu.get_vid_params(vid)
                vidout = alimu.videowriter(filein, width, height, fps, self.resizeval)

                while True:
                    flag, frame = vid.read()
                    if flag:
                        frame = alimu.imresize(frame, self.resizeval)
                        frame_nr = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                        alimu.draw_text(frame, str(frame_nr), (10,35), 0.9)
                        vidout.write(frame)
                    if not flag:
                        break

            else:
                if self.resizeval != 1:
                    comm = "' -vf 'scale=iw*" + str(self.resizeval) + ":-2' '"
                else:
                    comm = "' -vcodec copy '"
                bashcomm = "ffmpeg -i '" + filein + comm + filein[:-5] + ".mp4'"
                bashcomm = bashcomm + " -y -nostats -loglevel 0"
                print(bashcomm)
                output = subprocess.check_output(['bash','-c', bashcomm])

            alu.lineprint("Finished converting "+fileprint, label = "AnimRec")


        except KeyboardInterrupt:
            raise KeyboardInterruptError()


    def convertpool(self):

        if len(self.conv_files) > 0:

            pool = Pool(min(self.pools, self.flen))
            try:
                pool.map(self.conv_single, self.conv_files)
                pool.close()
                self.done = True
                alu.lineprint("Converting done!", label = "AnimRec")
            except KeyboardInterrupt:
                alu.lineprint("Got ^C, terminating pool", label = "AnimRec")
                pool.terminate()
            except Exception as e:
                excep = "Got exception: %r, terminating pool" % (e,)
                alu.lineprint(excep, label = "AnimRec")
                pool.terminate()
            finally:
                pool.join()

            if self.done and self.remove:
                for filein in self.conv_files:
                    os.remove(filein)
                alu.lineprint("Removed all original files..", label = "AnimRec")

        else:
            alu.lineprint("no files found..", label = "AnimRec")
