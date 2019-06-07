<small>Copyright (c) 2018 - 2019 Jolle Jolles<br/>
Last updated: 7 June 2019</small>

<h2>Installing ffmpeg on Mac OS X</h2>
FFmpeg is a great little program to help convert more or less any media format. I previously wrote an article <a href="http://jollejolles.com/installing-ffmpeg-with-h264-support-on-raspberry-pi/">how to install ffmpeg on the Raspberry Pi</a>. This short tutorial will help you install ffmpeg on Mac, which is luckily a lot simpler!

The easiest way to install ffmpeg is to use <a href="https://brew.sh">HomeBrew</a> a package manager for Mac. If you don’t have homebrew installed on your mac already, run the following command using terminal:

<code>/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"</code>

Once you have Homebrew installed, you can now simply install ffmpeg from terminal with the following command:

<code>brew install ffmpeg</code>

To install ffmpeg with specifical modules, instead of running the above command run below command or remove those modules you do not need:

<code>brew install ffmpeg --with-chromaprint --with-fdk-aac --with-fontconfig --with-freetype --with-frei0r --with-game-music-emu --with-libass --with-libbluray --with-libbs2b --with-libcaca --with-libgsm --with-libmodplug --with-librsvg --with-libsoxr --with-libssh --with-libvidstab --with-libvorbis --with-libvpx --with-opencore-amr --with-openh264 --with-openjpeg --with-openssl --with-opus --with-rtmpdump --with-rubberband --with-sdl2 --with-snappy --with-speex --with-tesseract --with-theora --with-tools --with-two-lame --with-wavpack --with-webp --with-x265 --with-xz --with-zeromq --with-zim</code>

