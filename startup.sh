#!/bin/bash
ps -ef | grep test_videos_dir.py | grep python &> /dev/null
if [ $? != 0 ]; then
	python test_video_orig.py DPW DPW_done &
fi

