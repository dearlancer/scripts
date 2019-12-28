#下载并推送frida-server到安卓手机中并启动
# use:   sh frida.sh
function getLastVersion(){
  data=$(curl -s https://github.com/frida/frida/releases/latest)
  version=$(expr "$data" : '.*tag\/\(.*\)">redirected')
  echo 'last version:'$version
}

function install(){
  curl -O -L 'https://github.com/frida/frida/releases/download/'$version'/frida-server-'$version'-android-arm64.xz'
  xz -d 'frida-server-'$version'-android-arm64.xz'
  echo '下载并解压成功，开始推送到安卓手机中，请保持usb连接可用'
  adb push 'frida-server-'$version'-android-arm64' /data/local/tmp/frida-server
  adb shell "su -c 'chmod 755 /data/local/tmp/frida-server'"
  echo 'frida-server成功推送，开始启动。。。'
  adb shell "su -c '/data/local/tmp/frida-server &'"
  rm 'frida-server-'$version'-android-arm64.xz'
  # rm 'frida-server-'$1'-android-arm64'
}

getLastVersion
install
