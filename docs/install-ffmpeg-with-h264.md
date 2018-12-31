<small>Copyright (c) 2018 - 2019 Jolle Jolles<br/>
Last updated: 31 Dec 2018</small>

<h2>Installing ffmpeg with h264 support on Raspberry Pi</h2>
The <a href="https://www.raspberrypi.org">Raspberry Pi</a> is a fantastic little computer for recording video. For about €50,- you can record in HD with full customizability and for as long as you want or have storage for. However, one issue is that the <code>.h264</code> format it records in is hard to work with. It is therefore often important to convert videos to widely applicable formats like <code>.mp4</code> to be able to view them properly and get the right meta information. For this I recommend the program <code>FFmpeg</code>.</p>

<p>Installing <a href="https://www.ffmpeg.org">ffmpeg</a> on a Raspberry Pi is not as simple as downloading an executable from the command line, but it is also not too difficult. Here are the steps:</p>

<h4>Install h264 library</h4>

<ol>
<li>Open a terminal window on the raspberrypi (or via SSH connection) and type in the following commands:</li>
<li>Download h264 library: <code>git clone --depth 1 http://git.videolan.org/git/x264</code> </li>
<li>Change directory to the x264 folder: <code>cd x264</code></li>
<li>Configure installation: <code>./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl</code></li>
<li>Create the installation: <code>make -j4</code></li>
<li>Install h264 library on your system: <code>sudo make install</code></li>
</ol>

<h3>Install ffmpeg with h264</h3>

<ol>
<li>Change to home directory: <code>cd ~</code></li>
<li>Download ffmpeg: <code>git clone git://source.ffmpeg.org/ffmpeg --depth=1</code></li>
<li>Change to ffmpeg directory: <code>cd ffmpg</code></li>
<li>Configure installation: <code>./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree</code></li>
<li>Make the installation: <code>make -j4</code>. <em>Note this step will take a long time!</em></li>
<li>Now finally run the installation: <code>sudo make install</code></li>
</ol>

<p>Note: If you are working with an older model of the raspberrypi (&lt; 3 B+) then you may not have 4 cores available. You will then have to change <code>make -j4</code> to <code>make -j</code>.</p>

<h3>Convert h264 video</h3>

<p>Now you are ready to convert a h264 video on your Raspberry Pi! Simply run the following command:</p>

<p><code>ffmpeg -i USER_VIDEO.h264 -vcodec copy USER_VIDEO.mp4</code></p>

<p>There are many options available and many other ways to convert h264 videos with ffmpeg, but this command is the quickest of all methods that I tested.</p>

