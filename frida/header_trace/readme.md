# Objc Class hook生成脚本
所有的头文件都在headers中，通过main.go来自动生成hook脚本,脚本生成位于script目录下

#### Usage
1. dump class头部到headers中
```
class-dump -H -o headers /Applications/WeChat.app/Contents/MacOS/WeChat
```
2. 生成hook脚本
```
go run main.go MMSessionMgr.h
frida -l ./script/MMSessionMgr.js --no-pause -p pid
```
3. 运行frida进行hook
```
frida -l ./script/MMSessionMgr.js --no-pause -p pid
```
