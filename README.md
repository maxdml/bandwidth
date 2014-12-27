bandwidth
=========

tool to get pageload time for a range of url and extract timing means


Howto:

- setup an apache server with mod_ssl activated
- put the listener in an accessible directory bandwidth/listener (the data are sent to https://127.0.0.1/bandwidth/listener.php)
- create a file named raw_data in the listener directory and set it to 777 (I know :)
- install chrome extension page load time (https://chrome.google.com/webstore/detail/page-load-time/fploionmjgeclbkemipmkogoaohcdbig)
- apply the patch timer.patch on the extension file timer.js (on Linux, at least Fedora, one can find it under ~/.config/google-chrome/Default/Extensions/fploionmjgeclbkemipmkogoaohcdbig/1.2.2_0)
- to get ride of chrome cache, download the extension 'Cache Killer' and configure it to be on when the browser is starting

Since this last step, Chrome should start sending data about tab's loading time to the listener (note: chrome has to be launched in CLI with the option --ignore-certificate-errors)

The entry point for data collection is the script bandwidth.py. Arguments are detailed by the -h switch.
Details of each run of the serie are saved in a file with the bw rate and date in the name.
Means are computed and presented in a separate json/csv (?) file.
